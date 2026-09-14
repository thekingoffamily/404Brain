# 404Brain のビルド（ローカル）

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2**（`.nvmrc` 参照）。リポジトリパスに**スペースを含めない**こと。

---

## 0. 事前準備（一度だけ）

### Windows

1. [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community)（または Build Tools）をインストール。
2. Workloads: **Desktop development with C++**, **Node.js build tools**。
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. インストール。

### Mac

Python + Xcode（通常は既にある）。

### Linux

```bash
npm install -g node-gyp
```

その後（Debian/Ubuntu）:

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. クローン + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Node バージョン:

```bash
nvm install
nvm use
```

（または別の方法で Node `20.18.2` を入れる）

```bash
npm install
```

---

## 2. ビルド（watch）

**方法 A — ターミナル**

```bash
npm run watch
```

次のような行が出るまで待つ:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**方法 B — VS Code / Cursor から**

`Ctrl+Shift+B`（Mac: `Cmd+Shift+B`）を押し、タスク完了まで待つ（初回は約 5 分）。

---

## 3. 開発モードで起動

**Windows:**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux:**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

404Brain のウィンドウが開きます。コード変更後: `Ctrl+R` / `Cmd+R`（または Command Palette → **Reload Window**）。

ローカル IDE 状態のリセット: `.tmp` フォルダを削除。

---

## 4. React UI（`contrib/brain` 配下の React を変えた場合）

```bash
npm run buildreact
```

メモリ不足（OOM）の場合:

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## よくある修正

| 問題 | 対処 |
|--------|-----|
| Node が違う | `.nvmrc` の `20.18.2` を使う |
| パスにスペース | リポジトリを移す |
| React / OOM | 上記どおり `NODE_OPTIONS=8192` で `buildreact` |
| Linux sandbox エラー | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## 連絡先

- メール: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
