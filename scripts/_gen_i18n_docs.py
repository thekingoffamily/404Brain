# -*- coding: utf-8 -*-
"""Generate README + BUILD for 10 languages."""
from pathlib import Path

ROOT = Path(r"c:\Users\palapalaru\Desktop\404Brain")

LANGS = [
    ("en", "English", "README.md", "BUILD.md"),
    ("ru", "Русский", "README.ru.md", "BUILD.ru.md"),
    ("zh", "中文", "README.zh.md", "BUILD.zh.md"),
    ("es", "Español", "README.es.md", "BUILD.es.md"),
    ("pt", "Português", "README.pt.md", "BUILD.pt.md"),
    ("de", "Deutsch", "README.de.md", "BUILD.de.md"),
    ("fr", "Français", "README.fr.md", "BUILD.fr.md"),
    ("ja", "日本語", "README.ja.md", "BUILD.ja.md"),
    ("ko", "한국어", "README.ko.md", "BUILD.ko.md"),
    ("uk", "Українська", "README.uk.md", "BUILD.uk.md"),
]


def lang_bar(kind: str) -> str:
    # kind: readme | build
    parts = []
    for code, label, readme, build in LANGS:
        target = readme if kind == "readme" else build
        parts.append(f"[{label}](./{target})")
    return " · ".join(parts)


# README translations: tagline, intro, features_h, features[], links_h, repo, releases, build_label, contact_h, email, telegram, credits_h, credits
README = {
    "en": {
        "alt": "404Brain logo",
        "tagline": "**404Brain** — AI-first desktop IDE, based on [VS Code](https://github.com/microsoft/vscode).",
        "intro": "Agents on your codebase. Checkpoints and live diffs. Any model or local host. Messages go straight to your providers — your data stays yours.",
        "features_h": "Features",
        "features": [
            "AI agents over real project files",
            "Checkpoints and visual diffs as code streams in",
            "Bring your own models / local hosts (OpenAI-compatible, Ollama, and more)",
            "Full desktop app source in this repository",
        ],
        "links_h": "Links",
        "repo": "Repository",
        "releases": "Releases",
        "build": "Build (step by step)",
        "contact_h": "Contact",
        "email": "Email",
        "telegram": "Telegram",
        "credits_h": "Credits",
        "credits": "Built on the open-source [VS Code](https://github.com/microsoft/vscode) codebase (MIT).",
    },
    "ru": {
        "alt": "Логотип 404Brain",
        "tagline": "**404Brain** — AI-first десктоп IDE на базе [VS Code](https://github.com/microsoft/vscode).",
        "intro": "Агенты по вашему коду. Чекпоинты и живые диффы. Любые модели и локальные хосты. Сообщения идут напрямую к провайдерам — ваши данные остаются у вас.",
        "features_h": "Возможности",
        "features": [
            "AI-агенты по реальному проекту",
            "Чекпоинты и визуальные диффы по мере стриминга кода",
            "Свои модели и локальные хосты (OpenAI-compatible, Ollama и др.)",
            "Полный исходник десктоп-приложения в этом репозитории",
        ],
        "links_h": "Ссылки",
        "repo": "Репозиторий",
        "releases": "Релизы",
        "build": "Сборка по шагам",
        "contact_h": "Связь",
        "email": "Почта",
        "telegram": "Telegram",
        "credits_h": "Благодарности",
        "credits": "Основано на открытом коде [VS Code](https://github.com/microsoft/vscode) (MIT).",
    },
    "zh": {
        "alt": "404Brain 标志",
        "tagline": "**404Brain** — 面向 AI 的桌面 IDE，基于 [VS Code](https://github.com/microsoft/vscode)。",
        "intro": "在真实代码库上使用 AI 代理。检查点与实时 diff。任意模型或本地主机。消息直达你的提供商——数据留在你这边。",
        "features_h": "功能",
        "features": [
            "基于真实项目文件的 AI 代理",
            "流式生成代码时的检查点与可视化 diff",
            "自带模型 / 本地主机（OpenAI 兼容、Ollama 等）",
            "本仓库包含完整桌面应用源码",
        ],
        "links_h": "链接",
        "repo": "仓库",
        "releases": "发布",
        "build": "分步构建",
        "contact_h": "联系",
        "email": "邮箱",
        "telegram": "Telegram",
        "credits_h": "致谢",
        "credits": "基于开源 [VS Code](https://github.com/microsoft/vscode)（MIT）。",
    },
    "es": {
        "alt": "Logo de 404Brain",
        "tagline": "**404Brain** — IDE de escritorio centrado en IA, basado en [VS Code](https://github.com/microsoft/vscode).",
        "intro": "Agentes sobre tu código. Checkpoints y diffs en vivo. Cualquier modelo o host local. Los mensajes van directo a tus proveedores: tus datos se quedan contigo.",
        "features_h": "Funciones",
        "features": [
            "Agentes de IA sobre archivos reales del proyecto",
            "Checkpoints y diffs visuales mientras llega el código",
            "Tus propios modelos / hosts locales (compatibles con OpenAI, Ollama y más)",
            "Código fuente completo de la app de escritorio en este repositorio",
        ],
        "links_h": "Enlaces",
        "repo": "Repositorio",
        "releases": "Releases",
        "build": "Compilación paso a paso",
        "contact_h": "Contacto",
        "email": "Email",
        "telegram": "Telegram",
        "credits_h": "Créditos",
        "credits": "Basado en el código abierto de [VS Code](https://github.com/microsoft/vscode) (MIT).",
    },
    "pt": {
        "alt": "Logo do 404Brain",
        "tagline": "**404Brain** — IDE desktop focada em IA, baseada no [VS Code](https://github.com/microsoft/vscode).",
        "intro": "Agentes no seu código. Checkpoints e diffs ao vivo. Qualquer modelo ou host local. As mensagens vão direto aos provedores — seus dados ficam com você.",
        "features_h": "Recursos",
        "features": [
            "Agentes de IA sobre arquivos reais do projeto",
            "Checkpoints e diffs visuais conforme o código chega",
            "Seus próprios modelos / hosts locais (compatíveis com OpenAI, Ollama e mais)",
            "Código-fonte completo do app desktop neste repositório",
        ],
        "links_h": "Links",
        "repo": "Repositório",
        "releases": "Releases",
        "build": "Build passo a passo",
        "contact_h": "Contato",
        "email": "Email",
        "telegram": "Telegram",
        "credits_h": "Créditos",
        "credits": "Baseado no código aberto do [VS Code](https://github.com/microsoft/vscode) (MIT).",
    },
    "de": {
        "alt": "404Brain-Logo",
        "tagline": "**404Brain** — KI-first Desktop-IDE, basierend auf [VS Code](https://github.com/microsoft/vscode).",
        "intro": "Agenten in deiner Codebase. Checkpoints und Live-Diffs. Beliebige Modelle oder lokale Hosts. Nachrichten gehen direkt an deine Provider — deine Daten bleiben bei dir.",
        "features_h": "Funktionen",
        "features": [
            "KI-Agenten über echte Projektdateien",
            "Checkpoints und visuelle Diffs während der Code streamt",
            "Eigene Modelle / lokale Hosts (OpenAI-kompatibel, Ollama und mehr)",
            "Vollständiger Desktop-App-Quellcode in diesem Repository",
        ],
        "links_h": "Links",
        "repo": "Repository",
        "releases": "Releases",
        "build": "Build Schritt für Schritt",
        "contact_h": "Kontakt",
        "email": "E-Mail",
        "telegram": "Telegram",
        "credits_h": "Danksagung",
        "credits": "Basierend auf dem Open-Source-Code von [VS Code](https://github.com/microsoft/vscode) (MIT).",
    },
    "fr": {
        "alt": "Logo 404Brain",
        "tagline": "**404Brain** — IDE bureau axé IA, basé sur [VS Code](https://github.com/microsoft/vscode).",
        "intro": "Des agents sur votre code. Points de contrôle et diffs en direct. N’importe quel modèle ou hôte local. Les messages vont directement chez vos fournisseurs — vos données restent les vôtres.",
        "features_h": "Fonctionnalités",
        "features": [
            "Agents IA sur les vrais fichiers du projet",
            "Points de contrôle et diffs visuels pendant le streaming du code",
            "Vos propres modèles / hôtes locaux (compatibles OpenAI, Ollama, etc.)",
            "Code source complet de l’app bureau dans ce dépôt",
        ],
        "links_h": "Liens",
        "repo": "Dépôt",
        "releases": "Releases",
        "build": "Build pas à pas",
        "contact_h": "Contact",
        "email": "E-mail",
        "telegram": "Telegram",
        "credits_h": "Crédits",
        "credits": "Basé sur le code open source de [VS Code](https://github.com/microsoft/vscode) (MIT).",
    },
    "ja": {
        "alt": "404Brain ロゴ",
        "tagline": "**404Brain** — [VS Code](https://github.com/microsoft/vscode) ベースの AI ファーストなデスクトップ IDE。",
        "intro": "コードベース上の AI エージェント。チェックポイントとライブ diff。任意のモデルやローカルホスト。メッセージはプロバイダーへ直接 — データはあなたのもとに。",
        "features_h": "機能",
        "features": [
            "実プロジェクトファイル上の AI エージェント",
            "コードストリーム中のチェックポイントと視覚的 diff",
            "自分のモデル / ローカルホスト（OpenAI 互換、Ollama など）",
            "このリポジトリにデスクトップアプリの全ソース",
        ],
        "links_h": "リンク",
        "repo": "リポジトリ",
        "releases": "リリース",
        "build": "ビルド手順",
        "contact_h": "連絡先",
        "email": "メール",
        "telegram": "Telegram",
        "credits_h": "クレジット",
        "credits": "オープンソースの [VS Code](https://github.com/microsoft/vscode)（MIT）をベースにしています。",
    },
    "ko": {
        "alt": "404Brain 로고",
        "tagline": "**404Brain** — [VS Code](https://github.com/microsoft/vscode) 기반 AI 우선 데스크톱 IDE.",
        "intro": "코드베이스 위 AI 에이전트. 체크포인트와 실시간 diff. 어떤 모델이나 로컬 호스트든. 메시지는 제공자에게 바로 — 데이터는 당신 것.",
        "features_h": "기능",
        "features": [
            "실제 프로젝트 파일 위 AI 에이전트",
            "코드 스트리밍 중 체크포인트와 시각적 diff",
            "자체 모델 / 로컬 호스트 (OpenAI 호환, Ollama 등)",
            "이 저장소에 데스크톱 앱 전체 소스",
        ],
        "links_h": "링크",
        "repo": "저장소",
        "releases": "릴리스",
        "build": "단계별 빌드",
        "contact_h": "연락처",
        "email": "이메일",
        "telegram": "Telegram",
        "credits_h": "크레딧",
        "credits": "오픈소스 [VS Code](https://github.com/microsoft/vscode) (MIT) 기반.",
    },
    "uk": {
        "alt": "Логотип 404Brain",
        "tagline": "**404Brain** — AI-first десктоп IDE на базі [VS Code](https://github.com/microsoft/vscode).",
        "intro": "Агенти над вашим кодом. Чекпоінти та живі дифи. Будь-які моделі чи локальні хости. Повідомлення йдуть просто до провайдерів — ваші дані лишаються з вами.",
        "features_h": "Можливості",
        "features": [
            "AI-агенти над реальними файлами проєкту",
            "Чекпоінти та візуальні дифи під час стрімінгу коду",
            "Власні моделі / локальні хости (OpenAI-compatible, Ollama тощо)",
            "Повний вихідний код десктоп-застосунку в цьому репозиторії",
        ],
        "links_h": "Посилання",
        "repo": "Репозиторій",
        "releases": "Релізи",
        "build": "Збірка крок за кроком",
        "contact_h": "Зв’язок",
        "email": "Пошта",
        "telegram": "Telegram",
        "credits_h": "Подяки",
        "credits": "На основі відкритого коду [VS Code](https://github.com/microsoft/vscode) (MIT).",
    },
}

# BUILD translations - keep code blocks identical; translate prose
BUILD = {
    "en": {
        "title": "# Build 404Brain (local)",
        "node_note": "Node **20.18.2** (see `.nvmrc`). Path to the repo must **not** contain spaces.",
        "s0": "## 0. Prerequisites (once)",
        "win": "### Windows",
        "win_steps": [
            "1. Install [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (or Build Tools).",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. Install.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (usually already there).",
        "linux": "### Linux",
        "linux_then": "Then (Debian/Ubuntu):",
        "s1": "## 1. Clone + install",
        "node_ver": "Node version:",
        "or_node": "(or install Node `20.18.2` another way)",
        "s2": "## 2. Build (watch)",
        "opt_a": "**Option A — from terminal**",
        "wait": "Wait until you see both lines roughly like:",
        "opt_b": "**Option B — from VS Code / Cursor**",
        "opt_b_note": "Press `Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) and wait until the build tasks finish (~5 min first time).",
        "s3": "## 3. Run Developer Mode",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "A 404Brain window opens. After code changes: `Ctrl+R` / `Cmd+R` (or Command Palette → **Reload Window**).",
        "reset": "To reset local IDE state: delete the `.tmp` folder.",
        "s4": "## 4. React UI (if you change React under `contrib/brain`)",
        "oom": "If it OOMs:",
        "fixes_h": "## Common fixes",
        "table_h": "| Problem | Fix |\n|--------|-----|\n| Wrong Node | Use `20.18.2` from `.nvmrc` |\n| Path with spaces | Move the repo |\n| React / OOM | `buildreact` with `NODE_OPTIONS=8192` as above |\n| Linux sandbox error | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## Contact",
        "email": "Email",
        "telegram": "Telegram",
    },
    "ru": {
        "title": "# Сборка 404Brain (локально)",
        "node_note": "Node **20.18.2** (см. `.nvmrc`). В пути к репо **не должно быть пробелов**.",
        "s0": "## 0. Один раз — зависимости",
        "win": "### Windows",
        "win_steps": [
            "1. Поставь [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (или Build Tools).",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. Install.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (обычно уже есть).",
        "linux": "### Linux",
        "linux_then": "Debian/Ubuntu:",
        "s1": "## 1. Клон + install",
        "node_ver": "Версия Node:",
        "or_node": "(или поставь Node `20.18.2` иначе)",
        "s2": "## 2. Сборка (watch)",
        "opt_a": "**Вариант A — терминал**",
        "wait": "Жди примерно такие строки:",
        "opt_b": "**Вариант B — из VS Code / Cursor**",
        "opt_b_note": "`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`), жди окончания задач (~5 мин в первый раз).",
        "s3": "## 3. Developer Mode",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "Откроется окно 404Brain. После правок кода: `Ctrl+R` / `Cmd+R` (или Command Palette → **Reload Window**).",
        "reset": "Сброс локального состояния IDE: удали папку `.tmp`.",
        "s4": "## 4. React UI (если трогал React в `contrib/brain`)",
        "oom": "Если не хватает памяти:",
        "fixes_h": "## Частые фиксы",
        "table_h": "| Проблема | Что сделать |\n|--------|-------------|\n| Не тот Node | `20.18.2` из `.nvmrc` |\n| Пробелы в пути | Перенеси репо |\n| React / OOM | `buildreact` с `NODE_OPTIONS=8192` |\n| Linux sandbox | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## Связь",
        "email": "Почта",
        "telegram": "Telegram",
    },
    "zh": {
        "title": "# 构建 404Brain（本地）",
        "node_note": "Node **20.18.2**（见 `.nvmrc`）。仓库路径中**不能有空格**。",
        "s0": "## 0. 一次性依赖",
        "win": "### Windows",
        "win_steps": [
            "1. 安装 [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community)（或 Build Tools）。",
            "2. Workloads：**Desktop development with C++**、**Node.js build tools**。",
            "3. Individual components：",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. 安装。",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode（通常已有）。",
        "linux": "### Linux",
        "linux_then": "然后（Debian/Ubuntu）：",
        "s1": "## 1. 克隆 + install",
        "node_ver": "Node 版本：",
        "or_node": "（或以其他方式安装 Node `20.18.2`）",
        "s2": "## 2. 构建（watch）",
        "opt_a": "**方式 A — 终端**",
        "wait": "等到大致出现如下两行：",
        "opt_b": "**方式 B — 在 VS Code / Cursor 中**",
        "opt_b_note": "按 `Ctrl+Shift+B`（Mac：`Cmd+Shift+B`），等待构建任务完成（首次约 5 分钟）。",
        "s3": "## 3. 运行开发模式",
        "win_h": "**Windows：**",
        "maclinux_h": "**Mac / Linux：**",
        "opens": "会打开 404Brain 窗口。改代码后：`Ctrl+R` / `Cmd+R`（或命令面板 → **Reload Window**）。",
        "reset": "重置本地 IDE 状态：删除 `.tmp` 文件夹。",
        "s4": "## 4. React UI（若修改了 `contrib/brain` 下的 React）",
        "oom": "若内存不足（OOM）：",
        "fixes_h": "## 常见问题",
        "table_h": "| 问题 | 处理 |\n|--------|-----|\n| Node 版本不对 | 使用 `.nvmrc` 中的 `20.18.2` |\n| 路径含空格 | 移动仓库 |\n| React / OOM | 如上使用 `NODE_OPTIONS=8192` 运行 `buildreact` |\n| Linux sandbox 错误 | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## 联系",
        "email": "邮箱",
        "telegram": "Telegram",
    },
    "es": {
        "title": "# Compilar 404Brain (local)",
        "node_note": "Node **20.18.2** (ver `.nvmrc`). La ruta del repo **no** debe tener espacios.",
        "s0": "## 0. Prerrequisitos (una vez)",
        "win": "### Windows",
        "win_steps": [
            "1. Instala [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (o Build Tools).",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. Instalar.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (suele estar ya).",
        "linux": "### Linux",
        "linux_then": "Luego (Debian/Ubuntu):",
        "s1": "## 1. Clonar + install",
        "node_ver": "Versión de Node:",
        "or_node": "(o instala Node `20.18.2` de otra forma)",
        "s2": "## 2. Build (watch)",
        "opt_a": "**Opción A — terminal**",
        "wait": "Espera hasta ver algo como:",
        "opt_b": "**Opción B — desde VS Code / Cursor**",
        "opt_b_note": "Pulsa `Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) y espera a que terminen las tareas (~5 min la primera vez).",
        "s3": "## 3. Modo desarrollador",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "Se abre una ventana de 404Brain. Tras cambios: `Ctrl+R` / `Cmd+R` (o Command Palette → **Reload Window**).",
        "reset": "Para resetear el estado local: borra la carpeta `.tmp`.",
        "s4": "## 4. UI React (si cambias React en `contrib/brain`)",
        "oom": "Si se queda sin memoria (OOM):",
        "fixes_h": "## Arreglos comunes",
        "table_h": "| Problema | Solución |\n|--------|-----|\n| Node incorrecto | Usa `20.18.2` de `.nvmrc` |\n| Espacios en la ruta | Mueve el repo |\n| React / OOM | `buildreact` con `NODE_OPTIONS=8192` |\n| Error sandbox Linux | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## Contacto",
        "email": "Email",
        "telegram": "Telegram",
    },
    "pt": {
        "title": "# Build 404Brain (local)",
        "node_note": "Node **20.18.2** (veja `.nvmrc`). O caminho do repo **não** pode ter espaços.",
        "s0": "## 0. Pré-requisitos (uma vez)",
        "win": "### Windows",
        "win_steps": [
            "1. Instale [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (ou Build Tools).",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. Instalar.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (geralmente já existe).",
        "linux": "### Linux",
        "linux_then": "Depois (Debian/Ubuntu):",
        "s1": "## 1. Clone + install",
        "node_ver": "Versão do Node:",
        "or_node": "(ou instale Node `20.18.2` de outro jeito)",
        "s2": "## 2. Build (watch)",
        "opt_a": "**Opção A — terminal**",
        "wait": "Espere ver linhas parecidas com:",
        "opt_b": "**Opção B — no VS Code / Cursor**",
        "opt_b_note": "Pressione `Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) e aguarde as tasks (~5 min na primeira vez).",
        "s3": "## 3. Modo desenvolvedor",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "Abre uma janela 404Brain. Após mudanças: `Ctrl+R` / `Cmd+R` (ou Command Palette → **Reload Window**).",
        "reset": "Para resetar o estado local: apague a pasta `.tmp`.",
        "s4": "## 4. UI React (se alterar React em `contrib/brain`)",
        "oom": "Se der OOM:",
        "fixes_h": "## Correções comuns",
        "table_h": "| Problema | Correção |\n|--------|-----|\n| Node errado | Use `20.18.2` do `.nvmrc` |\n| Espaços no caminho | Mova o repo |\n| React / OOM | `buildreact` com `NODE_OPTIONS=8192` |\n| Erro sandbox Linux | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## Contato",
        "email": "Email",
        "telegram": "Telegram",
    },
    "de": {
        "title": "# 404Brain bauen (lokal)",
        "node_note": "Node **20.18.2** (siehe `.nvmrc`). Der Repo-Pfad darf **keine** Leerzeichen enthalten.",
        "s0": "## 0. Voraussetzungen (einmalig)",
        "win": "### Windows",
        "win_steps": [
            "1. Installiere [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (oder Build Tools).",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. Installieren.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (meist schon da).",
        "linux": "### Linux",
        "linux_then": "Dann (Debian/Ubuntu):",
        "s1": "## 1. Klonen + install",
        "node_ver": "Node-Version:",
        "or_node": "(oder Node `20.18.2` anders installieren)",
        "s2": "## 2. Build (watch)",
        "opt_a": "**Option A — Terminal**",
        "wait": "Warte, bis du ungefähr siehst:",
        "opt_b": "**Option B — in VS Code / Cursor**",
        "opt_b_note": "`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) drücken und warten (~5 Min beim ersten Mal).",
        "s3": "## 3. Developer Mode",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "Ein 404Brain-Fenster öffnet sich. Nach Code-Änderungen: `Ctrl+R` / `Cmd+R` (oder Command Palette → **Reload Window**).",
        "reset": "Lokalen IDE-Zustand zurücksetzen: Ordner `.tmp` löschen.",
        "s4": "## 4. React-UI (bei Änderungen unter `contrib/brain`)",
        "oom": "Bei OOM:",
        "fixes_h": "## Häufige Fixes",
        "table_h": "| Problem | Fix |\n|--------|-----|\n| Falsche Node-Version | `20.18.2` aus `.nvmrc` |\n| Leerzeichen im Pfad | Repo verschieben |\n| React / OOM | `buildreact` mit `NODE_OPTIONS=8192` |\n| Linux-Sandbox-Fehler | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## Kontakt",
        "email": "E-Mail",
        "telegram": "Telegram",
    },
    "fr": {
        "title": "# Builder 404Brain (local)",
        "node_note": "Node **20.18.2** (voir `.nvmrc`). Le chemin du dépôt ne doit **pas** contenir d’espaces.",
        "s0": "## 0. Prérequis (une fois)",
        "win": "### Windows",
        "win_steps": [
            "1. Installez [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (ou Build Tools).",
            "2. Workloads : **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components :",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. Installer.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (souvent déjà là).",
        "linux": "### Linux",
        "linux_then": "Puis (Debian/Ubuntu) :",
        "s1": "## 1. Cloner + install",
        "node_ver": "Version de Node :",
        "or_node": "(ou installez Node `20.18.2` autrement)",
        "s2": "## 2. Build (watch)",
        "opt_a": "**Option A — terminal**",
        "wait": "Attendez des lignes du genre :",
        "opt_b": "**Option B — depuis VS Code / Cursor**",
        "opt_b_note": "Appuyez sur `Ctrl+Shift+B` (Mac : `Cmd+Shift+B`) et attendez la fin (~5 min la première fois).",
        "s3": "## 3. Mode développeur",
        "win_h": "**Windows :**",
        "maclinux_h": "**Mac / Linux :**",
        "opens": "Une fenêtre 404Brain s’ouvre. Après des changements : `Ctrl+R` / `Cmd+R` (ou Command Palette → **Reload Window**).",
        "reset": "Pour réinitialiser l’état local : supprimez le dossier `.tmp`.",
        "s4": "## 4. UI React (si vous modifiez React sous `contrib/brain`)",
        "oom": "En cas d’OOM :",
        "fixes_h": "## Correctifs courants",
        "table_h": "| Problème | Correctif |\n|--------|-----|\n| Mauvais Node | Utilisez `20.18.2` de `.nvmrc` |\n| Espaces dans le chemin | Déplacez le dépôt |\n| React / OOM | `buildreact` avec `NODE_OPTIONS=8192` |\n| Erreur sandbox Linux | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## Contact",
        "email": "E-mail",
        "telegram": "Telegram",
    },
    "ja": {
        "title": "# 404Brain のビルド（ローカル）",
        "node_note": "Node **20.18.2**（`.nvmrc` 参照）。リポジトリパスに**スペースを含めない**こと。",
        "s0": "## 0. 事前準備（一度だけ）",
        "win": "### Windows",
        "win_steps": [
            "1. [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community)（または Build Tools）をインストール。",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**。",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. インストール。",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode（通常は既にある）。",
        "linux": "### Linux",
        "linux_then": "その後（Debian/Ubuntu）:",
        "s1": "## 1. クローン + install",
        "node_ver": "Node バージョン:",
        "or_node": "（または別の方法で Node `20.18.2` を入れる）",
        "s2": "## 2. ビルド（watch）",
        "opt_a": "**方法 A — ターミナル**",
        "wait": "次のような行が出るまで待つ:",
        "opt_b": "**方法 B — VS Code / Cursor から**",
        "opt_b_note": "`Ctrl+Shift+B`（Mac: `Cmd+Shift+B`）を押し、タスク完了まで待つ（初回は約 5 分）。",
        "s3": "## 3. 開発モードで起動",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "404Brain のウィンドウが開きます。コード変更後: `Ctrl+R` / `Cmd+R`（または Command Palette → **Reload Window**）。",
        "reset": "ローカル IDE 状態のリセット: `.tmp` フォルダを削除。",
        "s4": "## 4. React UI（`contrib/brain` 配下の React を変えた場合）",
        "oom": "メモリ不足（OOM）の場合:",
        "fixes_h": "## よくある修正",
        "table_h": "| 問題 | 対処 |\n|--------|-----|\n| Node が違う | `.nvmrc` の `20.18.2` を使う |\n| パスにスペース | リポジトリを移す |\n| React / OOM | 上記どおり `NODE_OPTIONS=8192` で `buildreact` |\n| Linux sandbox エラー | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## 連絡先",
        "email": "メール",
        "telegram": "Telegram",
    },
    "ko": {
        "title": "# 404Brain 빌드 (로컬)",
        "node_note": "Node **20.18.2** (`.nvmrc` 참고). 저장소 경로에 **공백이 있으면 안 됩니다**.",
        "s0": "## 0. 사전 준비 (한 번)",
        "win": "### Windows",
        "win_steps": [
            "1. [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (또는 Build Tools) 설치.",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. 설치.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (보통 이미 있음).",
        "linux": "### Linux",
        "linux_then": "그다음 (Debian/Ubuntu):",
        "s1": "## 1. 클론 + install",
        "node_ver": "Node 버전:",
        "or_node": "(또는 다른 방식으로 Node `20.18.2` 설치)",
        "s2": "## 2. 빌드 (watch)",
        "opt_a": "**옵션 A — 터미널**",
        "wait": "대략 이런 줄이 나올 때까지 대기:",
        "opt_b": "**옵션 B — VS Code / Cursor**",
        "opt_b_note": "`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) 후 작업 완료까지 대기 (처음엔 약 5분).",
        "s3": "## 3. 개발 모드 실행",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "404Brain 창이 열립니다. 코드 변경 후: `Ctrl+R` / `Cmd+R` (또는 Command Palette → **Reload Window**).",
        "reset": "로컬 IDE 상태 초기화: `.tmp` 폴더 삭제.",
        "s4": "## 4. React UI (`contrib/brain` React를 바꾼 경우)",
        "oom": "메모리 부족(OOM)이면:",
        "fixes_h": "## 자주 쓰는 해결",
        "table_h": "| 문제 | 해결 |\n|--------|-----|\n| Node 버전이 다름 | `.nvmrc`의 `20.18.2` 사용 |\n| 경로에 공백 | 저장소 이동 |\n| React / OOM | 위처럼 `NODE_OPTIONS=8192`로 `buildreact` |\n| Linux sandbox 오류 | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## 연락처",
        "email": "이메일",
        "telegram": "Telegram",
    },
    "uk": {
        "title": "# Збірка 404Brain (локально)",
        "node_note": "Node **20.18.2** (див. `.nvmrc`). У шляху до репо **не має бути пробілів**.",
        "s0": "## 0. Один раз — залежності",
        "win": "### Windows",
        "win_steps": [
            "1. Встановіть [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (або Build Tools).",
            "2. Workloads: **Desktop development with C++**, **Node.js build tools**.",
            "3. Individual components:",
            "   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`",
            "   - `C++ ATL for latest build tools with Spectre Mitigations`",
            "   - `C++ MFC for latest build tools with Spectre Mitigations`",
            "4. Install.",
        ],
        "mac": "### Mac",
        "mac_note": "Python + Xcode (зазвичай уже є).",
        "linux": "### Linux",
        "linux_then": "Далі (Debian/Ubuntu):",
        "s1": "## 1. Клон + install",
        "node_ver": "Версія Node:",
        "or_node": "(або поставте Node `20.18.2` інакше)",
        "s2": "## 2. Збірка (watch)",
        "opt_a": "**Варіант A — термінал**",
        "wait": "Чекайте приблизно такі рядки:",
        "opt_b": "**Варіант B — з VS Code / Cursor**",
        "opt_b_note": "`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`), чекайте завершення (~5 хв уперше).",
        "s3": "## 3. Developer Mode",
        "win_h": "**Windows:**",
        "maclinux_h": "**Mac / Linux:**",
        "opens": "Відкриється вікно 404Brain. Після змін коду: `Ctrl+R` / `Cmd+R` (або Command Palette → **Reload Window**).",
        "reset": "Скинути локальний стан IDE: видаліть папку `.tmp`.",
        "s4": "## 4. React UI (якщо змінювали React у `contrib/brain`)",
        "oom": "Якщо не вистачає пам’яті (OOM):",
        "fixes_h": "## Часті фікси",
        "table_h": "| Проблема | Що зробити |\n|--------|-------------|\n| Не той Node | `20.18.2` з `.nvmrc` |\n| Пробіли в шляху | Перенесіть репо |\n| React / OOM | `buildreact` з `NODE_OPTIONS=8192` |\n| Linux sandbox | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |",
        "contact_h": "## Зв’язок",
        "email": "Пошта",
        "telegram": "Telegram",
    },
}


def write_readme(code: str, filename: str):
    r = README[code]
    build_file = next(b for c, _, _, b in LANGS if c == code)
    feats = "\n".join(f"- {x}" for x in r["features"])
    text = f"""# 404Brain

{lang_bar("readme")}

<div align="center">
	<img
		src="./404brain-logo.png"
		alt="{r["alt"]}"
		width="220"
		height="220"
	/>
</div>

{r["tagline"]}

{r["intro"]}

## {r["features_h"]}

{feats}

## {r["links_h"]}

- {r["repo"]}: https://github.com/thekingoffamily/404Brain
- {r["releases"]}: https://github.com/thekingoffamily/404Brain/releases
- {r["build"]}: [{build_file}](./{build_file})

## {r["contact_h"]}

- {r["email"]}: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- {r["telegram"]}: [@palapalaru](https://t.me/palapalaru)

## {r["credits_h"]}

{r["credits"]}
"""
    (ROOT / filename).write_text(text, encoding="utf-8", newline="\n")
    print("wrote", filename)


def write_build(code: str, filename: str):
    b = BUILD[code]
    win = "\n".join(b["win_steps"])
    text = f"""{b["title"]}

{lang_bar("build")}

{b["node_note"]}

---

{b["s0"]}

{b["win"]}

{win}

{b["mac"]}

{b["mac_note"]}

{b["linux"]}

```bash
npm install -g node-gyp
```

{b["linux_then"]}

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

{b["s1"]}

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

{b["node_ver"]}

```bash
nvm install
nvm use
```

{b["or_node"]}

```bash
npm install
```

---

{b["s2"]}

{b["opt_a"]}

```bash
npm run watch
```

{b["wait"]}

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

{b["opt_b"]}

{b["opt_b_note"]}

---

{b["s3"]}

{b["win_h"]}

```bat
.\\scripts\\code.bat --user-data-dir .\\.tmp\\user-data --extensions-dir .\\.tmp\\extensions
```

{b["maclinux_h"]}

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

{b["opens"]}

{b["reset"]}

---

{b["s4"]}

```bash
npm run buildreact
```

{b["oom"]}

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

{b["fixes_h"]}

{b["table_h"]}

---

{b["contact_h"]}

- {b["email"]}: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- {b["telegram"]}: [@palapalaru](https://t.me/palapalaru)
"""
    (ROOT / filename).write_text(text, encoding="utf-8", newline="\n")
    print("wrote", filename)


def main():
    for code, _label, readme, build in LANGS:
        write_readme(code, readme)
        write_build(code, build)
    print("done", len(LANGS), "languages")


if __name__ == "__main__":
    main()
