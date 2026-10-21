import os
from lib.video_common import (
    OUTPUT_DIR,
    build_video,
    resolve_asset_path,
)


if __name__ == "__main__":
    stream_video = resolve_asset_path("stream_6918262.mp4", "/tmp/stream_6918262.mp4")
    leaves_video = resolve_asset_path("leaves_6186130.mp4", "/tmp/leaves_6186130.mp4")
    swale_audio = resolve_asset_path("Swale.ogg", "/tmp/Swale.ogg")

    # 1. nerugoo 充電式ホットアイマスク / NIPLUX EYE RELAX S 用 (20秒・清流別アングル)
    build_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "shop_01_nerugoo_hot_eyemask_20s.mp4"),
        duration=20.0,
        start_offset=28.0,
        audio_path=swale_audio,
        audio_volume=0.32,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:950:0,eq=brightness=-0.05:contrast=1.06:saturation=1.05",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "細かい文字を追い続けた目へ。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "今は、水の揺れを眺めるだけ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "目の奥の力みをほどいて、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "ぼんやり流し見る20秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 14.5s は無字幕で目を休める時間
            {
                "start": 14.5,
                "end": 20.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "見終えたらスマホを置いて、", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "じんわり温かい目元で眠る夜へ。", "y": 468, "size": 43, "alpha": 0.96},
                    {"text": "※充電式ホットアイマスクは画面下の商品リンクへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 2. 国産エプソムソルト（無添加入浴剤）用 (22秒・清流ゆったりアングル)
    build_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "shop_02_epsom_salt_bath_22s.mp4"),
        duration=22.0,
        start_offset=36.0,
        audio_path=swale_audio,
        audio_volume=0.35,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:1450:0,eq=brightness=-0.04:contrast=1.05:saturation=1.08",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "考えごとが止まらない夜は、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "頭で解決しようとしなくていい。", "y": 480, "size": 45, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 8.0,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "水の流れを眺めながら、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "ひとつだけ、深く息を吐く。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 8.0s ~ 16.0s は無字幕
            {
                "start": 16.0,
                "end": 22.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "今夜はぬるめのお湯に浸かって、", "y": 390, "size": 43, "alpha": 0.96},
                    {"text": "体の芯からゆるめて眠る夜へ。", "y": 468, "size": 43, "alpha": 0.96},
                    {"text": "※使っている国産エプソムソルトは商品リンクへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 3. 水面波紋アンビエントライト（ベッドサイドナイトライト）用 (18秒・夜モード減光水紋)
    build_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "shop_03_water_wave_light_18s.mp4"),
        duration=18.0,
        start_offset=14.0,
        audio_path=swale_audio,
        audio_volume=0.25,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:450:0,eq=brightness=-0.12:contrast=1.10:saturation=1.04",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "部屋の白い明かりが、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "少しだけまぶしく感じる夜へ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "水面のゆらぎを眺めて、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "高ぶった神経を静める18秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 13.0s は無字幕
            {
                "start": 13.0,
                "end": 18.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "今夜は部屋の電気を消して、", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "水紋の灯りだけで眠る夜へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※水面波紋のナイトライトは画面下の商品リンクへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 4. 淡路島のお香 SOZO（三大香木 / 穏〜ON〜）＆真鍮お香立て用 (18秒・木漏れ日と揺れる葉)
    build_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "shop_04_sozo_incense_18s.mp4"),
        duration=18.0,
        start_offset=10.0,
        audio_path=swale_audio,
        audio_volume=0.20,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:600:0,eq=brightness=-0.04:contrast=1.04:saturation=1.02",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "今日の出来事が、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "まだ頭から離れない夜へ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "揺れる葉をぼんやり眺めて、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "仕事モードをそっと終わらせる。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 13.0s は無字幕
            {
                "start": 13.0,
                "end": 18.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "お香が燃え尽きるまでの間だけ、", "y": 390, "size": 43, "alpha": 0.96},
                    {"text": "何もしない夜時間を。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※香りのタイマー（淡路島のお香）は商品リンクへ", "y": 548, "size": 29, "alpha": 0.88},
                ],
            },
        ],
    )

    # 5. 無重力ジェル枕 / 今治睡眠用タオル2 用（食いしばり・首肩の緊張・頭の熱こもりケア 20秒）
    build_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "shop_05_pillow_neck_relax_20s.mp4"),
        duration=20.0,
        start_offset=6.0,
        audio_path=swale_audio,
        audio_volume=0.22,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:1750:0,eq=brightness=-0.05:contrast=1.05:saturation=1.04",
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
                    {"text": "ただ緑の揺れを眺める20秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.8s ~ 14.5s は無字幕
            {
                "start": 14.5,
                "end": 20.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "頭の熱と首の緊張を逃がして、", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "深く沈み込む眠りへ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※無重力ジェル枕・睡眠用タオルは商品リンクへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 6. 99.9%遮光 ふんわり快眠アイマスク 用（16秒・繊細な夜の光遮断）
    build_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "shop_06_blackout_eyemask_16s.mp4"),
        duration=16.0,
        start_offset=12.0,
        audio_path=swale_audio,
        audio_volume=0.18,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:1200:0,eq=brightness=-0.06:contrast=1.05:saturation=1.02",
        cards=[
            {
                "start": 0.0,
                "end": 3.6,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "わずかな光でも、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "目が冴えてしまう繊細な夜へ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.0,
                "end": 7.4,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "葉脈をひとつだけ目でたどって、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "まぶたの力を抜いていく。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            # 7.4s ~ 11.5s は無字幕
            {
                "start": 11.5,
                "end": 16.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "見終えたら、光をすべて遮って", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "朝まで静かな暗闇へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※ふんわり遮光アイマスクは画面下の商品リンクへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    print("All 6 showcase videos rendered successfully!")
