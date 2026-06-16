<h1 align="center">Pixelle MCP - Omnimodal Agent Framework</h1>

<p align="center"><b>English</b> | <a href="README_CN.md">Chinese</a> | <a href="README.vi.md">Tieng Viet</a></p>

<p align="center">An AIGC solution based on the MCP protocol, supporting both local ComfyUI and cloud ComfyUI (RunningHub) modes, seamlessly converting workflows into MCP tools with zero code.</p>

![](docs/readme-1.png)

https://github.com/user-attachments/assets/65422cef-96f9-44fe-a82b-6a124674c417

---

## Table of Contents

- [Features](#features)
- [Project Architecture](#project-architecture)
- [Quick Start](#quick-start)
- [Step-by-Step Installation](#step-by-step-installation)
- [Configuration](#configuration)
- [MCP Server Setup](#mcp-server-setup)
- [CLI Usage](#cli-usage)
- [Docker Deployment](#docker-deployment)
- [Integration with CreatorHub](#integration-with-creatorhub)
- [Add Your Own MCP Tool](#add-your-own-mcp-tool)
- [ComfyUI Workflow Specification](#comfyui-workflow-specification)
- [Troubleshooting](#troubleshooting)
- [Community](#community)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [License](#license)

---

## Features

- **Full-modal Support**: Supports TISV (Text, Image, Sound/Speech, Video) full-modal conversion and generation.
- **Dual Execution Modes**: Local ComfyUI self-hosted environment + RunningHub cloud ComfyUI service, choose based on your needs.
- **ComfyUI Ecosystem**: Built on [ComfyUI](https://github.com/comfyanonymous/ComfyUI), inheriting all capabilities from the open ComfyUI ecosystem.
- **Zero-code Development**: Defines and implements the Workflow-as-MCP Tool solution, enabling zero-code development and dynamic addition of new MCP Tools.
- **MCP Server**: Based on the [MCP](https://modelcontextprotocol.io/introduction) protocol, supporting integration with any MCP client (Cursor, Claude Desktop, etc.).
- **Web Interface**: Developed based on the [Chainlit](https://github.com/Chainlit/chainlit) framework, supporting multimodal interaction.
- **One-click Deployment**: Supports PyPI installation, CLI commands, Docker and other deployment methods, ready to use out of the box.
- **Simplified Configuration**: Uses environment variable configuration scheme, simple and intuitive.
- **Multi-LLM Support**: Supports OpenAI, Ollama, Gemini, DeepSeek, Claude, Qwen, and more.

---

## Project Architecture

Pixelle MCP adopts a **unified architecture design**, integrating MCP server, web interface, and file services into one application:

- **Web Interface**: Chainlit-based chat interface supporting multimodal interaction
- **MCP Endpoint**: For external MCP clients (Cursor, Claude Desktop) to connect
- **File Service**: Handles file upload, download, and storage
- **Workflow Engine**: Supports both local ComfyUI and cloud ComfyUI (RunningHub) workflows, automatically converts workflows into MCP tools

![](docs/%20mcp_structure.png)

---

## Quick Start

### Method 1: One-click Experience (uvx)

```bash
# Requires uv installed first
# Start with one command, no system installation required
uvx pixelle@latest
```

### Method 2: Pip Install

```bash
# Requires Python 3.11
pip install -U pixelle
pixelle
```

### Method 3: From Source

```bash
git clone https://github.com/AIDC-AI/Pixelle-MCP.git
cd Pixelle-MCP
uv run pixelle
```

After startup, the **configuration wizard** guides you through execution engine selection and LLM configuration.

### Access Services

- **Web Interface**: http://localhost:9004 (default credentials: `dev` / `dev`)
- **MCP Endpoint**: http://localhost:9004/pixelle/mcp

---

## Step-by-Step Installation

### Prerequisites

| Requirement | Details |
|---|---|
| Python | >= 3.11 |
| uv (recommended) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| ComfyUI (optional) | Required only for local mode. See [ComfyUI docs](https://github.com/comfyanonymous/ComfyUI) |
| RunningHub account (optional) | Required only for cloud mode. Register at [runninghub.ai](https://www.runninghub.ai) |

### Install via uv (Recommended)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run directly without installing to system
uvx pixelle@latest

# Or clone and run from source
git clone https://github.com/AIDC-AI/Pixelle-MCP.git
cd Pixelle-MCP
uv run pixelle
```

### Install via pip

```bash
# Ensure Python 3.11 is active
python3.11 -m pip install -U pixelle

# Start the service
pixelle
```

### First-time Setup

On first startup, the configuration wizard will prompt you to:

1. **Select Execution Engine**: Choose between local ComfyUI or RunningHub cloud service
2. **Configure LLM**: Set up at least one LLM provider (API key + model list)
3. **Create Directory Structure**: The system auto-creates `data/custom_workflows/` and related directories

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and edit:

```bash
cp .env.example .env
```

#### Basic Service

| Variable | Default | Description |
|---|---|---|
| `HOST` | `localhost` | Service bind address |
| `PORT` | `9004` | Service port |
| `PUBLIC_READ_URL` | `""` | Public access URL (for non-local deployments) |

#### ComfyUI Integration (Local Mode)

| Variable | Default | Description |
|---|---|---|
| `COMFYUI_BASE_URL` | `http://localhost:8188` | ComfyUI service address |
| `COMFYUI_API_KEY` | `""` | API key (required if using API Nodes) |
| `COMFYUI_COOKIES` | `""` | Auth cookies for ComfyUI |
| `COMFYUI_EXECUTOR_TYPE` | `http` | Executor type: `http` or `websocket` |

#### RunningHub Cloud Mode

| Variable | Default | Description |
|---|---|---|
| `RUNNINGHUB_BASE_URL` | `https://www.runninghub.ai` | API base URL (use `.cn` for China) |
| `RUNNINGHUB_API_KEY` | `""` | RunningHub API key |

#### LLM Providers

| Variable | Description |
|---|---|
| `OPENAI_BASE_URL` | OpenAI API base URL |
| `OPENAI_API_KEY` | OpenAI API key ([get here](https://platform.openai.com/api-keys)) |
| `CHAINLIT_CHAT_OPENAI_MODELS` | Comma-separated model names (e.g. `gpt-4o-mini`) |
| `OLLAMA_BASE_URL` | Ollama local server URL (default: `http://localhost:11434/v1`) |
| `OLLAMA_MODELS` | Comma-separated Ollama model names |
| `GEMINI_API_KEY` | Gemini API key ([get here](https://aistudio.google.com/app/apikey)) |
| `GEMINI_MODELS` | Comma-separated Gemini model names |
| `DEEPSEEK_API_KEY` | DeepSeek API key ([get here](https://platform.deepseek.com/api_keys)) |
| `DEEPSEEK_MODELS` | Comma-separated DeepSeek model names |
| `CLAUDE_API_KEY` | Anthropic API key ([get here](https://console.anthropic.com/settings/keys)) |
| `CLAUDE_MODELS` | Comma-separated Claude model names |
| `QWEN_API_KEY` | Alibaba Cloud API key ([get here](https://bailian.console.aliyun.com/)) |
| `QWEN_MODELS` | Comma-separated Qwen model names |
| `CHAINLIT_CHAT_DEFAULT_MODEL` | Default model for conversations |

#### Other Settings

| Variable | Default | Description |
|---|---|---|
| `CHAINLIT_AUTH_SECRET` | `changeme-...` | Auth secret (change in production) |
| `CHAINLIT_AUTH_ENABLED` | `true` | Enable authentication |
| `CDN_STRATEGY` | `auto` | CDN mode: `auto`, `china`, or `global` |

---

## MCP Server Setup

### As Standalone MCP Server

The MCP endpoint is available at:

```
http://localhost:9004/pixelle/mcp
```

### Configure in Cursor

Add to your MCP client configuration (e.g. `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "pixelle": {
      "url": "http://localhost:9004/pixelle/mcp"
    }
  }
}
```

### Configure in Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pixelle": {
      "url": "http://localhost:9004/pixelle/mcp"
    }
  }
}
```

### Verify Connection

Once connected, your MCP client will discover available tools (workflows) dynamically. Each ComfyUI workflow automatically becomes an MCP tool.

---

## CLI Usage

### Commands

| Command | Description |
|---|---|
| `pixelle` | Enter interactive mode (default) |
| `pixelle start` | Start the service |
| `pixelle start -d` | Start in background daemon mode |
| `pixelle start -f` | Force start (kill conflicting processes) |
| `pixelle stop` | Stop all Pixelle processes |
| `pixelle status` | Show service status |
| `pixelle logs` | View recent logs |
| `pixelle logs -f` | Follow logs in real-time |
| `pixelle init` | Run configuration wizard |
| `pixelle edit` | Edit configuration |
| `pixelle workflow` | Show loaded workflows and MCP tools |
| `pixelle dev` | Show development/debug info |

### Common Workflows

```bash
# First-time setup
pixelle init          # Configure engine + LLM
pixelle start         # Start service

# Daily usage
pixelle start -df     # Background force start
pixelle logs -f       # Monitor logs
pixelle stop          # Stop when done

# Debugging
pixelle status        # Check everything
pixelle workflow      # Verify loaded tools
pixelle dev           # Full system info
```

---

## Docker Deployment

### Quick Start

```bash
git clone https://github.com/AIDC-AI/Pixelle-MCP.git
cd Pixelle-MCP

# Create and edit configuration
cp .env.example .env
# Edit .env with your settings

# Start
docker compose up -d

# View logs
docker compose logs -f
```

### Docker Compose Configuration

The default `docker-compose.yml` exposes port `9004`, mounts `./data` and `.env`, and includes health checks. Key points:

- The `data/` directory persists workflow files and custom configurations
- The `.env` file is mounted read-only into the container
- `host.docker.internal` is mapped to access local ComfyUI from inside the container
- Health check hits `http://localhost:9004/health`

### Useful Commands

```bash
# Stop
docker compose down

# Rebuild after code changes
docker compose build --no-cache && docker compose up -d

# View container status
docker compose ps

# Enter container shell
docker compose exec pixelle bash
```

---

## Integration with CreatorHub

Pixelle MCP can be integrated into CreatorHub (or any MCP-compatible agent system) as a tool provider:

### 1. Register as MCP Server

Ensure Pixelle is running and accessible. The MCP endpoint is:

```
http://localhost:9004/pixelle/mcp
```

### 2. Configure CreatorHub

In CreatorHub's MCP server configuration, add:

```json
{
  "pixelle": {
    "url": "http://localhost:9004/pixelle/mcp"
  }
}
```

### 3. Available Tools

Once connected, CreatorHub will have access to all MCP tools created from your ComfyUI workflows. Each workflow becomes a callable tool with typed parameters and descriptions.

### 4. Workflow

1. Design workflows in ComfyUI
2. Export as API format JSON
3. Upload to Pixelle via the web UI or paste into chat
4. LLM automatically converts workflow to MCP tool
5. CreatorHub can now invoke the tool via MCP protocol

---

## Add Your Own MCP Tool

One workflow = One MCP Tool. Two methods to add:

- **Method 1**: Local ComfyUI workflow - export API format workflow files
- **Method 2**: RunningHub workflow ID - use cloud workflow IDs directly

### Step-by-Step

1. Build a workflow in ComfyUI (e.g. image Gaussian blur)
2. Set node titles with the parameter DSL syntax (see [Workflow Specification](#comfyui-workflow-specification))
3. Export as **API format** JSON file
4. Open the Pixelle web interface and paste the workflow JSON
5. The LLM automatically converts it to an MCP tool
6. Refresh the page - the tool is now available

> **RunningHub users**: You only need to input the workflow ID, no file download/upload needed.

---

## ComfyUI Workflow Specification

### Parameter Definition Syntax

In ComfyUI, edit node titles using this DSL:

```
$<param_name>.[~]<field_name>[!][:<description>]
```

| Symbol | Meaning |
|---|---|
| `param_name` | Parameter name for the MCP tool function |
| `~` | (Optional) URL parameter upload processing, returns relative path |
| `field_name` | Corresponding input field in the node |
| `!` | Required parameter marker |
| `description` | Parameter description |

### Examples

**Required parameter:**
- Node title: `$image.image!:Input image URL`
- Creates required param `image` mapped to the node's `image` field

**URL upload processing:**
- Node title: `$image.~image!:Input image URL`
- System auto-downloads URL and uploads to ComfyUI

### Type Inference

The system infers types from current node values:
- `int` - integer values (512, 1024)
- `float` - floating-point (1.5, 3.14)
- `bool` - boolean (true, false)
- `str` - string (default)

### Output Definition

**Auto-detected nodes**: `SaveImage`, `SaveVideo`, `SaveAudio`, `VHS_SaveVideo`, `VHS_SaveAudio`

**Manual output marking** (for multiple outputs):
- Node title: `$output.result`

### Tool Description (Optional)

Add a `String (Multiline)` node titled `MCP` with your tool description in the value field.

### Important Notes

1. Optional parameters (no `!`) must have default values set in the node
2. Fields connected to other nodes will not be parsed as parameters
3. Exported filename becomes the tool name - use meaningful English names
4. Must export as **API format**, not UI format
5. Test workflows in ComfyUI first before adding to Pixelle

---

## Troubleshooting

### Service won't start

```bash
pixelle status       # Check status
pixelle start -f     # Force start
pixelle logs         # Check error logs
```

### Port already in use

```bash
# Change port in .env
PORT=9005

# Or force start to kill conflicting processes
pixelle start -f
```

### ComfyUI connection failed

1. Ensure ComfyUI is running: `curl http://localhost:8188/system_stats`
2. Check `COMFYUI_BASE_URL` in `.env`
3. For Docker, ensure `host.docker.internal` is accessible

### RunningHub connection failed

1. Verify API key at [runninghub.ai](https://www.runninghub.ai)
2. Check `RUNNINGHUB_BASE_URL` (use `.cn` for China)
3. Ensure network access to RunningHub servers

### LLM not responding

1. Verify API key is set in `.env`
2. Check `CHAINLIT_CHAT_DEFAULT_MODEL` is configured
3. Test API key independently:
   ```bash
   # OpenAI test
   curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

### Docker issues

```bash
docker compose down && docker compose build --no-cache && docker compose up -d
docker compose logs -f
```

### Reset configuration

```bash
pixelle init    # Re-run configuration wizard
```

---

## Community

| Discord | WeChat |
|:---:|:---:|
| <img src="docs/discord.png" alt="Discord" width="200" /> | <img src="docs/wechat.png" alt="WeChat" width="200" /> |

---

## Contributing

We welcome all forms of contribution!

### Report Issues
- Submit bug reports on [Issues](https://github.com/AIDC-AI/Pixelle-MCP/issues)
- Search for similar issues before submitting
- Describe reproduction steps and environment in detail

### Feature Suggestions
- Submit feature requests in [Issues](https://github.com/AIDC-AI/Pixelle-MCP/issues)
- Describe the use case and how it improves experience

### Code Contributions

1. Fork this repo
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Develop and add tests
4. Commit: `git commit -m "feat: add your feature"`
5. Push: `git push origin feature/your-feature-name`
6. Create a Pull Request

### Code Style
- Python code follows [PEP 8](https://pep8.org/)
- Add documentation and comments for new features

### Contribute Workflows
- Share your ComfyUI workflows with the community
- Submit tested workflow files with usage instructions

---

## Acknowledgements

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [Chainlit](https://github.com/Chainlit/chainlit)
- [MCP](https://modelcontextprotocol.io/introduction)
- [WanVideo](https://github.com/Wan-Video/Wan2.1)
- [Flux](https://github.com/black-forest-labs/flux)
- [LiteLLM](https://github.com/BerriAI/litellm)

## License

This project is released under the MIT License ([LICENSE](LICENSE), SPDX-License-identifier: MIT).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AIDC-AI/Pixelle-MCP&type=Date)](https://star-history.com/#AIDC-AI/Pixelle-MCP&Date)
