# Сборка 404Brain (локально)

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

## Ленивый старт

**Windows:** двойной клик по `RUN_AND_INSTALL.bat`  
**Mac / Linux:** `chmod +x run_and_install.sh && ./run_and_install.sh`

Дальше этот гайд — только если что-то сломалось.

---

Node **20.18.2** (см. `.nvmrc`). В пути к репо **не должно быть пробелов**.

---

## 0. Один раз — зависимости

### Windows

1. Поставь [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (или Build Tools).
2. Workloads: **Desktop development with C++**, **Node.js build tools**.
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. Install.

### Mac

Python + Xcode (обычно уже есть).

### Linux

```bash
npm install -g node-gyp
```

Debian/Ubuntu:

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. Клон + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Версия Node:

```bash
nvm install
nvm use
```

(или поставь Node `20.18.2` иначе)

```bash
npm install
```

---

## 2. Сборка (watch)

**Вариант A — терминал**

```bash
npm run watch
```

Жди примерно такие строки:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**Вариант B — из VS Code / Cursor**

`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`), жди окончания задач (~5 мин в первый раз).

---

## 3. Developer Mode

**Windows:**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux:**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

Откроется окно 404Brain. После правок кода: `Ctrl+R` / `Cmd+R` (или Command Palette → **Reload Window**).

Сброс локального состояния IDE: удали папку `.tmp`.

---

## 4. React UI (если трогал React в `contrib/brain`)

```bash
npm run buildreact
```

Если не хватает памяти:

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## Частые фиксы

| Проблема | Что сделать |
|--------|-------------|
| Не тот Node | `20.18.2` из `.nvmrc` |
| Пробелы в пути | Перенеси репо |
| React / OOM | `buildreact` с `NODE_OPTIONS=8192` |
| Linux sandbox | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## Связь

- Почта: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
