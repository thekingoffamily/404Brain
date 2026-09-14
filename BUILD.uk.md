# Збірка 404Brain (локально)

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2** (див. `.nvmrc`). У шляху до репо **не має бути пробілів**.

---

## 0. Один раз — залежності

### Windows

1. Встановіть [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (або Build Tools).
2. Workloads: **Desktop development with C++**, **Node.js build tools**.
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. Install.

### Mac

Python + Xcode (зазвичай уже є).

### Linux

```bash
npm install -g node-gyp
```

Далі (Debian/Ubuntu):

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. Клон + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Версія Node:

```bash
nvm install
nvm use
```

(або поставте Node `20.18.2` інакше)

```bash
npm install
```

---

## 2. Збірка (watch)

**Варіант A — термінал**

```bash
npm run watch
```

Чекайте приблизно такі рядки:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**Варіант B — з VS Code / Cursor**

`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`), чекайте завершення (~5 хв уперше).

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

Відкриється вікно 404Brain. Після змін коду: `Ctrl+R` / `Cmd+R` (або Command Palette → **Reload Window**).

Скинути локальний стан IDE: видаліть папку `.tmp`.

---

## 4. React UI (якщо змінювали React у `contrib/brain`)

```bash
npm run buildreact
```

Якщо не вистачає пам’яті (OOM):

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## Часті фікси

| Проблема | Що зробити |
|--------|-------------|
| Не той Node | `20.18.2` з `.nvmrc` |
| Пробіли в шляху | Перенесіть репо |
| React / OOM | `buildreact` з `NODE_OPTIONS=8192` |
| Linux sandbox | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## Зв’язок

- Пошта: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
