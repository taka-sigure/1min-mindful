import os
from lib.video_common import (
    OUTPUT_DIR,
    build_video,
    resolve_asset_path,
)

# 互換エイリアス
build_safe_video = build_video


if __name__ == "__main__":
    stream_video = resolve_asset_path("stream_6918262.mp4", "/tmp/stream_6918262.mp4")
    leaves_video = resolve_asset_path("leaves_6186130.mp4", "/tmp/leaves_6186130.mp4")
    swale_audio = resolve_asset_path("Swale.ogg", "/tmp/Swale.ogg")

    # 1. 22秒・清流×目の休息（カートなし・プロフィール誘導版）
    build_safe_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "safe_lp_01_stream_eyecare_22s.mp4"),
        duration=22.0,
        start_offset=20.0,
        audio_path=swale_audio,
        audio_offset=2.0,
        audio_volume=0.32,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:1680:0,eq=brightness=-0.05:contrast=1.06:saturation=1.05",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "今日も画面を見続けた目へ。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "今は、水の揺れを眺めるだけ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "ピントを合わせるのをやめて、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "ぼんやり見送る22秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 16.2s は完全無字幕で目を休める時間
            {
                "start": 16.2,
                "end": 22.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "見終えたらスマホを置いて、", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "目元を温めて眠る夜へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※夜に使っている休息アイテムはプロフィールへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 2. 20秒・夜モード水面×湯船と灯り（カートなし・プロフィール誘導版）
    build_safe_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "safe_lp_02_stream_bath_light_20s.mp4"),
        duration=20.0,
        start_offset=32.0,
        audio_path=swale_audio,
        audio_offset=6.0,
        audio_volume=0.30,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:720:0,eq=brightness=-0.08:contrast=1.08:saturation=1.02",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "考えごとが止まらない夜は、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "水の流れをぼんやり眺めてみる。", "y": 480, "size": 45, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "ひとつだけ、深く息を吐いて", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "頭のおしゃべりを静める20秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 14.5s は無字幕
            {
                "start": 14.5,
                "end": 20.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "部屋の白い電気を消して、", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "温かい湯船と小さな灯りで眠る夜も。", "y": 468, "size": 42, "alpha": 0.96},
                    {"text": "※愛用の入浴剤・間接照明はプロフィールへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 3. 18秒・木漏れ日の葉脈×奥歯と首肩のゆるみ（カートなし・プロフィール誘導版）
    build_safe_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "safe_lp_03_leaves_neck_incense_18s.mp4"),
        duration=18.0,
        start_offset=8.0,
        audio_path=swale_audio,
        audio_offset=4.0,
        audio_volume=0.22,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:1350:0,eq=brightness=-0.04:contrast=1.05:saturation=1.03",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "いま、奥歯や肩に", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "知らずに力が入っていない？", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "あごをゆるめて、肩を落として、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "ただ緑の揺れを眺める18秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 13.0s は無字幕
            {
                "start": 13.0,
                "end": 18.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "お香の香りと、首元に馴染む枕で", "y": 390, "size": 43, "alpha": 0.96},
                    {"text": "深く呼吸できる夜へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※使っているお香・睡眠用タオル枕はプロフィールへ", "y": 548, "size": 29, "alpha": 0.88},
                ],
            },
        ],
    )

    print("All 3 safe profile-funnel videos rendered successfully!")
