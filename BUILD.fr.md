# Builder 404Brain (local)

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2** (voir `.nvmrc`). Le chemin du dépôt ne doit **pas** contenir d’espaces.

---

## 0. Prérequis (une fois)

### Windows

1. Installez [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (ou Build Tools).
2. Workloads : **Desktop development with C++**, **Node.js build tools**.
3. Individual components :
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. Installer.

### Mac

Python + Xcode (souvent déjà là).

### Linux

```bash
npm install -g node-gyp
```

Puis (Debian/Ubuntu) :

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. Cloner + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Version de Node :

```bash
nvm install
nvm use
```

(ou installez Node `20.18.2` autrement)

```bash
npm install
```

---

## 2. Build (watch)

**Option A — terminal**

```bash
npm run watch
```

Attendez des lignes du genre :

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**Option B — depuis VS Code / Cursor**

Appuyez sur `Ctrl+Shift+B` (Mac : `Cmd+Shift+B`) et attendez la fin (~5 min la première fois).

---

## 3. Mode développeur

**Windows :**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux :**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

Une fenêtre 404Brain s’ouvre. Après des changements : `Ctrl+R` / `Cmd+R` (ou Command Palette → **Reload Window**).

Pour réinitialiser l’état local : supprimez le dossier `.tmp`.

---

## 4. UI React (si vous modifiez React sous `contrib/brain`)

```bash
npm run buildreact
```

En cas d’OOM :

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## Correctifs courants

| Problème | Correctif |
|--------|-----|
| Mauvais Node | Utilisez `20.18.2` de `.nvmrc` |
| Espaces dans le chemin | Déplacez le dépôt |
| React / OOM | `buildreact` avec `NODE_OPTIONS=8192` |
| Erreur sandbox Linux | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## Contact

- E-mail: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
