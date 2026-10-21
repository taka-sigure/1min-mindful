import os
from lib.video_common import (
    OUTPUT_DIR,
    build_video,
    resolve_asset_path,
)

# 互換エイリアス
build_custom_video = build_video


if __name__ == "__main__":
    stream_video = resolve_asset_path("stream_6918262.mp4", "/tmp/stream_6918262.mp4")
    leaves_video = resolve_asset_path("leaves_6186130.mp4", "/tmp/leaves_6186130.mp4")
    swale_audio = resolve_asset_path("Swale.ogg", "/tmp/Swale.ogg")

    # 3本目: 水面波紋アンビエントライト＆間接照明（22秒）
    # Showcase: 水面波紋をイメージしたアンビエントライト (1734226398019290470 / 2,451円) + ガラス製アロマキャンドル (990円)
    build_custom_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "mindful_03_water_ripple_light_22s.mp4"),
        duration=22.0,
        start_offset=4.5,
        audio_path=swale_audio,
        audio_offset=3.0,
        audio_volume=0.30,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:1180:0,eq=brightness=-0.08:contrast=1.08:saturation=0.96,colorbalance=rs=0.06:gs=0.01:bs=-0.06",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "強い明かりで目が冴えた夜へ。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "今は、水のゆらぎを眺めるだけ。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "天井の電気をひとつ消して、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "水面の光をぼんやり見送る22秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            {
                "start": 16.2,
                "end": 22.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "寝る前は、水面のように揺れる", "y": 390, "size": 44, "alpha": 0.96},
                    {"text": "小さな間接照明だけで過ごす夜も。", "y": 468, "size": 42, "alpha": 0.96},
                    {"text": "※水面波紋のナイトライトは商品リンクへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 4本目: 深い目の休息 × NIPLUX アイウォーマー＆ホットアイマスク（24秒）
    # Showcase: NIPLUX EYE RELAX S (1732130154323478208 / 9,801円) + nerugoo (4,480円) + 遮光アイマスク (1,680円)
    build_custom_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "mindful_04_deep_eyewarmer_24s.mp4"),
        duration=24.0,
        start_offset=0.5,
        audio_path=swale_audio,
        audio_offset=5.5,
        audio_volume=0.32,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:420:0,eq=brightness=-0.05:contrast=1.07:saturation=1.08",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "目の奥がずんと重い日の夜に。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "ただ、森の緑と水を眺める24秒。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "まばたきをゆっくりにして、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "眉間の力をそっと抜いてみる。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            {
                "start": 18.0,
                "end": 24.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "見終えたら、目元をじんわり温める", "y": 390, "size": 42, "alpha": 0.96},
                    {"text": "アイウォーマーで深く休む夜へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※NIPLUX 温熱アイウォーマーはリンクへ", "y": 548, "size": 30, "alpha": 0.88},
                ],
            },
        ],
    )

    # 5本目: 首・肩の力を抜く呼吸 × 今治睡眠用タオル枕＆無重力ジェル枕（20秒）
    # Showcase: 今治睡眠用タオル2 枕 (1732322235734984529 / 6,600円) + 無重力ジェル枕 (1731596104749516239 / 5,778円)
    build_custom_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "mindful_05_neck_shoulder_pillow_20s.mp4"),
        duration=20.0,
        start_offset=9.5,
        audio_path=swale_audio,
        audio_offset=8.0,
        audio_volume=0.24,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:220:0,eq=brightness=-0.04:contrast=1.05:saturation=1.02",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "寝ても首や肩がこわばる夜に。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "一度だけ、肩をすとんと落とす20秒。", "y": 480, "size": 44, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "息を長く吐きながら、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "後頭部の重さを手放してみる。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            {
                "start": 14.2,
                "end": 20.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "今夜は、首の高さにやさしく馴染む", "y": 390, "size": 42, "alpha": 0.96},
                    {"text": "タオル枕やジェル枕で眠る夜へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※今治睡眠用タオル枕・無重力枕はリンクへ", "y": 548, "size": 29, "alpha": 0.88},
                ],
            },
        ],
    )

    # 6本目: 気持ちを切り替える香り × お香（三大香木・穏）＆真鍮お香立て（20秒）
    # Showcase: 三大香木 (1736151959545546595 / 1,700円) + 穏～ON～ (1736151959476995939 / 2,200円) + 真鍮ガラス瓢箪お香立て (1734621162131982154 / 1,489円)
    build_custom_video(
        input_video=leaves_video,
        output_mp4=os.path.join(OUTPUT_DIR, "mindful_06_incense_aroma_20s.mp4"),
        duration=20.0,
        start_offset=5.0,
        audio_path=swale_audio,
        audio_offset=1.5,
        audio_volume=0.22,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:2050:0,eq=brightness=-0.06:contrast=1.06:saturation=0.95,colorbalance=rs=0.05:gs=0.02:bs=-0.04",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "考えごとが止まらない夜は、", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "葉の揺れをぼんやり眺めてみる。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "仕事や画面の時間を終えて、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "夜の静けさに切り替える20秒。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            {
                "start": 14.2,
                "end": 20.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "見終えたら、お香をひとすじ焚いて", "y": 390, "size": 42, "alpha": 0.96},
                    {"text": "香りとともに深く息をつく夜へ。", "y": 468, "size": 44, "alpha": 0.96},
                    {"text": "※三大香木・ラベンダーのお香とお香立てはリンクへ", "y": 548, "size": 28, "alpha": 0.88},
                ],
            },
        ],
    )

    # 7本目: 湯船でゆるむ夜 × 国産エプソムソルト＆バスタイム（22秒）
    # Showcase: 国産 エプソムソルト 3kg (1732385911955818451 / 1,980円) + ガラス製アロマキャンドル (990円)
    build_custom_video(
        input_video=stream_video,
        output_mp4=os.path.join(OUTPUT_DIR, "mindful_07_epsom_salt_bath_22s.mp4"),
        duration=22.0,
        start_offset=3.2,
        audio_path=swale_audio,
        audio_offset=6.8,
        audio_volume=0.34,
        crop_filter="scale=-2:1920:flags=lanczos,crop=1080:1920:1560:0,eq=brightness=-0.05:contrast=1.06:saturation=1.04,colorbalance=rs=0.04:gs=0.02:bs=0.01",
        cards=[
            {
                "start": 0.0,
                "end": 3.8,
                "fade_in": 0.0,
                "fade_out": 0.5,
                "lines": [
                    {"text": "体の芯まで疲れが残る夜に。", "y": 400, "size": 46, "alpha": 0.98},
                    {"text": "今は、水の音だけを聴く22秒。", "y": 480, "size": 46, "alpha": 0.98},
                ],
            },
            {
                "start": 4.2,
                "end": 7.8,
                "fade_in": 0.4,
                "fade_out": 0.5,
                "lines": [
                    {"text": "呼吸をひとつ深くして、", "y": 400, "size": 44, "alpha": 0.96},
                    {"text": "今日一日の緊張をほどいていく。", "y": 480, "size": 44, "alpha": 0.96},
                ],
            },
            {
                "start": 16.2,
                "end": 22.0,
                "fade_in": 0.5,
                "fade_out": 0.4,
                "lines": [
                    {"text": "スマホを置いたら、エプソムソルトの", "y": 390, "size": 42, "alpha": 0.96},
                    {"text": "温かい湯船でゆっくり温まる夜も。", "y": 468, "size": 43, "alpha": 0.96},
                    {"text": "※国産エプソムソルト・キャンドルはリンクへ", "y": 548, "size": 29, "alpha": 0.88},
                ],
            },
        ],
    )
    print("All 5 additional showcase videos rendered successfully!")
