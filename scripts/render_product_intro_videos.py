import os
import json
import subprocess
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFilter
from lib.video_common import ASSETS_DIR, OUTPUT_DIR as ROOT_OUTPUT_DIR, TMP_DIR as ROOT_TMP_DIR, resolve_asset_path

WIDTH = 1080
HEIGHT = 1920
FPS = 30
DURATION = 20.0

OUTPUT_DIR = os.path.join(ROOT_OUTPUT_DIR, "product_intro_videos")
TMP_DIR = os.path.join(ROOT_TMP_DIR, "product_intro_build_v6")
GALLERY_BASE = resolve_asset_path("gallery", "/tmp/shop_product_images/gallery")

# TikTok Feed UI Safe Zone Center X (leaves x=875..1080 clear for Avatar/Heart/Comment/Bookmark/Share icons)
SAFE_CX = 485

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)


def render_appkit_text_png(png_path: str, width: int, height: int, lines: list[dict]):
    """
    Render crisp HiraginoSans-W6 / W3 typography with NSShadow to a transparent PNG via macOS JXA AppKit.
    Each item in lines:
      {"text": str, "y": int, "size": int, "weight": "W6"|"W3", "color": [r,g,b,a], "cx": Optional[int], "max_w": Optional[int]}
    """
    lines_json = json.dumps(lines, ensure_ascii=False)
    jxa_script = f"""
ObjC.import("AppKit");
const width = {width}, height = {height};
const rep = $.NSBitmapImageRep.alloc.initWithBitmapDataPlanesPixelsWidePixelsHighBitsPerSampleSamplesPerPixelHasAlphaIsPlanarColorSpaceNameBytesPerRowBitsPerPixel(
  null, width, height, 8, 4, true, false, $.NSDeviceRGBColorSpace, 0, 0
);
const ctx = $.NSGraphicsContext.graphicsContextWithBitmapImageRep(rep);
$.NSGraphicsContext.setCurrentContext(ctx);

$.NSColor.clearColor.set;
$.NSRectFill($.NSMakeRect(0, 0, width, height));

const shadow = $.NSShadow.alloc.init;
shadow.setShadowOffset($.NSMakeSize(0, -2));
shadow.setShadowBlurRadius(10.0);
shadow.setShadowColor($.NSColor.colorWithCalibratedWhiteAlpha(0.0, 0.85));

const lines = {lines_json};
for (const item of lines) {{
  const fontName = item.weight === "W3" ? "HiraginoSans-W3" : "HiraginoSans-W6";
  const c = item.color || [1.0, 1.0, 1.0, 0.98];
  const maxW = item.max_w || (width - 80);
  const cx = (item.cx !== undefined && item.cx !== null) ? item.cx : Math.round(width / 2);
  let fontSize = item.size || 30;
  let attrs = null;
  let nsStr = $.NSString.stringWithString(item.text);
  let sz = null;

  while (fontSize >= 14) {{
    const font = $.NSFont.fontWithNameSize(fontName, fontSize);
    attrs = $.NSMutableDictionary.alloc.init;
    attrs.setObjectForKey(font, $.NSFontAttributeName);
    attrs.setObjectForKey($.NSColor.colorWithCalibratedRedGreenBlueAlpha(c[0], c[1], c[2], c[3]), $.NSForegroundColorAttributeName);
    attrs.setObjectForKey(shadow, $.NSShadowAttributeName);
    sz = nsStr.sizeWithAttributes(attrs);
    if (sz.width <= maxW) break;
    fontSize -= 1;
  }}

  const x = Math.round(cx - (sz.width / 2));
  const y = Math.round(height - item.y - (sz.height / 2));
  nsStr.drawAtPointWithAttributes($.NSMakePoint(x, y), attrs);
  nsStr.drawAtPointWithAttributes($.NSMakePoint(x, y), attrs);
}}

$.NSGraphicsContext.currentContext.flushGraphics;
const pngData = rep.representationUsingTypeProperties($.NSBitmapImageFileTypePNG, $.NSDictionary.dictionary);
pngData.writeToFileAtomically({json.dumps(png_path)}, true);
"""
    subprocess.run(["osascript", "-l", "JavaScript", "-e", jxa_script], check=True)


def create_studio_ambient_background(prod_img_path: str, theme_rgb: tuple[int, int, int]) -> Image.Image:
    """
    Create a dark, calm @1min_mindful studio ambient background (#111215 base + subtle product aura).
    Completely free of trees, leaves, or rivers.
    """
    src = Image.open(prod_img_path).convert("RGB")
    sw, sh = src.size
    target_ratio = WIDTH / HEIGHT
    if sw / sh > target_ratio:
        new_w = int(sh * target_ratio)
        left = (sw - new_w) // 2
        src = src.crop((left, 0, left + new_w, sh))
    else:
        new_h = int(sw / target_ratio)
        top = (sh - new_h) // 2
        src = src.crop((0, top, sw, top + new_h))

    bg = src.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=85))

    dark_overlay = Image.new("RGB", (WIDTH, HEIGHT), theme_rgb)
    bg = Image.blend(bg.point(lambda p: int(p * 0.28)), dark_overlay, 0.45)

    vignette = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    vdraw = ImageDraw.Draw(vignette)
    for y in range(HEIGHT):
        if y < 320:
            alpha = int(135 * (1.0 - y / 320.0))
        elif y > 1350:
            alpha = int(190 * ((y - 1350) / (HEIGHT - 1350)))
        else:
            alpha = 30
        vdraw.line([(0, y), (WIDTH, y)], fill=(8, 9, 12, alpha))

    bg_rgba = bg.convert("RGBA")
    bg_rgba.alpha_composite(vignette)
    return bg_rgba


def build_scene_frame_png(
    out_png: str,
    prod_img_path: str,
    theme_rgb: tuple[int, int, int],
    step_str: str,
    headline: str,
    subheadline: str,
    card_title: str,
    body_line1: str,
    body_line2: str,
    spec_line: str,
    show_footer_note: bool = False,
):
    canvas = create_studio_ambient_background(prod_img_path, theme_rgb)

    # 1. Top "1分マインドフルネス ｜ おすすめの夜アイテム" pill badge (y=252..302, well below Following | For You at y=145..220)
    ui_layer_2x = Image.new("RGBA", (WIDTH * 2, HEIGHT * 2), (0, 0, 0, 0))
    udraw = ImageDraw.Draw(ui_layer_2x)
    pill_w = 590
    pill_x1 = SAFE_CX - pill_w // 2
    pill_x2 = pill_x1 + pill_w
    udraw.rounded_rectangle(
        (pill_x1 * 2, 252 * 2, pill_x2 * 2, 302 * 2),
        radius=25 * 2,
        fill=(16, 18, 24, 215),
        outline=(255, 255, 255, 52),
        width=2,
    )

    # 2. Bottom Dark Frosted Info Card (x=95..875, y=1090..1375 — clear of right-side Heart/Comment icons at x=895+)
    card_w = 780
    bx1 = SAFE_CX - card_w // 2
    bx2 = bx1 + card_w
    udraw.rounded_rectangle(
        (bx1 * 2, 1090 * 2, bx2 * 2, 1375 * 2),
        radius=30 * 2,
        fill=(16, 18, 24, 224),
        outline=(255, 255, 255, 44),
        width=2,
    )
    ui_layer = ui_layer_2x.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    canvas.alpha_composite(ui_layer)

    # 3. Product Hero Photo (630x630 centered at SAFE_CX -> x=170..800, y=434..1064 — clear of Avatar icon at x=875+)
    card_size = 630
    card_x = SAFE_CX - card_size // 2
    card_y = 434
    radius = 38

    prod_raw = Image.open(prod_img_path).convert("RGBA")
    prod_square = prod_raw.resize((card_size, card_size), Image.Resampling.LANCZOS)

    mask_2x = Image.new("L", (card_size * 2, card_size * 2), 0)
    ImageDraw.Draw(mask_2x).rounded_rectangle(
        (0, 0, card_size * 2 - 1, card_size * 2 - 1), radius=radius * 2, fill=255
    )
    mask = mask_2x.resize((card_size, card_size), Image.Resampling.LANCZOS)

    shadow_pad = 50
    shadow_img = Image.new("RGBA", (card_size + shadow_pad * 2, card_size + shadow_pad * 2), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow_img)
    sdraw.rounded_rectangle(
        (shadow_pad, shadow_pad + 12, shadow_pad + card_size, shadow_pad + card_size + 12),
        radius=radius,
        fill=(0, 0, 0, 175),
    )
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=36))
    canvas.alpha_composite(shadow_img, (card_x - shadow_pad, card_y - shadow_pad))

    rounded_prod = Image.new("RGBA", (card_size, card_size), (0, 0, 0, 0))
    rounded_prod.paste(prod_square, (0, 0), mask)

    border_2x = Image.new("RGBA", (card_size * 2, card_size * 2), (0, 0, 0, 0))
    ImageDraw.Draw(border_2x).rounded_rectangle(
        (1, 1, card_size * 2 - 2, card_size * 2 - 2),
        radius=radius * 2,
        outline=(255, 255, 255, 70),
        width=3,
    )
    border = border_2x.resize((card_size, card_size), Image.Resampling.LANCZOS)
    rounded_prod.alpha_composite(border)
    canvas.alpha_composite(rounded_prod, (card_x, card_y))

    # 4. Render typography layer via JXA AppKit (centered around SAFE_CX with auto max_w fitting)
    txt_png = out_png + "_txt.png"
    badge_text = f"1分マインドフルネス ｜ おすすめの夜アイテム   {step_str}"
    footer_text = (
        "※商品の詳細は、画面左下のリンクからご覧いただけます"
        if show_footer_note
        else "@1min_mindful"
    )
    footer_col = [0.90, 0.92, 0.96, 0.90] if show_footer_note else [0.68, 0.72, 0.80, 0.68]

    render_appkit_text_png(
        txt_png,
        WIDTH,
        HEIGHT,
        [
            {"text": badge_text, "y": 277, "size": 19, "weight": "W6", "color": [0.93, 0.90, 0.82, 0.96], "cx": SAFE_CX, "max_w": 550},
            {"text": headline, "y": 348, "size": 34, "weight": "W6", "color": [1.0, 1.0, 1.0, 0.99], "cx": SAFE_CX, "max_w": 840},
            {"text": subheadline, "y": 398, "size": 22, "weight": "W3", "color": [0.84, 0.87, 0.93, 0.92], "cx": SAFE_CX, "max_w": 820},
            {"text": card_title, "y": 1136, "size": 28, "weight": "W6", "color": [1.0, 0.98, 0.93, 0.99], "cx": SAFE_CX, "max_w": 730},
            {"text": body_line1, "y": 1200, "size": 21, "weight": "W3", "color": [0.92, 0.94, 0.97, 0.96], "cx": SAFE_CX, "max_w": 730},
            {"text": body_line2, "y": 1244, "size": 21, "weight": "W3", "color": [0.92, 0.94, 0.97, 0.96], "cx": SAFE_CX, "max_w": 730},
            {"text": spec_line, "y": 1320, "size": 20, "weight": "W3", "color": [0.96, 0.88, 0.72, 0.95], "cx": SAFE_CX, "max_w": 730},
            {"text": footer_text, "y": 1422, "size": 21, "weight": "W3", "color": footer_col, "cx": SAFE_CX, "max_w": 760},
        ],
    )

    canvas.alpha_composite(Image.open(txt_png).convert("RGBA"))
    canvas.convert("RGB").save(out_png, "PNG")
    if os.path.exists(txt_png):
        os.remove(txt_png)


def render_single_product_video(spec: dict):
    vid_id = spec["id"]
    out_mp4 = os.path.join(OUTPUT_DIR, spec["out_name"])
    theme_rgb = spec["theme_rgb"]

    scene_pngs = []
    for idx, sc in enumerate(spec["scenes"]):
        p_png = os.path.join(TMP_DIR, f"{vid_id}_scene_{idx}.png")
        build_scene_frame_png(
            out_png=p_png,
            prod_img_path=sc["img"],
            theme_rgb=theme_rgb,
            step_str=f"{idx + 1} / 4",
            headline=sc["headline"],
            subheadline=sc["subheadline"],
            card_title=sc["card_title"],
            body_line1=sc["body_line1"],
            body_line2=sc["body_line2"],
            spec_line=sc["spec_line"],
            show_footer_note=(idx == 3),
        )
        scene_pngs.append(p_png)

    cmd = ["ffmpeg", "-y"]
    for p in scene_pngs:
        cmd.extend(["-i", p])
    cmd.extend(["-f", "lavfi", "-t", f"{DURATION:.2f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"])

    filter_parts = [
        "[0:v]loop=loop=168:size=1:start=0,fps=30,trim=duration=5.6,setpts=PTS-STARTPTS,format=yuv420p[s0]",
        "[1:v]loop=loop=168:size=1:start=0,fps=30,trim=duration=5.6,setpts=PTS-STARTPTS,format=yuv420p[s1]",
        "[2:v]loop=loop=168:size=1:start=0,fps=30,trim=duration=5.6,setpts=PTS-STARTPTS,format=yuv420p[s2]",
        "[3:v]loop=loop=168:size=1:start=0,fps=30,trim=duration=5.6,setpts=PTS-STARTPTS,format=yuv420p[s3]",
        "[s0][s1]xfade=transition=fade:duration=0.8:offset=4.8[x01]",
        "[x01][s2]xfade=transition=fade:duration=0.8:offset=9.6[x02]",
        "[x02][s3]xfade=transition=fade:duration=0.8:offset=14.4[x03]",
        "[x03]trim=duration=20.0,setpts=PTS-STARTPTS,format=yuv420p[vout]",
    ]

    cmd.extend([
        "-filter_complex", ";".join(filter_parts),
        "-map", "[vout]",
        "-map", "4:a",
        "-c:v", "h264_videotoolbox",
        "-b:v", "5500k",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-shortest",
        out_mp4,
    ])

    print(f"Rendering {out_mp4} ...")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    print(f"Done: {out_mp4}")
    return out_mp4


PRODUCTS = [
    {
        "id": "01_nerugoo",
        "out_name": "product_intro_01_nerugoo_eyemask.mp4",
        "theme_rgb": (42, 26, 48),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/01_1731783656634156051/gallery_04.jpg",
                "headline": "目を閉じても、目の奥が重たい夜に。",
                "subheadline": "nerugoo リバティ・ファブリックス 充電式ホットアイマスク",
                "card_title": "シルクのように滑らかな生地が、目元を包む",
                "body_line1": "英国リバティ社のタナローン素材を採用した限定モデル。",
                "body_line2": "スマホやPCでこわばった目元をじんわり解きほぐします。",
                "spec_line": "カラー：ベッツィイエロー / ベッツィブルー（2色展開）",
            },
            {
                "img": f"{GALLERY_BASE}/01_1731783656634156051/desc_01.jpg",
                "headline": "気分で選べる、2つのリバティ花柄。",
                "subheadline": "Betsy Yellow ＆ Betsy Blue",
                "card_title": "高温・中温・低温の3段階温度調整",
                "body_line1": "その日の目の疲れに合わせて、ワンタッチで温度変更。",
                "body_line2": "コードレス設計だから、どんな寝姿勢でも邪魔になりません。",
                "spec_line": "素材：オリジナルリバティ生地（タナローン素材）",
            },
            {
                "img": f"{GALLERY_BASE}/01_1731783656634156051/gallery_02.jpg",
                "headline": "途中で寝落ちしてしまっても、安心。",
                "subheadline": "くり返し使えて、毎晩清潔な肌ざわり",
                "card_title": "30分自動オフタイマー ＆ カバー手洗いOK",
                "body_line1": "約30分で自動的に電源が切れる安心設計。",
                "body_line2": "カバーは取り外して洗えるので、いつも清潔に使えます。",
                "spec_line": "充電：USB Type-C 充電式（専用ケーブル付属）",
            },
            {
                "img": f"{GALLERY_BASE}/01_1731783656634156051/gallery_01.jpg",
                "headline": "自分へのご褒美にも、ギフトにも。",
                "subheadline": "MONOQLO年間ベストバイ受賞・グッドデザイン賞受賞",
                "card_title": "nerugoo 充電式ホットアイマスク（ギフトBOX付）",
                "body_line1": "使い捨てない、毎晩の心地よいナイトルーティン。",
                "body_line2": "化粧箱入りで、大切な人へのプレゼントにも選ばれています。",
                "spec_line": "価格：4,480円（税込・送料無料） / メーカー1年保証付",
            },
        ],
    },
    {
        "id": "02_epsom_salt",
        "out_name": "product_intro_02_epsom_salt.mp4",
        "theme_rgb": (18, 36, 52),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/02_1732385911955818451/gallery_05.jpg",
                "headline": "手足が冷えて、なかなか寝つけない夜に。",
                "subheadline": "アースコンシャス 国産エプソムソルト（3kg / 30回分）",
                "card_title": "瀬戸内海のミネラルが、体の芯まで温める",
                "body_line1": "お風呂に入れるだけで、自宅のバスルームが極上スパに。",
                "body_line2": "湯上がりもポカポカと湯冷めしにくい体へ導きます。",
                "spec_line": "成分：国産最上級グレード 100%硫酸マグネシウム（瀬戸内産）",
            },
            {
                "img": f"{GALLERY_BASE}/02_1732385911955818451/gallery_07.jpg",
                "headline": "無香料・無着色で、毎日やさしいバスタイム。",
                "subheadline": "追い焚きOK・残り湯洗濯OK・赤ちゃんとの入浴にも",
                "card_title": "塩分ゼロだから、浴槽や風呂釜を傷めない",
                "body_line1": "「ソルト」という名前でも塩分は含まない純粋なミネラル結晶。",
                "body_line2": "お気に入りのアロマオイルを加えて楽しむこともできます。",
                "spec_line": "仕様：無香料・無着色・防腐剤無添加",
            },
            {
                "img": f"{GALLERY_BASE}/02_1732385911955818451/gallery_04.jpg",
                "headline": "たっぷり30回分、惜しみなく使える3kg。",
                "subheadline": "計量スプーン付き・保管しやすいチャック袋",
                "card_title": "付属スプーン5杯を、お湯に溶かすだけ",
                "body_line1": "150Lのお湯に約100g（付属スプーン5杯）が1回分の目安。",
                "body_line2": "毎日の入浴習慣として続けやすい大容量パックです。",
                "spec_line": "内容量：3kg（約30回分） / 専用計量スプーン付属",
            },
            {
                "img": f"{GALLERY_BASE}/02_1732385911955818451/gallery_01.jpg",
                "headline": "1回あたり約66円で始める、夜の温浴習慣。",
                "subheadline": "楽天・Amazonでも高評価のロングセラー入浴剤",
                "card_title": "アースコンシャス 国産エプソムソルト 3kg",
                "body_line1": "しっかり温まって汗をかき、ベッドに入る頃には自然な眠気へ。",
                "body_line2": "冷えや疲れが抜けにくい方のナイトルーティンに。",
                "spec_line": "価格：1,980円（税込・送料無料） / 1回あたり約66円",
            },
        ],
    },
    {
        "id": "03_water_wave_light",
        "out_name": "product_intro_03_water_wave_light.mp4",
        "theme_rgb": (38, 30, 20),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/03_1734226398019290470/gallery_03.jpg",
                "headline": "部屋の白い照明が、眩しすぎる夜に。",
                "subheadline": "水面波紋 アンビエントプロジェクターライト",
                "card_title": "天井や壁に、静かな水面がゆらめく間接照明",
                "body_line1": "クリスタル調シェードから広がる波紋のゆらぎが、",
                "body_line2": "スマホで冴えてしまった脳を穏やかにクールダウンします。",
                "spec_line": "デザイン：木目調ベース × クリスタル波紋シェード",
            },
            {
                "img": f"{GALLERY_BASE}/03_1734226398019290470/gallery_01.jpg",
                "headline": "その日の気分で選べる、16色の灯り。",
                "subheadline": "暖かなアンバーから、深いブルー・オーロラ色まで",
                "card_title": "リモコン付属で、ベッドの中から色・明るさ調整",
                "body_line1": "眠る前は落ち着いた暖色、リラックスタイムには幻想的な寒色など、",
                "body_line2": "布団に入ったままリモコンひとつで切り替えられます。",
                "spec_line": "機能：16色カラー切替・無段階調光・リモコン操作",
            },
            {
                "img": f"{GALLERY_BASE}/03_1734226398019290470/gallery_02.jpg",
                "headline": "ベッドサイドに置ける、手のひらサイズ。",
                "subheadline": "寝室・リビング・バスルームのリラックス空間に",
                "card_title": "USB給電対応・場所を取らないコンパクト設計",
                "body_line1": "枕元のサイドテーブルや棚の上にちょこんと置けるサイズ感。",
                "body_line2": "消灯前の30分を、ホテルのような癒しの空間に変えてくれます。",
                "spec_line": "電源：USB給電式 / タッチ操作＆リモコン両対応",
            },
            {
                "img": f"{GALLERY_BASE}/03_1734226398019290470/gallery_04.jpg",
                "headline": "いつもの寝室を、静かな癒しの空間へ。",
                "subheadline": "インテリアに馴染むナチュラルなデザイン",
                "card_title": "水面波紋 アンビエントプロジェクターライト",
                "body_line1": "点灯していない日中も、美しいオブジェとして部屋に馴染みます。",
                "body_line2": "夜の読書やストレッチ、眠りにつく前の静かな時間に。",
                "spec_line": "価格：2,451円（税込・送料無料）",
            },
        ],
    },
    {
        "id": "04_sozo_incense",
        "out_name": "product_intro_04_sozo_incense.mp4",
        "theme_rgb": (36, 26, 22),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/04_1736151959476995939/gallery_03.jpg",
                "headline": "頭のスイッチが、なかなか切れない夜へ。",
                "subheadline": "SOZO【お香】穏 〜ON〜（ラベンダー / ジャスミン）",
                "card_title": "お香の名産地・兵庫県淡路島で生まれた静かな香り",
                "body_line1": "心を鎮めるラベンダーと、気分をほぐすジャスミン。",
                "body_line2": "立ち上るひとすじの煙が、部屋の空気をすっと変えてくれます。",
                "spec_line": "生産地：兵庫県淡路島（日本製） / 素材：タブ粉・シナ粉・香料",
            },
            {
                "img": f"{GALLERY_BASE}/04_1736151959476995939/gallery_05.jpg",
                "headline": "心を鎮めるラベンダーと、気分をほぐすジャスミン。",
                "subheadline": "その日の気分で選べる2種の香りアソート",
                "card_title": "お香15本・マッチ・不燃性マットのオールインワン",
                "body_line1": "1箱にラベンダーとジャスミンの2種類が入っているので飽きずに楽しめます。",
                "body_line2": "専用マットとマッチ付きで、届いたその夜からすぐに焚くことができます。",
                "spec_line": "燃焼時間：1本あたり約10分（おやすみ前の習慣に最適）",
            },
            {
                "img": f"{GALLERY_BASE}/04_1736151959476995939/gallery_04.jpg",
                "headline": "強すぎない、天然木粉ベースのやさしい芳香。",
                "subheadline": "お香初心者や寝室でも使いやすい穏やかな香り立ち",
                "card_title": "煙が消えたあとも、心地よい残り香が続く",
                "body_line1": "ツンとした強さを抑えた、職人の調香による上品な香り。",
                "body_line2": "就寝前の読書タイムや、ストレッチのお供にぴったりです。",
                "spec_line": "セット内容：お香15本・マッチ1箱・不燃性マット1枚",
            },
            {
                "img": f"{GALLERY_BASE}/04_1736151959476995939/gallery_01.jpg",
                "headline": "1日の終わりに、香りで整えるナイトルーティン。",
                "subheadline": "現代のライフスタイルに馴染むモダンなパッケージ",
                "card_title": "SOZO お香「穏 〜ON〜」淡路島産インセンス",
                "body_line1": "お香初心者の方や、大切な方へのちょっとしたギフトにも好評。",
                "body_line2": "深呼吸したくなる香りで、穏やかな夜時間をつくります。",
                "spec_line": "価格：2,200円（税込・送料無料）",
            },
        ],
    },
    {
        "id": "05_imabari_pillow",
        "out_name": "product_intro_05_imabari_towel_pillow.mp4",
        "theme_rgb": (24, 34, 42),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/05_1732322235734984529/gallery_02.jpg",
                "headline": "どの枕を試しても、朝起きると首が重い方へ。",
                "subheadline": "今治睡眠用タオル2 ピローレスネックフィットタオル",
                "card_title": "純国産・今治タオルの綿100%が首のカーブを支える",
                "body_line1": "高さが合わない枕で首や肩がこる「枕難民」のために開発。",
                "body_line2": "もちもちの今治タオル生地が、頸椎の隙間を優しく埋めます。",
                "spec_line": "素材：綿100%（今治タオルブランド認定・純国産品質）",
            },
            {
                "img": f"{GALLERY_BASE}/05_1732322235734984529/gallery_06.jpg",
                "headline": "くるくる巻くだけで、自分にぴったりの高さに。",
                "subheadline": "その日の体調や寝姿勢に合わせてミリ単位で調整可能",
                "card_title": "仰向けでも横向きでも、理想のネックラインをキープ",
                "body_line1": "高めの枕が好きな方も、ほぼフラットで寝たい方も自由自在。",
                "body_line2": "ストレートネック対策や、首元の冷え対策にも活躍します。",
                "spec_line": "サイズ：約135×60cm / 高さ調整用専用ポール付属",
            },
            {
                "img": f"{GALLERY_BASE}/05_1732322235734984529/gallery_05.jpg",
                "headline": "自宅の洗濯機で、いつでも丸洗いできる清潔さ。",
                "subheadline": "タオルだから、洗って干すだけでいつもふかふか",
                "card_title": "一般的な枕では難しい「毎日の丸洗い」が簡単に",
                "body_line1": "寝汗や皮脂が気になったら、そのまま洗濯機で洗えてすぐ乾きます。",
                "body_line2": "肌が敏感な方や、清潔な寝具で気持ちよく眠りたい方に。",
                "spec_line": "お手入れ：家庭用洗濯機で丸洗いOK",
            },
            {
                "img": f"{GALLERY_BASE}/05_1732322235734984529/gallery_07.jpg",
                "headline": "今治タオルの優しさに包まれて眠る夜を。",
                "subheadline": "専用ポール付属・寝室に馴染む4色のニュアンスカラー",
                "card_title": "今治睡眠用タオル2（専用ポール付）",
                "body_line1": "累計販売数多数の人気シリーズ。ギフトとしても喜ばれています。",
                "body_line2": "首・肩に負担をかけない新しい睡眠習慣を始めませんか。",
                "spec_line": "価格：6,600円（税込・送料無料）",
            },
        ],
    },
    {
        "id": "06_blackout_eyemask",
        "out_name": "product_intro_06_blackout_eyemask.mp4",
        "theme_rgb": (18, 22, 38),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/06_1734626745675515314/gallery_06.jpg",
                "headline": "わずかな光で、夜中に目が覚めてしまう方へ。",
                "subheadline": "睡眠科医監修 99.9%遮光 ふんわり快眠アイマスク",
                "card_title": "鼻まわりの隙間まで優しく包み、光を99.9%カット",
                "body_line1": "カーテンの隙間光や充電ランプの光をしっかり遮断し、",
                "body_line2": "つけた瞬間から深い眠りのための暗闇を作ります。",
                "spec_line": "遮光性能：国内検査機関にて遮光率99.9%実証済み",
            },
            {
                "img": f"{GALLERY_BASE}/06_1734626745675515314/gallery_02.jpg",
                "headline": "つけていることを忘れる、ふんわり軽い肌ざわり。",
                "subheadline": "独自5層構造 ＆ 約25gの超軽量シルク調素材",
                "card_title": "目やまつ毛を圧迫しない、ソフトなフィット感",
                "body_line1": "中綿入りの柔らかなクッション構造で、長時間つけても快適。",
                "body_line2": "通気性と保湿性に優れた生地が、デリケートな目元を守ります。",
                "spec_line": "重量：約25g / 構造：ふんわり5層クッション構造",
            },
            {
                "img": f"{GALLERY_BASE}/06_1734626745675515314/gallery_05.jpg",
                "headline": "朝まで耳が痛くならない、幅広ソフトバンド。",
                "subheadline": "頭囲48〜100cmまで無段階調整・手洗いOK",
                "card_title": "寝返りを打ってもズレにくく、締め付け感ゼロへ",
                "body_line1": "耳にかけないバックストラップ方式で、横向き寝でも耳が痛くなりません。",
                "body_line2": "汚れが気になったら手洗いできるので、毎晩清潔に使えます。",
                "spec_line": "仕様：長さ調整可能ゴムバンド / 水洗い対応",
            },
            {
                "img": f"{GALLERY_BASE}/06_1734626745675515314/gallery_01.jpg",
                "headline": "手頃な価格で始める、質の高い睡眠環境づくり。",
                "subheadline": "睡眠科医監修・持ち運びに便利な収納ポーチ付き",
                "card_title": "睡眠科医監修 99.9%遮光 ふんわり快眠アイマスク",
                "body_line1": "自宅での就寝時はもちろん、飛行機や新幹線の移動・仮眠にも。",
                "body_line2": "選べる5つのカラーバリエーションをご用意しています。",
                "spec_line": "価格：1,680円（税込・送料無料） / 専用収納ポーチ付属",
            },
        ],
    },
    {
        "id": "07_niplux_eyerelax",
        "out_name": "product_intro_07_niplux_eyerelax.mp4",
        "theme_rgb": (42, 22, 26),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/07_1732130154323478208/gallery_04.jpg",
                "headline": "目の奥のこわばりを、指先感覚でほぐす夜に。",
                "subheadline": "NIPLUX EYE RELAX S アイウォーマー",
                "card_title": "温熱 × 加圧エアバッグで、目元をじっくり包み込む",
                "body_line1": "シリーズ累計200万台突破のNIPLUXから進化した最新モデル。",
                "body_line2": "人の指先のような心地よい加圧で、1日の目元疲れをケアします。",
                "spec_line": "機能：加圧エアバッグ × グラフェン温熱（2段階温度調節）",
            },
            {
                "img": f"{GALLERY_BASE}/07_1732130154323478208/gallery_07.jpg",
                "headline": "こめかみから目元まで、ググッと心地よい加圧。",
                "subheadline": "従来品より加圧力が127%アップしたマルチエアクッション",
                "card_title": "目元の輪郭にフィットする3D立体エアバッグ構造",
                "body_line1": "目のまわり全体を優しく、かつしっかりとプレス。",
                "body_line2": "アイホールにゆとりを持たせた設計で、眼球への圧迫感を抑えます。",
                "spec_line": "設計：アイホール構造 / 3段階加圧レベル調整",
            },
            {
                "img": f"{GALLERY_BASE}/07_1732130154323478208/gallery_06.jpg",
                "headline": "つけて約1分でじんわり温まる、速暖グラフェン。",
                "subheadline": "熱伝導性に優れたグラフェン素材で目元全体を均一に温める",
                "card_title": "約38℃〜42℃の心地よい温感が、深い休息へ導く",
                "body_line1": "スイッチを入れてすぐに温かさを感じられる速暖設計。",
                "body_line2": "おやすみ前の15分間、温かいタオルを乗せたような解放感に。",
                "spec_line": "タイマー：15分自動オフタイマー搭載（寝落ちしても安心）",
            },
            {
                "img": f"{GALLERY_BASE}/07_1732130154323478208/gallery_08.jpg",
                "headline": "静かな夜を邪魔しない、静音設計＆コードレス。",
                "subheadline": "二つ折りでコンパクト収納・お手入れ簡単なPUレザー",
                "card_title": "NIPLUX EYE RELAX S（USB Type-C充電式）",
                "body_line1": "約42.7dBの静音設計で、就寝前の静かな時間にもぴったり。",
                "body_line2": "自分へのご褒美ケアや、大切な方へのギフトにも選ばれています。",
                "spec_line": "価格：9,801円（税込・送料無料） / メーカー保証付",
            },
        ],
    },
    {
        "id": "08_zero_gravity_pillow",
        "out_name": "product_intro_08_zero_gravity_pillow.mp4",
        "theme_rgb": (22, 26, 38),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/08_1731596104749516239/gallery_02.jpg",
                "headline": "頭を乗せた瞬間、ふわっと重力が消える感覚。",
                "subheadline": "無重力ジェル枕 TPE素材（専用カバー付き）",
                "card_title": "頭に吸い付くようにフィットする、新感覚ハニカム枕",
                "body_line1": "ゴムのような柔軟性を持つTPE（熱可塑性エラストマー）素材を採用。",
                "body_line2": "頭や首の重みを一点に集中させず、包み込むように支えます。",
                "spec_line": "素材：高弾力TPEジェル素材（専用なめらかカバー付属）",
            },
            {
                "img": f"{GALLERY_BASE}/08_1731596104749516239/gallery_06.jpg",
                "headline": "10年使ってもへたりにくい、圧倒的な弾力性。",
                "subheadline": "無数の三角格子（ハニカム構造）が体圧をスムーズに分散",
                "card_title": "寝返りが打ちやすく、朝まで首・肩がラクに",
                "body_line1": "どんな頭の形や寝姿勢にも瞬時に変形してフィット。",
                "body_line2": "適度な反発力があるため、無理のない自然な寝返りをサポートします。",
                "spec_line": "構造：立体ハニカム格子構造（高耐久・体圧分散）",
            },
            {
                "img": f"{GALLERY_BASE}/08_1731596104749516239/gallery_08.jpg",
                "headline": "向きを変えるだけで、好みの高さを選べる。",
                "subheadline": "約8cmと約10cmの前後ウェーブ型デザイン",
                "card_title": "首元のカーブに寄り添う人間工学ウェーブ形状",
                "body_line1": "低めが好きな方は8cm側、しっかり支えたい方は10cm側へ。",
                "body_line2": "仰向け寝でも横向き寝でも、首筋の自然なラインをキープします。",
                "spec_line": "サイズ：高さ約8cm / 10cm（ウェーブ型）",
            },
            {
                "img": f"{GALLERY_BASE}/08_1731596104749516239/gallery_01.jpg",
                "headline": "頭に熱がこもらず、本体ごと水洗いできて清潔。",
                "subheadline": "通気性抜群の貫通構造 ＆ シャワーで丸洗いOK",
                "card_title": "無重力ジェル枕 TPE素材（専用カバー付）",
                "body_line1": "通気孔から熱や湿気を逃がすため、一晩中さらっと快適な寝心地。",
                "body_line2": "枕本体も水で丸洗いできるので、いつでも清潔にお使いいただけます。",
                "spec_line": "価格：5,778円（税込・送料無料）",
            },
        ],
    },
    {
        "id": "09_brass_incense_holder",
        "out_name": "product_intro_09_brass_incense_holder.mp4",
        "theme_rgb": (38, 30, 22),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/09_1734621162131982154/gallery_03.jpg",
                "headline": "お香の灰を気にせず、静かに香りを愉しむ夜に。",
                "subheadline": "真鍮 × 耐熱ガラス 瓢箪（ひょうたん）お香立て",
                "card_title": "ベッドサイドに美しく佇む、防風ガラス付き香炉",
                "body_line1": "透明なガラスカバーが風を防ぎ、お香の煙を穏やかに立ち昇らせます。",
                "body_line2": "エアコンの風で灰が飛び散る心配がなく、寝室でも安心です。",
                "spec_line": "素材：高ホウケイ酸耐熱ガラス × 無垢真鍮ベース",
            },
            {
                "img": f"{GALLERY_BASE}/09_1734621162131982154/gallery_04.jpg",
                "headline": "ガラスの中でゆらめく煙を、ただ眺める時間。",
                "subheadline": "防風・灰飛散防止設計でデスクや枕元を汚さない",
                "card_title": "落ちた灰はすべてガラスと真鍮トレイの中へ",
                "body_line1": "お香を焚いたあとにテーブルの上を掃除する手間がありません。",
                "body_line2": "間接照明の光を反射するガラスの曲線が、夜の空間を彩ります。",
                "spec_line": "サイズ：直径約8.7cm × 高さ約14cm",
            },
            {
                "img": f"{GALLERY_BASE}/09_1734621162131982154/gallery_06.jpg",
                "headline": "重厚感のある真鍮トレイと、縁起の良い瓢箪型。",
                "subheadline": "使い込むほどに味わいが深まるブラス（真鍮）素材",
                "card_title": "安定感のある瓢箪ホルダーが、お香をまっすぐ保持",
                "body_line1": "直径2.5mm未満の一般的なスティックお香に対応。",
                "body_line2": "ガラスカバーを外して、真鍮トレイ単体で使うことも可能です。",
                "spec_line": "対応：スティック型お香（穴径2.5mm未満）",
            },
            {
                "img": f"{GALLERY_BASE}/09_1734621162131982154/gallery_08.jpg",
                "headline": "3つのパーツに分解できて、お手入れも簡単。",
                "subheadline": "ガラスカバー・真鍮トレイ・瓢箪お香立ての3点セット",
                "card_title": "真鍮ガラス 瓢箪お香立て（防風・灰飛散防止）",
                "body_line1": "溜まった灰はガラスカバーを外してサッと捨てるだけ。",
                "body_line2": "水洗いもできるので、毎日の香りの習慣を清潔に続けられます。",
                "spec_line": "価格：1,489円（税込・送料無料）",
            },
        ],
    },
    {
        "id": "10_sozo_three_fragrant_woods",
        "out_name": "product_intro_10_sozo_three_fragrant_woods.mp4",
        "theme_rgb": (36, 28, 24),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/10_1736151959545546595/gallery_03.jpg",
                "headline": "日本の懐かしい花々の香りに、心がほどける夜。",
                "subheadline": "SOZO【お香】三大香木（沈丁花・くちなし・金木犀）",
                "card_title": "淡路島の香司が仕立てた、3つの香りのアソート",
                "body_line1": "春の沈丁花、初夏のくちなし、秋の金木犀。",
                "body_line2": "季節の記憶を呼び覚ます優しい花の香りが、寝室にふわりと広がります。",
                "spec_line": "香り：沈丁花 / くちなし / 金木犀（3種アソート）",
            },
            {
                "img": f"{GALLERY_BASE}/10_1736151959545546595/gallery_02.jpg",
                "headline": "お香立てがなくても、届いたその夜から愉しめる。",
                "subheadline": "専用マッチ1箱 ＆ 不燃性マット1枚がセットに",
                "card_title": "不燃性マットの上に寝かせて焚ける安心スタイル",
                "body_line1": "付属の黒い不燃性マットの上にお香をそのまま置いて焚くだけ。",
                "body_line2": "火をつける瞬間から、静かなマインドフルネスの時間が始まります。",
                "spec_line": "付属品：お香15本・専用マッチ1箱・不燃性マット1枚",
            },
            {
                "img": f"{GALLERY_BASE}/10_1736151959545546595/gallery_04.jpg",
                "headline": "おやすみ前の7分間、スマホを置いて香りを聴く。",
                "subheadline": "1本あたり約7分のショートサイズ・日本製",
                "card_title": "寝る前のちょっとした気分転換にちょうどいい長さ",
                "body_line1": "長すぎない約7分の燃焼時間だから、就寝前にも気軽に焚けます。",
                "body_line2": "強い合成香料が苦手な方にもおすすめの、穏やかな香り立ちです。",
                "spec_line": "生産国：日本（兵庫県淡路島） / 燃焼時間：約7分",
            },
            {
                "img": f"{GALLERY_BASE}/10_1736151959545546595/gallery_05.jpg",
                "headline": "その日の気分で香りを選ぶ、夜の小さな贅沢。",
                "subheadline": "モダンな小箱パッケージでプチギフトにも人気",
                "card_title": "SOZO お香「三大香木」15本入セット",
                "body_line1": "3種類の香りを少しずつ試せるので、お香デビューにも最適。",
                "body_line2": "1日の終わりに、深呼吸したくなる香りの習慣を。",
                "spec_line": "価格：1,700円（税込・送料無料）",
            },
        ],
    },
    {
        "id": "11_glass_aroma_candle",
        "out_name": "product_intro_11_glass_aroma_candle.mp4",
        "theme_rgb": (38, 28, 18),
        "scenes": [
            {
                "img": f"{GALLERY_BASE}/11_1733361545697461699/gallery_01.jpg",
                "headline": "部屋の明かりを消して、小さな炎を見つめる夜。",
                "subheadline": "エレガントなガラス製アロマキャンドル",
                "card_title": "1/fゆらぎの灯りと優しい香りが、心を鎮める",
                "body_line1": "アンバーグラス越しにゆらめく温かなキャンドルの灯り。",
                "body_line2": "規則性と不規則性が調和した炎のゆらぎが、深いリラックスへ導きます。",
                "spec_line": "仕様：ガラスジャー入りフレグランスキャンドル",
            },
            {
                "img": f"{GALLERY_BASE}/11_1733361545697461699/gallery_07.jpg",
                "headline": "ベッドサイドやバスルームを、穏やかな空間に。",
                "subheadline": "天然ソイワックス配合・ススが出にくくクリーンな燃焼",
                "card_title": "強すぎない上品な香りで、寝室でも使いやすい",
                "body_line1": "火を灯すと、ほのかなアロマが空間全体に優しく広がります。",
                "body_line2": "読書の時間や、眠りにつく前のストレッチのお供に。",
                "spec_line": "サイズ：直径約5.2cm × 高さ約6.2cm（コンパクトサイズ）",
            },
            {
                "img": f"{GALLERY_BASE}/11_1733361545697461699/gallery_03.jpg",
                "headline": "インテリアに馴染む、クラシックなガラスジャー。",
                "subheadline": "火を灯していない時も絵になるミニマルデザイン",
                "card_title": "風を防ぎ、最後まで綺麗に溶けるグラス容器",
                "body_line1": "キャンドルホルダー不要で、そのままテーブルに置いて使えます。",
                "body_line2": "使い終わったあとのガラス瓶は、小物入れとしても活用できます。",
                "spec_line": "デザイン：クラシックラベル × 耐熱ガラス容器",
            },
            {
                "img": f"{GALLERY_BASE}/11_1733361545697461699/gallery_05.jpg",
                "headline": "1,000円以下で気軽に始める、キャンドルのある夜。",
                "subheadline": "専用クラフトボックス入り・プレゼントにも",
                "card_title": "エレガントなガラス製アロマキャンドル（化粧箱付）",
                "body_line1": "おしゃれなリボン付きボックス入りで、自分用にもギフトにも。",
                "body_line2": "忙しい1日の終わりに、灯りと香りで心をととのえる時間を。",
                "spec_line": "価格：990円（税込） / 専用ギフトボックス入り",
            },
        ],
    },
]


if __name__ == "__main__":
    import sys
    only_new = "--only-new" in sys.argv
    targets = [
        p for p in PRODUCTS
        if not (only_new and os.path.exists(os.path.join(OUTPUT_DIR, p["out_name"])))
    ]
    print(f"Rendering {len(targets)} product videos...")
    with ProcessPoolExecutor(max_workers=3) as ex:
        list(ex.map(render_single_product_video, targets))
    print("All v5 (1min-mindful Recommended Night Item) videos rendered successfully!")

