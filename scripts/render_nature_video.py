import subprocess
import math
import sys
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1920
FPS = 30
TOTAL_SECONDS = 65.0
TOTAL_FRAMES = int(FPS * TOTAL_SECONDS)

FONT_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
font_header = ImageFont.truetype(FONT_PATH, 32)
font_title = ImageFont.truetype(FONT_PATH, 54)
font_sub = ImageFont.truetype(FONT_PATH, 42)
font_circle = ImageFont.truetype(FONT_PATH, 36)
font_small = ImageFont.truetype(FONT_PATH, 28)

INPUT_BG = "/tmp/rain_bg_65s.mp4"
AUDIO_FILE = "output/pure_rain_65s.wav"
OUTPUT_MP4 = "output/1min_mindful_nature_rain.mp4"

print(f"Compositing nature video with breathing guide: {TOTAL_FRAMES} frames...")

# 背景動画のデコードパイプ
in_pipe = subprocess.Popen([
    "ffmpeg", "-i", INPUT_BG,
    "-f", "rawvideo",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-"
], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

# 最終MP4のエンコードパイプ (動画 + 本物の雨音)
out_pipe = subprocess.Popen([
    "ffmpeg", "-y",
    "-f", "rawvideo",
    "-vcodec", "rawvideo",
    "-s", f"{WIDTH}x{HEIGHT}",
    "-pix_fmt", "rgb24",
    "-r", str(FPS),
    "-i", "-",
    "-i", AUDIO_FILE,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "faster",
    "-crf", "22",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    OUTPUT_MP4
], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

cx, cy = 540, 820
cycle_time = 16.0
frame_bytes = WIDTH * HEIGHT * 3

for f in range(TOTAL_FRAMES):
    raw_frame = in_pipe.stdout.read(frame_bytes)
    if not raw_frame or len(raw_frame) < frame_bytes:
        break
        
    t = f / FPS
    
    # 実写動画フレームを読み込み
    img = Image.frombytes("RGB", (WIDTH, HEIGHT), raw_frame)
    draw = ImageDraw.Draw(img, "RGBA")
    
    # ヘッダー (半透明の優しい白)
    header_text = "1分マインドフルネス"
    bbox_h = draw.textbbox((0, 0), header_text, font=font_header)
    hw = bbox_h[2] - bbox_h[0]
    draw.text(((WIDTH - hw) // 2, 220), header_text, fill=(200, 205, 215, 180), font=font_header)
    
    # 呼吸サークル計算
    r = 100
    circle_text = "1分"
    
    if 7.0 <= t < 55.0:
        rel_t = (t - 7.0) % cycle_time
        if rel_t < 4.0:
            prog = rel_t / 4.0
            smooth = (1 - math.cos(prog * math.pi)) / 2
            r = 100 + smooth * 110
            circle_text = "すって"
        elif rel_t < 8.0:
            prog = (rel_t - 4.0) / 4.0
            r = 210 + math.sin(prog * math.pi * 2) * 2
            circle_text = "とめて"
        else:
            prog = (rel_t - 8.0) / 8.0
            smooth = (1 - math.cos(prog * math.pi)) / 2
            r = 210 - smooth * 110
            circle_text = "はいて"
    elif t >= 55.0:
        r = 100
        circle_text = "安眠"
        
    # 外側の半透明リング
    draw.ellipse((cx - 215, cy - 215, cx + 215, cy + 215), outline=(255, 255, 255, 50), width=2)
    
    # 呼吸サークル本体 (実写が透けて見える半透明ダークブルーの塗り + 繊細な白枠)
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(10, 15, 25, 160), outline=(230, 235, 250, 190), width=3)
    
    # サークル中央の文字
    bbox_c = draw.textbbox((0, 0), circle_text, font=font_circle)
    cw = bbox_c[2] - bbox_c[0]
    ch = bbox_c[3] - bbox_c[1]
    draw.text((cx - cw // 2, cy - ch // 2 - 2), circle_text, fill=(255, 255, 255, 230), font=font_circle)
    
    # 字幕テキスト
    lines = []
    if t < 3.5:
        lines = [("あたまの中が、うるさーい夜へ。", font_title, (255, 255, 255, 240))]
    elif t < 7.0:
        lines = [
            ("今夜は1分だけ、", font_title, (255, 255, 255, 240)),
            ("頭のおしゃべりを強制終了しよう。", font_sub, (220, 225, 235, 200))
        ]
    elif 7.0 <= t < 23.0:
        rel_t = t - 7.0
        if rel_t < 4.0:
            lines = [("鼻から、静かに息をすって……", font_title, (245, 245, 255, 230))]
        elif rel_t < 8.0:
            lines = [("息をとめて……", font_title, (235, 240, 250, 220))]
        else:
            lines = [("口から細く長ーく、吐き出して……", font_title, (230, 235, 245, 220))]
    elif 23.0 <= t < 39.0:
        rel_t = t - 23.0
        if rel_t < 4.0:
            lines = [("肩の力を抜いて、すって……", font_title, (245, 245, 255, 230))]
        elif rel_t < 8.0:
            lines = [("とめて……", font_title, (235, 240, 250, 220))]
        else:
            lines = [
                ("今日の反省も、", font_title, (240, 245, 255, 230)),
                ("全部息と一緒に吐き出して……", font_sub, (215, 220, 230, 200))
            ]
    elif 39.0 <= t < 55.0:
        rel_t = t - 39.0
        if rel_t < 4.0:
            lines = [("奥歯の噛み締めをほどいて、すって……", font_title, (245, 245, 255, 230))]
        elif rel_t < 8.0:
            lines = [("とめて……", font_title, (235, 240, 250, 220))]
        else:
            lines = [
                ("まぶたの重みを感じて、", font_title, (240, 245, 255, 230)),
                ("ゆっくり吐いて……", font_sub, (215, 220, 230, 200))
            ]
    elif t < 60.0:
        lines = [
            ("少し、頭の中が静かになったかな。", font_title, (250, 250, 255, 240)),
            ("ベッドに入ってからもできるように保存してね。", font_small, (200, 205, 215, 180))
        ]
    else:
        lines = [
            ("今夜は、おやすみなさい。", font_title, (255, 255, 255, 245)),
            ("@1min_mindful", font_header, (180, 185, 200, 180))
        ]
        
    start_y = 1240
    for text, font, color in lines:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        # テキストの背景に薄い黒シャドウを入れて視認性を確保
        draw.text(((WIDTH - w) // 2 + 1, start_y + 1), text, fill=(0, 0, 0, 180), font=font)
        draw.text(((WIDTH - w) // 2, start_y), text, fill=color, font=font)
        start_y += h + 24
        
    out_pipe.stdin.write(img.convert("RGB").tobytes())
    
    if f % 150 == 0:
        percent = int(f / TOTAL_FRAMES * 100)
        print(f"Progress: {percent}% ({f}/{TOTAL_FRAMES} frames)...")

in_pipe.stdout.close()
in_pipe.wait()
out_pipe.stdin.close()
out_pipe.wait()
print(f"Nature video complete: {OUTPUT_MP4}")
