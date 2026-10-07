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

AUDIO_FILE = "output/night1_audio.wav"
OUTPUT_MP4 = "output/1min_mindful_night1.mp4"

print(f"Starting video rendering: {TOTAL_FRAMES} frames ({TOTAL_SECONDS}s at {FPS}fps)...")

ffmpeg_cmd = [
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
]

proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)

# 背景キャッシュ用画像
base_bg = Image.new("RGB", (WIDTH, HEIGHT), (15, 17, 21))
draw_base = ImageDraw.Draw(base_bg)
header_text = "1分マインドフルネス"
bbox_h = draw_base.textbbox((0, 0), header_text, font=font_header)
hw = bbox_h[2] - bbox_h[0]
draw_base.text(((WIDTH - hw) // 2, 220), header_text, fill=(110, 115, 128), font=font_header)

cx, cy = 540, 820
cycle_time = 16.0

for f in range(TOTAL_FRAMES):
    t = f / FPS
    
    img = base_bg.copy()
    draw = ImageDraw.Draw(img)
    
    # 呼吸サークル計算
    r = 100
    circle_text = "1分"
    
    if 7.0 <= t < 55.0:
        rel_t = (t - 7.0) % cycle_time
        if rel_t < 4.0:
            # 4秒吸う (100 -> 210)
            prog = rel_t / 4.0
            smooth = (1 - math.cos(prog * math.pi)) / 2
            r = 100 + smooth * 110
            circle_text = "すって"
        elif rel_t < 8.0:
            # 4秒止める (210)
            prog = (rel_t - 4.0) / 4.0
            r = 210 + math.sin(prog * math.pi * 2) * 2
            circle_text = "とめて"
        else:
            # 8秒吐く (210 -> 100)
            prog = (rel_t - 8.0) / 8.0
            smooth = (1 - math.cos(prog * math.pi)) / 2
            r = 210 - smooth * 110
            circle_text = "はいて"
    elif t >= 55.0:
        r = 100
        circle_text = "安眠"
        
    # 外側の薄いリング
    draw.ellipse((cx - 215, cy - 215, cx + 215, cy + 215), outline=(35, 38, 48), width=2)
    
    # 呼吸サークル本体
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(26, 30, 42), outline=(78, 88, 120), width=3)
    
    # サークル中央の文字
    bbox_c = draw.textbbox((0, 0), circle_text, font=font_circle)
    cw = bbox_c[2] - bbox_c[0]
    ch = bbox_c[3] - bbox_c[1]
    draw.text((cx - cw // 2, cy - ch // 2 - 2), circle_text, fill=(210, 218, 235), font=font_circle)
    
    # 字幕テキスト
    lines = []
    if t < 3.5:
        lines = [("あたまの中が、うるさーい夜へ。", font_title, (240, 240, 245))]
    elif t < 7.0:
        lines = [
            ("今夜は1分だけ、", font_title, (240, 240, 245)),
            ("頭のおしゃべりを強制終了しよう。", font_sub, (180, 185, 198))
        ]
    elif 7.0 <= t < 23.0:
        rel_t = t - 7.0
        if rel_t < 4.0:
            lines = [("鼻から、静かに息をすって……", font_title, (230, 235, 245))]
        elif rel_t < 8.0:
            lines = [("息をとめて……", font_title, (210, 218, 235))]
        else:
            lines = [("口から細く長ーく、吐き出して……", font_title, (200, 205, 220))]
    elif 23.0 <= t < 39.0:
        rel_t = t - 23.0
        if rel_t < 4.0:
            lines = [("肩の力を抜いて、すって……", font_title, (230, 235, 245))]
        elif rel_t < 8.0:
            lines = [("とめて……", font_title, (210, 218, 235))]
        else:
            lines = [
                ("今日の反省も、", font_title, (220, 225, 235)),
                ("全部息と一緒に吐き出して……", font_sub, (180, 185, 198))
            ]
    elif 39.0 <= t < 55.0:
        rel_t = t - 39.0
        if rel_t < 4.0:
            lines = [("奥歯の噛み締めをほどいて、すって……", font_title, (230, 235, 245))]
        elif rel_t < 8.0:
            lines = [("とめて……", font_title, (210, 218, 235))]
        else:
            lines = [
                ("まぶたの重みを感じて、", font_title, (220, 225, 235)),
                ("ゆっくり吐いて……", font_sub, (180, 185, 198))
            ]
    elif t < 60.0:
        lines = [
            ("少し、頭の中が静かになったかな。", font_title, (235, 235, 242)),
            ("ベッドに入ってからもできるように保存してね。", font_small, (150, 155, 170))
        ]
    else:
        lines = [
            ("今夜は、おやすみなさい。", font_title, (240, 240, 245)),
            ("@1min_mindful", font_header, (120, 125, 140))
        ]
        
    start_y = 1240
    for text, font, color in lines:
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        draw.text(((WIDTH - w) // 2, start_y), text, fill=color, font=font)
        start_y += h + 24
        
    proc.stdin.write(img.tobytes())
    
    if f % 150 == 0:
        percent = int(f / TOTAL_FRAMES * 100)
        print(f"Progress: {percent}% ({f}/{TOTAL_FRAMES} frames rendered)...")

proc.stdin.close()
proc.wait()
print(f"Render complete! Generated: {OUTPUT_MP4}")
