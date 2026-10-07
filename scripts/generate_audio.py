import os
import wave
import struct
import math
import subprocess

SAMPLE_RATE = 44100
TOTAL_DURATION = 65.0
TOTAL_SAMPLES = int(SAMPLE_RATE * TOTAL_DURATION)

# 1. 録音するセリフと開始秒数
VOICE_SEGMENTS = [
    (0.8, "あたまの中が、うるさーい夜へ。"),
    (3.5, "今夜は1分だけ、頭のおしゃべりを強制終了しよう。"),
    (7.5, "鼻から、静かに息をすって。"),
    (11.5, "息をとめて。"),
    (15.5, "口から細く長ーく、吐き出して。"),
    (23.5, "肩の力を抜いて、すって。"),
    (27.5, "とめて。"),
    (31.5, "今日の反省も、全部息と一緒に吐き出して。"),
    (39.5, "奥歯の噛み締めをほどいて、すって。"),
    (43.5, "とめて。"),
    (47.5, "まぶたの重みを感じて、ゆっくり吐いて。"),
    (56.0, "少し、頭の中が静かになったかな。"),
    (60.0, "今夜は、おやすみなさい。"),
]

os.makedirs("/tmp/mindful_audio", exist_ok=True)

# 音声バッファ（ステレオ、左右チャンネル）
left_channel = [0.0] * TOTAL_SAMPLES
right_channel = [0.0] * TOTAL_SAMPLES

# 2. 環境音（432Hz + 216Hz の心地よいアンビエントドローン ＋ 柔らかなピンクノイズ風の雨音）を生成
print("Synthesizing ambient background sound...")
import random
random.seed(42)

for i in range(TOTAL_SAMPLES):
    t = i / SAMPLE_RATE
    # 穏やかなフェードイン(最初の2秒)とフェードアウト(最後の3秒)
    env = 1.0
    if t < 2.0:
        env = t / 2.0
    elif t > 62.0:
        env = (65.0 - t) / 3.0

    # 432Hz / 216Hz の微細なうなり（バイノーラル・ビート風: 左432Hz, 右436Hzで4Hzのシータ波誘導）
    tone_l = math.sin(2 * math.pi * 216 * t) * 0.04 + math.sin(2 * math.pi * 432 * t) * 0.02
    tone_r = math.sin(2 * math.pi * 216 * t) * 0.04 + math.sin(2 * math.pi * 436 * t) * 0.02
    
    # 穏やかなホワイトノイズ（雨音風に低周波でゆらぎ）
    noise = (random.random() * 2 - 1) * 0.015
    
    left_channel[i] = (tone_l + noise) * env
    right_channel[i] = (tone_r + noise) * env

# 3. macOS say コマンドで静かな日本語音声を生成し、タイムラインにミックス
print("Generating voiceover segments...")
for idx, (start_sec, text) in enumerate(VOICE_SEGMENTS):
    aiff_path = f"/tmp/mindful_audio/seg_{idx}.aiff"
    wav_path = f"/tmp/mindful_audio/seg_{idx}.wav"
    
    # say コマンドで落ち着いたトーン(レート115)で発声
    subprocess.run(["say", "-v", "Kyoko", "-r", "115", "-o", aiff_path, text], check=True)
    # ffmpeg で 44.1kHz 16bit PCM WAV に変換
    subprocess.run(["ffmpeg", "-y", "-i", aiff_path, "-ar", str(SAMPLE_RATE), "-ac", "1", wav_path], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    # WAVを読み込んでバッファに加算
    with wave.open(wav_path, "r") as wf:
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)
        samples = struct.unpack(f"<{n_frames}h", raw)
        
        start_sample = int(start_sec * SAMPLE_RATE)
        for s_idx, val in enumerate(samples):
            target_idx = start_sample + s_idx
            if target_idx < TOTAL_SAMPLES:
                # 声の音量を程よくミックス (0.8)
                norm_val = (val / 32768.0) * 0.85
                left_channel[target_idx] += norm_val
                right_channel[target_idx] += norm_val

# 4. クリッピング防止と16bit整数変換
print("Mastering final audio...")
out_wav_path = "output/night1_audio.wav"
with wave.open(out_wav_path, "w") as out_wf:
    out_wf.setnchannels(2)
    out_wf.setsampwidth(2)
    out_wf.setframerate(SAMPLE_RATE)
    
    out_frames = bytearray()
    for i in range(TOTAL_SAMPLES):
        l = max(-1.0, min(1.0, left_channel[i]))
        r = max(-1.0, min(1.0, right_channel[i]))
        
        l_int = int(l * 32767)
        r_int = int(r * 32767)
        
        out_frames.extend(struct.pack("<hh", l_int, r_int))
        
    out_wf.writeframes(out_frames)

print(f"Successfully created: {out_wav_path}")
