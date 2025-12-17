# DeepResearch Demo

DeepResearch 是一个基于 MCP (Model Coordination Protocol) 的智能研究助理系统。

## 项目概述

该项目结合了 MCP 协议、大型语言模型（如 DeepSeek）和网络搜索技术，能够自动进行深度研究并生成分析报告。

## 核心组件

### 1. MCP 服务器 (altitude_mcp_server.py)

MCP 服务器提供了核心的研究能力，包括：

- **网络搜索功能**：集成 Searxng 搜索引擎进行信息检索
- **网页内容提取**：使用 Jina Reader 提取网页文本内容
- **内容相关性评估**：利用 LLM 判断网页内容与查询的相关性
- **上下文提取**：从相关网页中提取有用信息
- **迭代搜索优化**：根据已有信息确定是否需要进一步搜索及生成新查询

### 2. MCP 客户端

项目包含多种客户端实现：

- **HTTP 流式客户端** (client-streamable-http.py)：支持与 MCP 服务器进行流式通信
- **标准测试客户端** (client-stdio.py)：用于测试服务器连接和工具发现
- **streamable-http** (test.py)：测试 MCP 流式通信的另一实现

### 3. Searxng 搜索引擎

项目集成了 Searxng 搜索引擎，提供私有化的网络搜索能力：
- 支持 Docker 部署
- 包含 Caddy 反向代理和 Valkey 数据库
- 支持 HTTPS 自动证书配置

## 工作流程

1. 用户提出查询问题
2. 系统生成多个精确的搜索查询词
3. 通过 Searxng 进行网络搜索获取链接
4. 抓取网页内容并评估相关性
5. 提取相关上下文信息
6. 根据已有信息判断是否需要进一步研究
7. 整合所有信息生成专业报告

## 主要特性

- **智能搜索**：自动生成精准搜索查询词
- **内容筛选**：自动评估网页内容的相关性和有用性
- **迭代研究**：支持多轮搜索和信息补充
- **专业报告生成**：针对军事领域生成专业分析报告
- **模块化设计**：基于 MCP 协议，易于扩展工具和功能

## 技术栈

- Python 3.x
- MCP (Model Coordination Protocol)
- DeepSeek 大语言模型
- Searxng 搜索引擎
- Jina Reader 网页内容提取
- Docker 容器化部署

## 使用方法

1. 启动 Searxng 搜索引擎：
   ```bash
   cd searxng
   docker compose up -d
   ```

2. 配置并启动 MCP 服务器：
   ```bash
   python altitude_mcp_server.py
   ```

3. 运行客户端进行交互：
   ```bash
   python client-streamable-http.py
   ```
   ```bash
   python client-stdio.py
   ```