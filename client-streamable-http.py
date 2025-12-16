"""MCP Streamable HTTP Client"""

import asyncio
import json
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from anthropic import Anthropic
from dotenv import load_dotenv

from openai import AsyncOpenAI

from prompts import *

base_url="https://api.deepseek.com"
api_key='sk-00141ef3447840dda7bc7f06f7318d9d'
model_name="deepseek-chat"

load_dotenv()

def get_clear_json(text):
    """
    从输入的文本中提取JSON格式的内容
    参数:
        text (str): 包含可能JSON格式内容的文本
    返回:
        tuple: (状态码, 提取的内容)
            状态码为1表示成功提取JSON内容，为0表示未找到JSON格式
            提取的内容为去除标记后的纯JSON字符串
    """
    # 检查文本中是否包含JSON标记
    if '```json' not in text:
        # 如果没有找到JSON标记，返回状态码0和原始文本
        return 0, text
    # 如果找到JSON标记，分割文本并提取JSON内容
    return 1, text.split('```json')[1].split('```')[0]

class MCPClient:
    """MCP Client for interacting with an MCP Streamable HTTP server"""

    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.client = AsyncOpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    async def connect_to_streamable_http_server(
        self, server_url: str, headers: Optional[dict] = None
    ):
        """Connect to an MCP server running with HTTP Streamable transport"""
        self._streams_context = streamablehttp_client(  # pylint: disable=W0201
            url=server_url,
            headers=headers or {},
        )
        read_stream, write_stream, _ = await self._streams_context.__aenter__()  # pylint: disable=E1101

        self._session_context = ClientSession(read_stream, write_stream)  # pylint: disable=W0201
        self.session: ClientSession = await self._session_context.__aenter__()  # pylint: disable=C2801

        await self.session.initialize()

    async def process_query(self, query: str) -> str:
        """使用 LLM 和 MCP 服务器提供的工具处理查询"""

        response = await self.session.list_tools()

        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT + str(available_tools)
            },
            {
                "role": "user",
                "content": query
            }
        ]
        response = await self.client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        message = response.choices[0].message

        results = []
        while True:

            flag, json_text = get_clear_json(message.content)

            if flag == 0:
                response = await self.client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": query}]
                )
                return response.choices[0].message.content

            json_text = json.loads(json_text)
            tool_name = json_text['name']
            tool_args = json_text['params']
            result = await self.session.call_tool(tool_name, tool_args)
            results.append(result.content[0].text)

            messages.append({
                "role": "assistant",
                "content": message.content
            })
            messages.append({
                "role": "user",
                "content": f'工具调用结果如下：{result}'
            })

            messages.append({
                "role": "user",
                "content": NEXT_STEP_PROMPT.format(query)
            })

            response = await self.client.chat.completions.create(
                model=model_name,
                messages=messages
            )

            message = response.choices[0].message

            if 'finish' in message.content:
                break

            messages.append({
                "role": "assistant",
                "content": message.content
            })

        messages.append({
            "role": "user",
            "content": FINISH_GENETATE.format('\n\n'.join(results), query)
        })

        response = await self.client.chat.completions.create(
            model=model_name,
            messages=messages
        )

        message = response.choices[0].message.content
        return message

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:  # pylint: disable=W0125
            await self._streams_context.__aexit__(None, None, None)  # pylint: disable=E1101


async def main():
    """Main function to run the MCP client"""
    client = MCPClient()
    try:
        await client.connect_to_streamable_http_server(
            "http://localhost:8001/mcp"
        )
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())