<h1 align="center">欢迎来到 Arcs-MCP 👋</h1>

[![python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&labelColor=61DAFB&style=for-the-badge)](https://github.com/Cyanty/Arcs-MCP)
[![fastapi](https://img.shields.io/badge/FastAPI-0.115.11-009688?logo=fastapi&labelColor=61DAFB&style=for-the-badge)](https://github.com/Cyanty/Arcs-MCP)
[![uv](https://img.shields.io/badge/uv-0.7.19-DE5FE9?logo=UV&labelColor=61DAFB&style=for-the-badge)](https://github.com/Cyanty/Arcs-MCP)
[![chrome](https://img.shields.io/badge/chrome-4285F4?logo=googlechrome&labelColor=61DAFB&style=for-the-badge)](https://github.com/Cyanty/Arcs-MCP)
[![license](https://img.shields.io/badge/License-Apache%202.0-blue?labelColor=61DAFB&style=for-the-badge)](https://github.com/Cyanty/Arcs-MCP)
[![mcp](https://img.shields.io/badge/MCP-412991?logo=modelcontextprotocol&labelColor=61DAFB&style=for-the-badge)](https://github.com/Cyanty/Arcs-MCP)
<a href="https://deepwiki.com/Cyanty/Arcs-MCP"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki" style="width: 150px; height: 29px;"></a>

---

# 支持MCP服务的多平台一键发布工具

## 📖 概述

如果有将文章分享发布到多个平台的需求，可以借助这个工具来简化这一流程。该发布工具支持MCP服务，可以让用户使用自然语言处理并实现文章在多个平台的一键式发布。

用户可以描述他们想要实现的效果，例如，“将这篇文章发布到CSDN上。”——工具会自动将文章发布到指定的发布源平台上。

## 🔑 前置条件

- 兼容 MCP 的 AI 客户端：Claude 桌面版、Gemini CLI、Cherry Studio 或其他 MCP 客户端。
- uv：一个现代的 Python 包安装器和解析器。

## 📦 安装与配置

### 1. 安装 uv 环境

这里推荐使用 [Cherry Studio](https://docs.cherry-ai.com/advanced-basic/mcp) 客户端来配置该工具的MCP服务，操作和环境配置会更加友好。Cherry Studio 还自带了 uv 环境的部署功能，用户可以一键完成安装。

> **Tips**：Cherry Studio 目前只使用内置的 [uv](https://github.com/astral-sh/uv) 和 [bun](https://github.com/oven-sh/bun)，**不会复用**系统中已经安装的 uv 和 bun。

也可选择**手动独立安装** uv 环境，使用命令行完成部署：

**macOS & Linux**

```sh
# 使用 `curl` 下载脚本并通过 `sh` 执行：
curl -LsSf https://astral.sh/uv/install.sh | sh

# 如果系统没有 `curl`，可以使用 `wget`：
wget -qO- https://astral.sh/uv/install.sh | sh
```

**Windows**

```sh
# 使用 `irm` 下载脚本并通过 `iex` 执行：
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. 克隆仓库

1. 克隆仓库并切换至该目录：

```sh
git clone https://github.com/Cyanty/Arcs-MCP.git
cd Arcs-MCP
```

2. 复制环境配置文件：

```sh
cp .env.example .env
```

> **Tips**：部分平台支持 API 发布文章，可通过`.env`文件配置所需平台密钥。

3. 构建并运行服务：

```sh
uv run --directory your/path/to/Arcs-MCP server.py
```

### 3. 配置 MCP 客户端

配置您的 MCP 客户端，这里我们以 [Cherry Studio](https://docs.cherry-ai.com/advanced-basic/mcp) 的AI客户端工具为例。

- 在 `添加服务器` 按钮中点击 `快速创建` 选项，选择 *可流式传输的HTTP (streamableHttp) 类型* ，并添加如下URL：

```http
http://127.0.0.1:8001/submit/mcp
```

`快速创建`配置如下图所示：

![](https://raw.githubusercontent.com/Cyanty/images/main/collect/Snipaste_2025-07-15_10-56-27.png)

或者 采用JSON配置，

- 在 `添加服务器` 按钮中点击 `从JSON导入` 选项，将以下内容添加到配置文件中：

```json
{
  "mcpServers": {
    "SubmitArticleServer": {
      "type": "streamableHttp",
      "url": "http://localhost:8001/submit/mcp"
    }
  }
}
```

## 🚀 使用方法

> **Tips**：在开始之前，请确保您的 MCP 客户端已成功完成上述配置。

### 可用工具

可用工具一览：

![](https://raw.githubusercontent.com/Cyanty/images/main/collect/Snipaste_2025-07-15_11-20-14.png)

工具说明：

**help_open_browser**：帮助用户打开一次浏览器（MCP发布浏览器），例如："请帮我打开浏览器"，用户可通过此浏览器进行**账号登录**等操作。

**submit_verify_login**：校验所有发布源平台的账号登录状态，例如："请帮我验证所有平台的登录状态"，用户可通过此方法验证各平台账号登录状态及个人令牌/密钥是否有效。

**get_submit_toggle_switch**：获取当前各发布源的发布开关状态，例如："请告诉我当前各平台的发布开关状态"，发布开关用于为用户标识哪些平台是可以进行发布文章操作的。

**update_submit_toggle_switch**：更新各发布源平台的发布开关状态，例如："请开启CSDN平台的发布开关"，开启平台发布开关可用于发布文章到指定的平台。

**submit_article_content_prompt**：发布文章的文本内容到各平台，例如："将文章的文本内容发布到CSDN上"，等待发布操作完成，就可以在发布的平台上看到自己的文章了。

**submit_article_file_to_platforms**：通过文章的文件路径发布到各平台，例如："帮我把`/your/path/to/file-absolute-path`这篇文章发布到CSDN上"，等待发布操作完成，就可以在发布的平台上看到自己的文章了。

### 发布文章示例

> **Tips**：在发布之前，请确保您的 MCP发布浏览器及个人令牌/密钥 -> 处于登录或可用状态。

使用 [Cherry Studio](https://docs.cherry-ai.com/advanced-basic/mcp) 通过聊天的方式发布一篇文章到 CSDN 上。

在新建聊天窗口中，点击 MCP服务器，选中之前配置的 *SubmitArticleServer* MCP服务：

![](https://raw.githubusercontent.com/Cyanty/images/main/collect/Snipaste_2025-07-15_11-25-09.png)

在聊天框中输入，比如："帮我把这篇文章发布到CSDN上。文章的本地路径为：C:\\Users\\Administrator\\Desktop\\发布一篇文章测试.md"，等待大模型返回发布结果：

![](https://raw.githubusercontent.com/Cyanty/images/main/collect/submit_gif_01.gif)

该发布工具同时支持以文本内容的方式进行发布，不过由于集成的AI客户端工具处理方式差异，大模型可能会读取文章全部内容作为上下文，比较耗费Token，耗时也较长。这里推荐使用 *以文件路径的方式* 发布文章。

以文本内容的方式发布，聊天输入示例如下：

![](https://raw.githubusercontent.com/Cyanty/images/main/collect/Snipaste_2025-07-15_11-46-32.png)

## ⚡ 发布实现

该发布工具为MCP服务提供支持，通过整合各平台发布接口和自动化技术实现高效发布：

- **统一入口**：支持从.md文件直接导入内容，适配MCP服务实现异步并行发布

- **图片处理**：自动转换外链图片为平台兼容的图片链接地址

- **发布方式**：根据不同平台特性采用API调用或浏览器自动化两种策略

目前支持的发布平台（可自定义横向扩展其他平台）

|    平台    |        发布方式         |
| :--------: | :---------------------: |
|    CSDN    |       自动化发布        |
|    掘金    |  草稿API + 自动化发布   |
|   博客园   |     Metaweblog API      |
| 微信公众号 |  MD格式美化 + 开放API   |
|    知乎    | MD格式美化 + 自动化发布 |
| Halo自建站 |      API/令牌认证       |
|   ......   |                         |

除此之外，工具还提供了一个发布操作的web页面，用户可在浏览器页面上进行操作，上传本地.md格式文件实现各平台文章的发布。

如：访问 http://127.0.0.1:8001 ，发布页面如下：

![](https://raw.githubusercontent.com/Cyanty/images/main/collect/Snipaste_2025-07-15_14-22-09.png)

## 🤝 欢迎贡献

欢迎贡献！无论是修复 bug、添加新功能还是改进文档，都可以随时提交 Pull Request 或打开一个 issue。

## 📝 License

本项目遵循 [Apache License 2.0](https://opensource.org/licenses/Apache-2.0) 协议，完整文本见 [LICENSE](LICENSE) 文件。

