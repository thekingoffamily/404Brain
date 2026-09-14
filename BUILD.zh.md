# 构建 404Brain（本地）

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2**（见 `.nvmrc`）。仓库路径中**不能有空格**。

---

## 0. 一次性依赖

### Windows

1. 安装 [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community)（或 Build Tools）。
2. Workloads：**Desktop development with C++**、**Node.js build tools**。
3. Individual components：
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. 安装。

### Mac

Python + Xcode（通常已有）。

### Linux

```bash
npm install -g node-gyp
```

然后（Debian/Ubuntu）：

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. 克隆 + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Node 版本：

```bash
nvm install
nvm use
```

（或以其他方式安装 Node `20.18.2`）

```bash
npm install
```

---

## 2. 构建（watch）

**方式 A — 终端**

```bash
npm run watch
```

等到大致出现如下两行：

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**方式 B — 在 VS Code / Cursor 中**

按 `Ctrl+Shift+B`（Mac：`Cmd+Shift+B`），等待构建任务完成（首次约 5 分钟）。

---

## 3. 运行开发模式

**Windows：**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux：**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

会打开 404Brain 窗口。改代码后：`Ctrl+R` / `Cmd+R`（或命令面板 → **Reload Window**）。

重置本地 IDE 状态：删除 `.tmp` 文件夹。

---

## 4. React UI（若修改了 `contrib/brain` 下的 React）

```bash
npm run buildreact
```

若内存不足（OOM）：

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## 常见问题

| 问题 | 处理 |
|--------|-----|
| Node 版本不对 | 使用 `.nvmrc` 中的 `20.18.2` |
| 路径含空格 | 移动仓库 |
| React / OOM | 如上使用 `NODE_OPTIONS=8192` 运行 `buildreact` |
| Linux sandbox 错误 | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## 联系

- 邮箱: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
