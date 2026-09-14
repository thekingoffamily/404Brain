# 404Brain bauen (lokal)

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2** (siehe `.nvmrc`). Der Repo-Pfad darf **keine** Leerzeichen enthalten.

---

## 0. Voraussetzungen (einmalig)

### Windows

1. Installiere [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (oder Build Tools).
2. Workloads: **Desktop development with C++**, **Node.js build tools**.
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. Installieren.

### Mac

Python + Xcode (meist schon da).

### Linux

```bash
npm install -g node-gyp
```

Dann (Debian/Ubuntu):

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. Klonen + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Node-Version:

```bash
nvm install
nvm use
```

(oder Node `20.18.2` anders installieren)

```bash
npm install
```

---

## 2. Build (watch)

**Option A — Terminal**

```bash
npm run watch
```

Warte, bis du ungefähr siehst:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**Option B — in VS Code / Cursor**

`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) drücken und warten (~5 Min beim ersten Mal).

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

Ein 404Brain-Fenster öffnet sich. Nach Code-Änderungen: `Ctrl+R` / `Cmd+R` (oder Command Palette → **Reload Window**).

Lokalen IDE-Zustand zurücksetzen: Ordner `.tmp` löschen.

---

## 4. React-UI (bei Änderungen unter `contrib/brain`)

```bash
npm run buildreact
```

Bei OOM:

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## Häufige Fixes

| Problem | Fix |
|--------|-----|
| Falsche Node-Version | `20.18.2` aus `.nvmrc` |
| Leerzeichen im Pfad | Repo verschieben |
| React / OOM | `buildreact` mit `NODE_OPTIONS=8192` |
| Linux-Sandbox-Fehler | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## Kontakt

- E-Mail: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
