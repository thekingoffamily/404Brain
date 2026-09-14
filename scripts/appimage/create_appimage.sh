#!/bin/bash

# Exit on error
set -e

# Check platform
platform=$(uname)

if [[ "$platform" == "Darwin" ]]; then
    echo "Running on macOS. Note that the AppImage created will only work on Linux systems."
    if ! command -v docker &> /dev/null; then
        echo "Docker Desktop for Mac is not installed. Please install it from https://www.docker.com/products/docker-desktop"
        exit 1
    fi
elif [[ "$platform" == "Linux" ]]; then
    echo "Running on Linux. Proceeding with AppImage creation..."
else
    echo "This script is intended to run on macOS or Linux. Current platform: $platform"
    exit 1
fi

# Enable BuildKit
export DOCKER_BUILDKIT=1

BUILD_IMAGE_NAME="brain-appimage-builder"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Docker is not running. Please start Docker first."
    exit 1
fi

# Check and install Buildx if needed
if ! docker buildx version >/dev/null 2>&1; then
    echo "Installing Docker Buildx..."
    mkdir -p ~/.docker/cli-plugins/
    curl -SL https://github.com/docker/buildx/releases/download/v0.13.1/buildx-v0.13.1.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx
    chmod +x ~/.docker/cli-plugins/docker-buildx
fi

# Download appimagetool if not present
if [ ! -f "appimagetool" ]; then
    echo "Downloading appimagetool..."
    wget -O appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool
fi

# Delete any existing AppImage to avoid bloating the build
rm -f Brain-x86_64.AppImage

# Create build Dockerfile
echo "Creating build Dockerfile..."
cat > Dockerfile.build << 'EOF'
# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# Install required dependencies
RUN apt-get update && apt-get install -y \
    libfuse2 \
    libglib2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxss1 \
    libxtst6 \
    libnss3 \
    libasound2 \
    libdrm2 \
    libgbm1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
EOF

# Create .dockerignore file
echo "Creating .dockerignore file..."
cat > .dockerignore << EOF
Dockerfile.build
.dockerignore
.git
.gitignore
.DS_Store
*~
*.swp
*.swo
*.tmp
*.bak
*.log
*.err
node_modules/
venv/
*.egg-info/
*.tox/
dist/
EOF

# Build Docker image without cache
echo "Building Docker image (no cache)..."
docker build --no-cache -t "$BUILD_IMAGE_NAME" -f Dockerfile.build .

# Create AppImage using local appimagetool
echo "Creating AppImage..."
docker run --rm --privileged -v "$(pwd):/app" "$BUILD_IMAGE_NAME" bash -c '
cd /app && \
rm -rf BrainApp.AppDir && \
mkdir -p BrainApp.AppDir/usr/bin BrainApp.AppDir/usr/lib BrainApp.AppDir/usr/share/applications && \
find . -maxdepth 1 ! -name BrainApp.AppDir ! -name "." ! -name ".." -exec cp -r {} BrainApp.AppDir/usr/bin/ \; && \
cp brain.png BrainApp.AppDir/ && \
echo "[Desktop Entry]" > BrainApp.AppDir/brain.desktop && \
echo "Name=Brain" >> BrainApp.AppDir/brain.desktop && \
echo "Comment=Open source AI code editor." >> BrainApp.AppDir/brain.desktop && \
echo "GenericName=Text Editor" >> BrainApp.AppDir/brain.desktop && \
echo "Exec=void %F" >> BrainApp.AppDir/brain.desktop && \
echo "Icon=void" >> BrainApp.AppDir/brain.desktop && \
echo "Type=Application" >> BrainApp.AppDir/brain.desktop && \
echo "StartupNotify=false" >> BrainApp.AppDir/brain.desktop && \
echo "StartupWMClass=Brain" >> BrainApp.AppDir/brain.desktop && \
echo "Categories=TextEditor;Development;IDE;" >> BrainApp.AppDir/brain.desktop && \
echo "MimeType=application/x-brain-workspace;" >> BrainApp.AppDir/brain.desktop && \
echo "Keywords=void;" >> BrainApp.AppDir/brain.desktop && \
echo "Actions=new-empty-window;" >> BrainApp.AppDir/brain.desktop && \
echo "[Desktop Action new-empty-window]" >> BrainApp.AppDir/brain.desktop && \
echo "Name=New Empty Window" >> BrainApp.AppDir/brain.desktop && \
echo "Name[de]=Neues leeres Fenster" >> BrainApp.AppDir/brain.desktop && \
echo "Name[es]=Nueva ventana vacía" >> BrainApp.AppDir/brain.desktop && \
echo "Name[fr]=Nouvelle fenêtre vide" >> BrainApp.AppDir/brain.desktop && \
echo "Name[it]=Nuova finestra vuota" >> BrainApp.AppDir/brain.desktop && \
echo "Name[ja]=新しい空のウィンドウ" >> BrainApp.AppDir/brain.desktop && \
echo "Name[ko]=새 빈 창" >> BrainApp.AppDir/brain.desktop && \
echo "Name[ru]=Новое пустое окно" >> BrainApp.AppDir/brain.desktop && \
echo "Name[zh_CN]=新建空窗口" >> BrainApp.AppDir/brain.desktop && \
echo "Name[zh_TW]=開新空視窗" >> BrainApp.AppDir/brain.desktop && \
echo "Exec=void --new-window %F" >> BrainApp.AppDir/brain.desktop && \
echo "Icon=void" >> BrainApp.AppDir/brain.desktop && \
chmod +x BrainApp.AppDir/brain.desktop && \
cp BrainApp.AppDir/brain.desktop BrainApp.AppDir/usr/share/applications/ && \
echo "[Desktop Entry]" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "Name=Brain - URL Handler" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "Comment=Open source AI code editor." > BrainApp.AppDir/brain-url-handler.desktop && \
echo "GenericName=Text Editor" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "Exec=void --open-url %U" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "Icon=void" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "Type=Application" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "NoDisplay=true" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "StartupNotify=true" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "Categories=Utility;TextEditor;Development;IDE;" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "MimeType=x-scheme-handler/void;" > BrainApp.AppDir/brain-url-handler.desktop && \
echo "Keywords=void;" > BrainApp.AppDir/brain-url-handler.desktop && \
chmod +x BrainApp.AppDir/brain-url-handler.desktop && \
cp BrainApp.AppDir/brain-url-handler.desktop BrainApp.AppDir/usr/share/applications/ && \
echo "#!/bin/bash" > BrainApp.AppDir/AppRun && \
echo "HERE=\$(dirname \"\$(readlink -f \"\${0}\")\")" >> BrainApp.AppDir/AppRun && \
echo "export PATH=\${HERE}/usr/bin:\${PATH}" >> BrainApp.AppDir/AppRun && \
echo "export LD_LIBRARY_PATH=\${HERE}/usr/lib:\${LD_LIBRARY_PATH}" >> BrainApp.AppDir/AppRun && \
echo "exec \${HERE}/usr/bin/void --no-sandbox \"\$@\"" >> BrainApp.AppDir/AppRun && \
chmod +x BrainApp.AppDir/AppRun && \
chmod -R 755 BrainApp.AppDir && \

# Strip unneeded symbols from the binary to reduce size
strip --strip-unneeded BrainApp.AppDir/usr/bin/void

ls -la BrainApp.AppDir/ && \
ARCH=x86_64 ./appimagetool -n BrainApp.AppDir Brain-x86_64.AppImage
'

# Clean up
rm -rf BrainApp.AppDir .dockerignore appimagetool

echo "AppImage creation complete! Your AppImage is: Brain-x86_64.AppImage"
