import json
import os
import subprocess

SCRIPTS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(SCRIPTS_DIR)

OUTPUT_DIR = os.path.join(REPO_ROOT, "output")
ASSETS_DIR = os.environ.get("MINDFUL_ASSETS_DIR", os.path.join(REPO_ROOT, "assets"))
TMP_DIR = os.path.join(REPO_ROOT, ".astro", "tmp_subtitles")
CATALOG_PATH = os.path.join(SCRIPTS_DIR, "products_catalog.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)


def resolve_asset_path(rel_path: str, legacy_tmp_path: str | None = None) -> str:
    """
    永続化された assets/ 配下のパスを優先して返し、未配置の場合はレガシー /tmp パスへフォールバックする。
    """
    primary = os.path.join(ASSETS_DIR, rel_path)
    if os.path.exists(primary):
        return primary
    if legacy_tmp_path and os.path.exists(legacy_tmp_path):
        return legacy_tmp_path
    return primary


def load_products_catalog() -> dict[str, dict]:
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {item["id"]: item for item in data.get("products", [])}


def render_subtitle_png(png_path: str, lines: list[dict]):
    """
    macOS AppKit (HiraginoSans-W6/W3 + NSShadow) を使って 1080x1920 の透過PNG字幕カードを生成する。
    lines: [{"text": str, "y": int, "size": int, "alpha": float, "weight": Optional[str]}]
    """
    lines_json = json.dumps(lines, ensure_ascii=False)
    jxa_script = f"""
ObjC.import("AppKit");
const width = 1080, height = 1920;
const rep = $.NSBitmapImageRep.alloc.initWithBitmapDataPlanesPixelsWidePixelsHighBitsPerSampleSamplesPerPixelHasAlphaIsPlanarColorSpaceNameBytesPerRowBitsPerPixel(
  null, width, height, 8, 4, true, false, $.NSDeviceRGBColorSpace, 0, 0
);
const ctx = $.NSGraphicsContext.graphicsContextWithBitmapImageRep(rep);
$.NSGraphicsContext.setCurrentContext(ctx);

$.NSColor.clearColor.set;
$.NSRectFill($.NSMakeRect(0, 0, width, height));

const shadow = $.NSShadow.alloc.init;
shadow.setShadowOffset($.NSMakeSize(0, -2));
shadow.setShadowBlurRadius(12.0);
shadow.setShadowColor($.NSColor.colorWithCalibratedWhiteAlpha(0.0, 0.88));

const lines = {lines_json};
for (const item of lines) {{
  const fontName = item.weight === "W3" ? "HiraginoSans-W3" : "HiraginoSans-W6";
  const font = $.NSFont.fontWithNameSize(fontName, item.size || 46);
  const attrs = $.NSMutableDictionary.alloc.init;
  attrs.setObjectForKey(font, $.NSFontAttributeName);
  attrs.setObjectForKey($.NSColor.colorWithCalibratedWhiteAlpha(1.0, item.alpha || 0.98), $.NSForegroundColorAttributeName);
  attrs.setObjectForKey(shadow, $.NSShadowAttributeName);

  const nsStr = $.NSString.stringWithString(item.text);
  const size = nsStr.sizeWithAttributes(attrs);
  const x = Math.round((width - size.width) / 2);
  const y = Math.round(height - item.y - (size.height / 2));
  nsStr.drawAtPointWithAttributes($.NSMakePoint(x, y), attrs);
  nsStr.drawAtPointWithAttributes($.NSMakePoint(x, y), attrs);
}}

$.NSGraphicsContext.currentContext.flushGraphics;
const pngData = rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $.NSDictionary.dictionary);
pngData.writeToFileAtomically({json.dumps(png_path)}, true);
"""
    subprocess.run(["osascript", "-l", "JavaScript", "-e", jxa_script], check=True)


def build_video(
    input_video: str,
    output_mp4: str,
    duration: float,
    cards: list[dict],
    audio_path: str | None = None,
    audio_volume: float = 0.32,
    start_offset: float = 0.0,
    audio_offset: float = 0.0,
    crop_filter: str = "scale=-2:1920:flags=lanczos,crop=1080:1920",
):
    """
    背景動画・透過PNG字幕カード・環境音を ffmpeg で合成して 1080x1920 MP4 を出力する共通ビルダー。
    """
    if not os.path.exists(input_video):
        raise FileNotFoundError(
            f"Input video not found: {input_video} (place source media in {ASSETS_DIR})"
        )

    png_paths = []
    for idx, card in enumerate(cards):
        png_path = os.path.join(TMP_DIR, f"{os.path.basename(output_mp4)}_card_{idx}.png")
        render_subtitle_png(png_path, card["lines"])
        png_paths.append(png_path)

    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{start_offset:.2f}",
        "-t", f"{duration:.2f}",
        "-i", input_video,
    ]
    for p in png_paths:
        cmd.extend(["-loop", "1", "-t", f"{duration:.2f}", "-i", p])

    if audio_path:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(
                f"Audio file not found: {audio_path} (place source audio in {ASSETS_DIR})"
            )
        cmd.extend(["-ss", f"{audio_offset:.2f}", "-t", f"{duration:.2f}", "-i", audio_path])

    filter_parts = [
        f"[0:v]{crop_filter},fps=30,format=yuv420p[v0]"
    ]
    prev_v = "v0"
    for idx, card in enumerate(cards):
        in_idx = idx + 1
        st = card["start"]
        ed = card["end"]
        fi = card.get("fade_in", 0.35)
        fo = card.get("fade_out", 0.5)
        fo_start = max(st, ed - fo)
        sub_label = f"sub{idx}"
        out_label = f"v{idx+1}"

        f_str = f"[{in_idx}:v]format=rgba"
        if fi > 0:
            f_str += f",fade=t=in:st={st:.2f}:d={fi:.2f}:alpha=1"
        if fo > 0:
            f_str += f",fade=t=out:st={fo_start:.2f}:d={fo:.2f}:alpha=1"
        f_str += f"[{sub_label}]"
        filter_parts.append(f_str)

        filter_parts.append(
            f"[{prev_v}][{sub_label}]overlay=0:0:enable='between(t,{st:.2f},{ed:.2f})':format=auto[{out_label}]"
        )
        prev_v = out_label

    if audio_path:
        audio_in_idx = len(cards) + 1
        fade_out_st = max(0.0, duration - 2.0)
        filter_parts.append(
            f"[{audio_in_idx}:a]volume={audio_volume},afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_st:.2f}:d=2.0[aout]"
        )
        cmd.extend([
            "-filter_complex", ";".join(filter_parts),
            "-map", f"[{prev_v}]",
            "-map", "[aout]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "faster",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_mp4,
        ])
    else:
        cmd.extend([
            "-f", "lavfi", "-t", f"{duration:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-filter_complex", ";".join(filter_parts),
            "-map", f"[{prev_v}]",
            "-map", f"{len(cards)+1}:a",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "faster",
            "-crf", "20",
            "-c:a", "aac",
            "-b:a", "128k",
            "-shortest",
            output_mp4,
        ])

    print(f"Rendering {output_mp4} ...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    print(f"Done: {output_mp4}")
