from PIL import Image
from pathlib import Path

root = Path(r"c:\Users\palapalaru\Desktop\404Brain")
src = root / "404brain-logo.png"
assert src.exists(), src

img = Image.open(src).convert("RGBA")

# Make near-white / light-gray background transparent
pixels = img.load()
w, h = img.size
for y in range(h):
    for x in range(w):
        r, g, b, a = pixels[x, y]
        if r > 230 and g > 230 and b > 230:
            pixels[x, y] = (r, g, b, 0)

bbox = img.getbbox()
if bbox:
    pad = 8
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(w, x1 + pad)
    y1 = min(h, y1 + pad)
    img = img.crop((x0, y0, x1, y1))


def square_canvas(im, size, bg=(0, 0, 0, 0)):
    canvas = Image.new("RGBA", (size, size), bg)
    im2 = im.copy()
    im2.thumbnail((size, size), Image.Resampling.LANCZOS)
    ox = (size - im2.width) // 2
    oy = (size - im2.height) // 2
    canvas.paste(im2, (ox, oy), im2)
    return canvas


def save_png(path, size, bg=(0, 0, 0, 0)):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    square_canvas(img, size, bg).save(path, "PNG")
    print("png", path.relative_to(root), size)


def save_ico(path, sizes):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    icons = [square_canvas(img, s) for s in sizes]
    icons[0].save(
        path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
        append_images=icons[1:],
    )
    print("ico", path.relative_to(root), sizes)


save_png(root / "resources/linux/code.png", 1024)
save_png(root / "resources/server/code-192.png", 192)
save_png(root / "resources/server/code-512.png", 512)
save_png(root / "resources/win32/code_70x70.png", 70)
save_png(root / "resources/win32/code_150x150.png", 150)
save_png(root / "resources/win32/logo_cube_noshadow.png", 1024)
save_ico(root / "resources/win32/code.ico", [16, 24, 32, 48, 64, 128, 256])
save_ico(root / "resources/server/favicon.ico", [16, 32, 48])

save_ico(root / "void_icons/code.ico", [16, 24, 32, 48, 64, 128, 256])
save_png(root / "void_icons/cubecircled.png", 512)
save_png(root / "void_icons/logo_cube_noshadow.png", 1024)
save_png(root / "void_icons/slice_of_void.png", 1024)

media = root / "src/vs/workbench/browser/parts/editor/media"
save_png(media / "void_cube_noshadow.png", 1024)
save_png(media / "slice_of_void.png", 1024)

icns_path = root / "resources/darwin/code.icns"
try:
    icns_sizes = [16, 32, 64, 128, 256, 512, 1024]
    layers = [square_canvas(img, s) for s in icns_sizes]
    layers[0].save(icns_path, format="ICNS", append_images=layers[1:])
    print("icns", icns_path.relative_to(root), "ok")
except Exception as e:
    save_png(root / "resources/darwin/code.png", 1024)
    print("icns FAILED:", e)

print("DONE")
