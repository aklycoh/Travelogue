import os, json
from PIL import Image, ExifTags
import pillow_heif
pillow_heif.register_heif_opener()

GPSTAGS = ExifTags.GPSTAGS
TAGS = ExifTags.TAGS

def to_deg(val):
    try:
        d, m, s = val
        return float(d) + float(m)/60 + float(s)/3600
    except Exception:
        return None

def get_meta(path):
    info = {"file": os.path.basename(path)}
    try:
        img = Image.open(path)
        info["size"] = img.size
        exif = img.getexif()
        if exif:
            for tid, val in exif.items():
                tag = TAGS.get(tid, tid)
                if tag == "DateTime":
                    info["DateTime"] = str(val)
                if tag == "DateTimeOriginal":
                    info["DateTimeOriginal"] = str(val)
                if tag == "Make":
                    info["Make"] = str(val)
                if tag == "Model":
                    info["Model"] = str(val)
            # IFD ExifOffset for DateTimeOriginal
            try:
                exif_ifd = exif.get_ifd(0x8769)
                for tid, val in exif_ifd.items():
                    tag = TAGS.get(tid, tid)
                    if tag in ("DateTimeOriginal","DateTimeDigitized"):
                        info[tag] = str(val)
                    if tag == "LensModel":
                        info["LensModel"] = str(val)
            except Exception:
                pass
            try:
                gps_ifd = exif.get_ifd(0x8825)
                if gps_ifd:
                    g = {GPSTAGS.get(k,k): v for k,v in gps_ifd.items()}
                    lat = to_deg(g.get("GPSLatitude")) if g.get("GPSLatitude") else None
                    lon = to_deg(g.get("GPSLongitude")) if g.get("GPSLongitude") else None
                    if lat and g.get("GPSLatitudeRef") == "S": lat = -lat
                    if lon and g.get("GPSLongitudeRef") == "W": lon = -lon
                    if lat and lon:
                        info["GPS"] = [round(lat,6), round(lon,6)]
                    if g.get("GPSAltitude"):
                        try:
                            info["Alt"] = round(float(g["GPSAltitude"]),1)
                        except Exception:
                            pass
            except Exception:
                pass
    except Exception as e:
        info["error"] = str(e)
    return info

root = r"D:/program/Travelogue"
files = [f for f in os.listdir(root) if f.lower().endswith((".heic",".jpg",".jpeg"))]
files.sort()
out = [get_meta(os.path.join(root,f)) for f in files]
print(json.dumps(out, ensure_ascii=False, indent=2))
