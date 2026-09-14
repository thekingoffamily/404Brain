# Build 404Brain (local)

Node **20.18.2** (see `.nvmrc`). Path to the repo must **not** contain spaces.

---

## 0. Prerequisites (once)

### Windows

1. Install [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (or Build Tools).
2. Workloads: **Desktop development with C++**, **Node.js build tools**.
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. Install.

### Mac

Python + Xcode (usually already there).

### Linux

```bash
npm install -g node-gyp
```

Then (Debian/Ubuntu):

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. Clone + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Node version:

```bash
nvm install
nvm use
```

(or install Node `20.18.2` another way)

```bash
npm install
```

---

## 2. Build (watch)

**Option A — from terminal**

```bash
npm run watch
```

Wait until you see both lines roughly like:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**Option B — from VS Code / Cursor**

Press `Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) and wait until the build tasks finish (~5 min first time).

---

## 3. Run Developer Mode

**Windows:**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux:**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

A 404Brain window opens. After code changes: `Ctrl+R` / `Cmd+R` (or Command Palette → **Reload Window**).

To reset local IDE state: delete the `.tmp` folder.

---

## 4. React UI (if you change React under `contrib/void`)

```bash
npm run buildreact
```

If it OOMs:

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## Common fixes

| Problem | Fix |
|--------|-----|
| Wrong Node | Use `20.18.2` from `.nvmrc` |
| Path with spaces | Move the repo |
| React / OOM | `buildreact` with `NODE_OPTIONS=8192` as above |
| Linux sandbox error | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## Contact

- Email: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)

---

## Русский — коротко по шагам

1. Поставь Node **20.18.2** и C++ build tools (на Windows — VS 2022, см. выше).
2. `git clone https://github.com/thekingoffamily/404Brain` → `cd 404Brain` → `npm install`.
3. `npm run watch` — жди `0 errors`.
4. Windows: `.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions`  
   Mac/Linux: `./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions`
5. Меняешь код → в окне 404Brain жми **Reload** (`Ctrl+R` / `Cmd+R`).
6. Трогал React → `npm run buildreact`.
