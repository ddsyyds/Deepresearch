from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import asyncio

async def main():
    try:
        server_url = "http://127.0.0.1:8001/mcp"
        async with streamablehttp_client(url=server_url) as (read, write, get_session_id):
            async with ClientSession(read, write) as session:
                print(f"连接成功!")
                # 初始化会话
                await session.initialize()
                print("会话初始化完成")
                # 获取会话 ID
                session_id = get_session_id()
                print(f"会话 ID: {session_id}")
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(tool)
    except Exception as e:
        print(f"连接失败: {e}")
if __name__ == "__main__":
    asyncio.run(main())
