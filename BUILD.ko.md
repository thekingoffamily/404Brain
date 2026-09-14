# 404Brain 빌드 (로컬)

[English](./BUILD.md) · [Русский](./BUILD.ru.md) · [中文](./BUILD.zh.md) · [Español](./BUILD.es.md) · [Português](./BUILD.pt.md) · [Deutsch](./BUILD.de.md) · [Français](./BUILD.fr.md) · [日本語](./BUILD.ja.md) · [한국어](./BUILD.ko.md) · [Українська](./BUILD.uk.md)

Node **20.18.2** (`.nvmrc` 참고). 저장소 경로에 **공백이 있으면 안 됩니다**.

---

## 0. 사전 준비 (한 번)

### Windows

1. [Visual Studio 2022 Community](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community) (또는 Build Tools) 설치.
2. Workloads: **Desktop development with C++**, **Node.js build tools**.
3. Individual components:
   - `MSVC v143 - VS 2022 C++ x64/x86 Spectre-mitigated libs (Latest)`
   - `C++ ATL for latest build tools with Spectre Mitigations`
   - `C++ MFC for latest build tools with Spectre Mitigations`
4. 설치.

### Mac

Python + Xcode (보통 이미 있음).

### Linux

```bash
npm install -g node-gyp
```

그다음 (Debian/Ubuntu):

```bash
sudo apt-get install build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev libkrb5-dev python-is-python3
```

---

## 1. 클론 + install

```bash
git clone https://github.com/thekingoffamily/404Brain
cd 404Brain
```

Node 버전:

```bash
nvm install
nvm use
```

(또는 다른 방식으로 Node `20.18.2` 설치)

```bash
npm install
```

---

## 2. 빌드 (watch)

**옵션 A — 터미널**

```bash
npm run watch
```

대략 이런 줄이 나올 때까지 대기:

```text
Finished compilation extensions with 0 errors
Finished compilation with 0 errors
```

**옵션 B — VS Code / Cursor**

`Ctrl+Shift+B` (Mac: `Cmd+Shift+B`) 후 작업 완료까지 대기 (처음엔 약 5분).

---

## 3. 개발 모드 실행

**Windows:**

```bat
.\scripts\code.bat --user-data-dir .\.tmp\user-data --extensions-dir .\.tmp\extensions
```

**Mac / Linux:**

```bash
./scripts/code.sh --user-data-dir ./.tmp/user-data --extensions-dir ./.tmp/extensions
```

404Brain 창이 열립니다. 코드 변경 후: `Ctrl+R` / `Cmd+R` (또는 Command Palette → **Reload Window**).

로컬 IDE 상태 초기화: `.tmp` 폴더 삭제.

---

## 4. React UI (`contrib/brain` React를 바꾼 경우)

```bash
npm run buildreact
```

메모리 부족(OOM)이면:

```powershell
# Windows PowerShell
$env:NODE_OPTIONS="--max-old-space-size=8192"; npm run buildreact
```

```bash
# Mac / Linux
NODE_OPTIONS="--max-old-space-size=8192" npm run buildreact
```

---

## 자주 쓰는 해결

| 문제 | 해결 |
|--------|-----|
| Node 버전이 다름 | `.nvmrc`의 `20.18.2` 사용 |
| 경로에 공백 | 저장소 이동 |
| React / OOM | 위처럼 `NODE_OPTIONS=8192`로 `buildreact` |
| Linux sandbox 오류 | `sudo chown root:root .build/electron/chrome-sandbox && sudo chmod 4755 .build/electron/chrome-sandbox` |

---

## 연락처

- 이메일: [thekingoffamily2017@gmail.com](mailto:thekingoffamily2017@gmail.com)
- Telegram: [@palapalaru](https://t.me/palapalaru)
