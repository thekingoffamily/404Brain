# Build 404Brain (local)

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2** (veja `.nvmrc`). O caminho do repo **não** pode ter espaços.

---

## 0. Pré-requisitos (uma vez)

### Windows

1. Instale [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (ou Build Tools).
2. Workloads: **Desktop development with C++**, **Node.js build tools**.
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. Instalar.

### Mac

Python + Xcode (geralmente já existe).

### Linux

```bash
npm install -g node-gyp
```

Depois (Debian/Ubuntu):

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. Clone + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Versão do Node:

```bash
nvm install
nvm use
```

(ou instale Node `20.18.2` de outro jeito)

```bash
npm install
```

---

## 2. Build (watch)

**Opção A — terminal**

```bash
npm run watch
```

Espere ver linhas parecidas com:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**Opção B — no VS Code / Cursor**

Pressione `Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) e aguarde as tasks (~5 min na primeira vez).

---

## 3. Modo desenvolvedor

**Windows:**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux:**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

Abre uma janela 404Brain. Após mudanças: `Ctrl+R` / `Cmd+R` (ou Command Palette → **Reload Window**).

Para resetar o estado local: apague a pasta `.tmp`.

---

## 4. UI React (se alterar React em `contrib/brain`)

```bash
npm run buildreact
```

Se der OOM:

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## Correções comuns

| Problema | Correção |
|--------|-----|
| Node errado | Use `20.18.2` do `.nvmrc` |
| Espaços no caminho | Mova o repo |
| React / OOM | `buildreact` com `NODE_OPTIONS=8192` |
| Erro sandbox Linux | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## Contato

- Email: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
