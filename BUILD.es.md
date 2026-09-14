# Compilar 404Brain (local)

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2** (ver `.nvmrc`). La ruta del repo **no** debe tener espacios.

---

## 0. Prerrequisitos (una vez)

### Windows

1. Instala [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (o Build Tools).
2. Workloads: **Desktop development with C++**, **Node.js build tools**.
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. Instalar.

### Mac

Python + Xcode (suele estar ya).

### Linux

```bash
npm install -g node-gyp
```

Luego (Debian/Ubuntu):

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. Clonar + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Versión de Node:

```bash
nvm install
nvm use
```

(o instala Node `20.18.2` de otra forma)

```bash
npm install
```

---

## 2. Build (watch)

**Opción A — terminal**

```bash
npm run watch
```

Espera hasta ver algo como:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**Opción B — desde VS Code / Cursor**

Pulsa `Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) y espera a que terminen las tareas (~5 min la primera vez).

---

## 3. Modo desarrollador

**Windows:**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux:**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

Se abre una ventana de 404Brain. Tras cambios: `Ctrl+R` / `Cmd+R` (o Command Palette → **Reload Window**).

Para resetear el estado local: borra la carpeta `.tmp`.

---

## 4. UI React (si cambias React en `contrib/brain`)

```bash
npm run buildreact
```

Si se queda sin memoria (OOM):

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## Arreglos comunes

| Problema | Solución |
|--------|-----|
| Node incorrecto | Usa `20.18.2` de `.nvmrc` |
| Espacios en la ruta | Mueve el repo |
| React / OOM | `buildreact` con `NODE_OPTIONS=8192` |
| Error sandbox Linux | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## Contacto

- Email: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
