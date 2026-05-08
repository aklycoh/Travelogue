import os
from PIL import Image, ImageOps
import pillow_heif
pillow_heif.register_heif_opener()

SRC = r"D:/program/Travelogue"
OUT_FULL = os.path.join(SRC, "images", "full")
OUT_THUMB = os.path.join(SRC, "images", "thumb")
os.makedirs(OUT_FULL, exist_ok=True)
os.makedirs(OUT_THUMB, exist_ok=True)

def process(path):
    base = os.path.splitext(os.path.basename(path))[0]
    full_path = os.path.join(OUT_FULL, base + ".jpg")
    thumb_path = os.path.join(OUT_THUMB, base + ".jpg")
    if os.path.exists(full_path) and os.path.exists(thumb_path):
        return
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    if img.mode != "RGB":
        img = img.convert("RGB")
    full = img.copy()
    full.thumbnail((1800, 1800), Image.LANCZOS)
    full.save(full_path, "JPEG", quality=82, optimize=True, progressive=True)
    thumb = img.copy()
    thumb.thumbnail((600, 600), Image.LANCZOS)
    thumb.save(thumb_path, "JPEG", quality=78, optimize=True, progressive=True)
    print("ok", base)

files = [f for f in os.listdir(SRC) if f.lower().endswith((".heic",".jpg",".jpeg"))]
for f in sorted(files):
    try:
        process(os.path.join(SRC, f))
    except Exception as e:
        print("FAIL", f, e)
print("done")
