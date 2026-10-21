import os
from lib.video_common import (
    OUTPUT_DIR,
    TMP_DIR,
    build_video,
    render_subtitle_png,
    resolve_asset_path,
)

__all__ = ["OUTPUT_DIR", "TMP_DIR", "render_subtitle_png", "build_video"]


if __name__ == "__main__":
    stream_video = resolve_asset_path("stream_6918262.mp4", "/tmp/stream_6918262.mp4")
    leaves_video = resolve_asset_path("leaves_6186130.mp4", "/tmp/leaves_6186130.mp4")
    swale_audio = resolve_asset_path("Swale.ogg", "/tmp/Swale.ogg")

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

    # 5. 18秒・葉脈をたどる×夜のアロマキャンドル（TikTok Shopショーケース商品タグ＆LP両対応版）
    build_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "eyecare_leaves_candle_18s_tiktok_shop.mp4"),
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
            # 7.8s ~ 13.2s は無字幕
            {
                "start": 13.2,
                "end": 18.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "見終えたら明かりを落として、", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "キャンドルの灯りで目を休める夜へ。", "y": 468, "size": 42, "alpha": 0.96},
                    {"text": "※ガラス製アロマキャンドル・アイマスクはリンクへ", "y": 548, "size": 29, "alpha": 0.88},
                ],
            },
        ],
    )
    print("All 5 videos rendered successfully!")
