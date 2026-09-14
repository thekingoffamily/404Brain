# 404Brain

[English](./README.md) · [Русский](./README.ru.md) · [中文](./README.zh.md) · [Español](./README.es.md) · [Português](./README.pt.md) · [Deutsch](./README.de.md) · [Français](./README.fr.md) · [日本語](./README.ja.md) · [한국어](./README.ko.md) · [Українська](./README.uk.md)

<div align="center">
	<img
		src="./404brain-logo.png"
		alt="404Brain logo"
		width="220"
		height="220"
	/>
</div>

**404Brain** — AI-first desktop IDE, based on [VS Code](https://github.com/microsoft/vscode).

Agents on your codebase. Checkpoints and live diffs. Any model or local host. Messages go straight to your providers — your data stays yours.

## Lazy start (recommended)

**Windows:** double-click `RUN_AND_INSTALL.bat`  
(It auto-downloads portable **Node 20.18.2** into `.tools/` if your system Node is 22/23 — you can keep the new Node.)

**Mac / Linux:** `chmod +x run_and_install.sh && ./run_and_install.sh`

That script installs deps (if needed), compiles once, and opens 404Brain.  
Need Node **20.18.2**. On Windows also VS 2022 C++ build tools (see [BUILD.md](./BUILD.md)).

**Models from Russia:** built-in **AITUNNEL** provider (OpenAI-compatible, RUB, no VPN). Sign up: [aitunnel.ru/?r=52512](https://aitunnel.ru/?r=52512) · Docs: [aitunnel.ru/docs](https://aitunnel.ru/docs).

## Features

- AI agents over real project files — **Agent** mode (read + edit + terminal + MCP), **Gather** (read-only), **Normal** (plain chat)
- Checkpoints and visual diffs as code streams in, roll back per-file from chat history
- **Quick Edit (Ctrl+K)** inline edits, **Apply** code blocks, **Autocomplete** (FIM), **SCM** commit-message writer
- **SSH** and **WSL** remote development — bundled `open-remote-ssh` and `open-remote-wsl` extensions
- Bring your own models / local hosts (OpenAI-compatible, Ollama, vLLM, LM Studio, LiteLLM, and more)
- **MCP** (Model Context Protocol) — plug external tools into the agent
- Full desktop app source in this repository

## Providers

Nearly 20 providers: OpenAI, Anthropic, Google Gemini, DeepSeek, Groq, xAI, Mistral, OpenRouter, AWS Bedrock, Azure, Vertex, plus **AITUNNEL** — 200+ models, pay in RUB, no VPN.

## Links

- Repository: https://github.com/thekingoffamily/404Brain
- Releases: https://github.com/thekingoffamily/404Brain/releases
- Build (step by step): [BUILD.md](./BUILD.md)

## Contact

- Email: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)

## Credits

Built on the open-source [VS Code](https://github.com/microsoft/vscode) codebase (MIT).
