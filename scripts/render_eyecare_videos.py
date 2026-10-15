import os
import subprocess
import json

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
TMP_DIR = "/tmp/eyecare_subtitles"
os.makedirs(TMP_DIR, exist_ok=True)


def render_subtitle_png(png_path: str, lines: list[dict]):
    """
    macOS AppKit (HiraginoSans-W6 + NSShadow) を使って 1080x1920 の透過PNG字幕カードを生成する。
    lines: [{"text": str, "y": int, "size": int, "alpha": float}]
      y は画面上端からの中心Y座標 (1080x1920基準、6万再生動画は y=400, 480)
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
  const font = $.NSFont.fontWithNameSize(fontName, item.size || 47);
  const attrs = $.NSMutableDictionary.alloc.init;
  attrs.setObjectForKey(font, $.NSFontAttributeName);
  attrs.setObjectForKey($.NSColor.colorWithCalibratedWhiteAlpha(1.0, item.alpha || 0.98), $.NSForegroundColorAttributeName);
  attrs.setObjectForKey(shadow, $.NSShadowAttributeName);

  const nsStr = $.NSString.stringWithString(item.text);
  const size = nsStr.sizeWithAttributes(attrs);
  const x = Math.round((width - size.width) / 2);
  const y = Math.round(height - item.y - (size.height / 2));
  // Draw twice so drop shadow is rich and legible on any natural background
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
    audio_volume: float = 0.35,
    start_offset: float = 0.0,
    crop_filter: str = "scale=-2:1920:flags=lanczos,crop=1080:1920",
):
    """
    cards: [
      {
        "start": float,
        "end": float,
        "fade_in": float,
        "fade_out": float,
        "lines": [{"text": ..., "y": ..., "size": ..., "alpha": ...}]
      }
    ]
    """
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
        cmd.extend(["-ss", "0.0", "-t", f"{duration:.2f}", "-i", audio_path])

    # Build filter_complex
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
        # Silent audio track for TikTok compatibility
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


if __name__ == "__main__":
    stream_video = "/tmp/stream_6918262.mp4"
    leaves_video = "/tmp/leaves_6186130.mp4"
    swale_audio = "/tmp/Swale.ogg"

    stream_crop = "scale=-2:1920:flags=lanczos,crop=1080:1920:1950:0,eq=brightness=-0.06:contrast=1.06:saturation=1.06"

    # 1. 24秒・森の清流×小川環境音（ソフト誘導あり版）
    build_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "eyecare_stream_24s_shop_and_lp.mp4"),
        duration=24.0,
        start_offset=2.0,
        audio_path=swale_audio,
        audio_volume=0.35,
        crop_filter=stream_crop,
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.6,
                "lines": [
                    {"text": "今日も画面を見続けた目へ。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "今は、水の流れを眺めるだけ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.6,
                "lines": [
                    {"text": "ピントを合わせるのをやめて、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "ぼんやり見送る24秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 18.2s (10.4秒間) は完全無字幕で目を休める時間
            {
                "start": 18.2,
                "end": 24.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "このままスマホを置いて、", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "目元を温めて眠る夜も。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※夜に使っているアイマスクはリンクへ", "y": 548, "size": 31, "alpha": 0.88},
                ],
            },
        ],
    )

    # 2. 24秒・森の清流×小川環境音（6万再生ヒット完全踏襲・冒頭字幕のみ版）
    build_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "eyecare_stream_24s_pure.mp4"),
        duration=24.0,
        start_offset=2.0,
        audio_path=swale_audio,
        audio_volume=0.35,
        crop_filter=stream_crop,
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.6,
                "lines": [
                    {"text": "今日も画面を見続けた目へ。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "今は、水の流れを眺めるだけ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
        ],
    )

    # 3. 18秒・葉脈をたどる×控えめな小川音（ソフト誘導あり版）
    build_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "eyecare_leaves_18s_shop_and_lp.mp4"),
        duration=18.0,
        start_offset=0.0,
        audio_path=swale_audio,
        audio_volume=0.22,
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "目が疲れている夜は、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "葉脈をゆっくりたどってみる。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "一本だけ、先まで見たら", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "ふっと視線をゆるめる。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 13.5s は無字幕
            {
                "start": 13.5,
                "end": 18.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "見終えたら、光を遮って", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "目を休める時間へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※使っているシルクのアイマスクはリンクへ", "y": 548, "size": 31, "alpha": 0.85},
                ],
            },
        ],
    )

    # 4. 18秒・葉脈をたどる（完全無音・純粋マインドフルネス版）
    build_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "eyecare_leaves_18s_pure_silent.mp4"),
        duration=18.0,
        start_offset=0.0,
        audio_path=None,
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "目が疲れている夜は、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "葉脈をゆっくりたどってみる。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "一本だけ、先まで見たら", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "ふっと視線をゆるめる。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            {
                "start": 13.8,
                "end": 18.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "このまま画面を閉じて、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "目を休める夜へ。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
        ],
    )
    print("All 4 videos rendered successfully!")
