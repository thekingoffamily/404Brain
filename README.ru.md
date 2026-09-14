# 404Brain

[English](./README.md) · [Русский](./README.ru.md) · [中文](./README.zh.md) · [Español](./README.es.md) · [Português](./README.pt.md) · [Deutsch](./README.de.md) · [Français](./README.fr.md) · [日本語](./README.ja.md) · [한국어](./README.ko.md) · [Українська](./README.uk.md)

<div align="center">
	<img
		src="./404brain-logo.png"
		alt="Логотип 404Brain"
		width="220"
		height="220"
	/>
</div>

**404Brain** — AI-first десктоп IDE на базе [VS Code](https://github.com/microsoft/vscode).

Агенты по вашему коду. Чекпоинты и живые диффы. Любые модели и локальные хосты. Сообщения идут напрямую к провайдерам — ваши данные остаются у вас.

## Ленивый старт (рекомендуется)

**Windows:** двойной клик по `RUN_AND_INSTALL.bat`  
(Сам скачает portable **Node 20.18.2** в `.tools/`, если у тебя системный Node 22/23 — новый Node можно не сносить.)

**Mac / Linux:** `chmod +x run_and_install.sh && ./run_and_install.sh`

Скрипт сам поставит зависимости (если надо), соберёт и откроет 404Brain.  
Нужен Node **20.18.2**. На Windows ещё VS 2022 с C++ (см. [BUILD.ru.md](./BUILD.ru.md)).

**Модели из РФ:** встроенный провайдер **AITUNNEL** (OpenAI-совместимый, рубли, без VPN). Регистрация: [aitunnel.ru/?r=52512](https://aitunnel.ru/?r=52512) · Доки: [aitunnel.ru/docs](https://aitunnel.ru/docs).

## Возможности

- AI-агенты по реальному проекту: режимы **Agent** (полный агент: чтение + правка + терминал + MCP), **Gather** (только чтение) и **Normal** (чистый чат)
- Чекпоинты и визуальные диффы по мере стриминга кода, откат изменений по истории чата
- **Quick Edit (Ctrl+K)** — правка кода прямо в редакторе, **Apply** — применение код-блоков из чата, **Autocomplete** — FIM-автодополнение, **SCM** — генератор текста коммитов
- Работа по **SSH** и **WSL**: встроенные расширения `open-remote-ssh` и `open-remote-wsl` (Remote Development)
- Свои модели и локальные хосты (OpenAI-compatible, Ollama, vLLM, LM Studio, LiteLLM и др.)
- MCP (Model Context Protocol) — подключение внешних тулов к агенту
- Полный исходник десктоп-приложения в этом репозитории

## Провайдеры

Почти 20 провайдеров: OpenAI, Anthropic, Google Gemini, DeepSeek, Groq, xAI, Mistral, OpenRouter, AWS Bedrock, Azure, Vertex, а также **AITUNNEL** — агрегатор 200+ моделей с оплатой в рублях и без VPN.

## Ссылки

- Репозиторий: https://github.com/thekingoffamily/404Brain
- Релизы: https://github.com/thekingoffamily/404Brain/releases
- Сборка по шагам: [BUILD.ru.md](./BUILD.ru.md)

## Связь

- Почта: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)

## Благодарности

Основано на открытом коде [VS Code](https://github.com/microsoft/vscode) (MIT).
