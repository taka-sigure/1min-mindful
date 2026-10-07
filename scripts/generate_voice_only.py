import wave
import struct
import subprocess
import os

SAMPLE_RATE = 44100
TOTAL_DURATION = 65.0
TOTAL_SAMPLES = int(SAMPLE_RATE * TOTAL_DURATION)

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

# 純粋な声のみのトラック
voice_buf = [0.0] * TOTAL_SAMPLES

for idx, (start_sec, text) in enumerate(VOICE_SEGMENTS):
    aiff_path = f"/tmp/mindful_audio/seg_{idx}.aiff"
    wav_path = f"/tmp/mindful_audio/seg_{idx}.wav"
    
    with wave.open(wav_path, "r") as wf:
        n_frames = wf.getnframes()
        raw = wf.readframes(n_frames)
        samples = struct.unpack(f"<{n_frames}h", raw)
        
        start_sample = int(start_sec * SAMPLE_RATE)
        for s_idx, val in enumerate(samples):
            target_idx = start_sample + s_idx
            if target_idx < TOTAL_SAMPLES:
                # 声を自然な音量(0.7)で配置
                voice_buf[target_idx] += (val / 32768.0) * 0.75

out_voice_path = "output/pure_voice_only.wav"
with wave.open(out_voice_path, "w") as out_wf:
    out_wf.setnchannels(1)
    out_wf.setsampwidth(2)
    out_wf.setframerate(SAMPLE_RATE)
    
    out_frames = bytearray()
    for i in range(TOTAL_SAMPLES):
        v = max(-1.0, min(1.0, voice_buf[i]))
        v_int = int(v * 32767)
        out_frames.extend(struct.pack("<h", v_int))
        
    out_wf.writeframes(out_frames)

print("Generated: output/pure_voice_only.wav")
