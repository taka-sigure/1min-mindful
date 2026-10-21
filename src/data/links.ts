import { affiliateConfig } from "../config/affiliate";

export type LinkCategory =
  | "目元を休める"
  | "灯りと香り"
  | "眠りとバスタイム"
  | "夜の音";

/** リンク集の1件。商品ページはあとから asin か productUrl を足す。 */
export interface LinkItem {
  id: string;
  category: LinkCategory;
  title: string;
  description: string;
  /**
   * Amazonの検索キーワード。
   * asin も productUrl も無いとき、この語の検索URLにフォールバックする。
   */
  searchQuery?: string;
  /**
   * 商品ページのURL。asin が無いときに searchQuery より優先する。
   * amazon.co.jp のURLにはアソシエイトタグを付ける。
   */
  productUrl?: string;
  /**
   * AmazonのASIN（英数字10桁）。
   * 指定すると productUrl と searchQuery より優先する。
   */
  asin?: string;
  /**
   * Amazon以外のリンク先（YouTubeなど）。
   * 指定すると他の項目より優先し、アソシエイトタグは付けない。
   */
  url?: string;
  /**
   * 楽天市場の検索キーワード（もしもアフィリエイト経由URL生成用・任意）。
   */
  rakutenQuery?: string;
  isExternal?: boolean;
}

/** ページに渡す、遷移先が決まったリンク。 */
export interface ResolvedLinkItem extends LinkItem {
  /** 実際に開くURL。 */
  href: string;
  /** 楽天市場（もしもアフィリエイト経由）のURL（指定時のみ）。 */
  rakutenUrl?: string;
  /** Amazonアソシエイトの対象か。YouTube などは false。 */
  isAffiliate: boolean;
}

const accountName = "1分マインドフルネス";

export const profileData = {
  accountName,
  handle: "@1min_mindful",
  description: "夜、頭が静かになる1分を。\n呼吸と、少しの言葉。",
  footerMessage: "今日もおつかれさまでした。",
  /** ページ上部に出すステマ規制向けの表示。 */
  adLabel: "PR",
  adNotice: "商品リンクは広告です",
  /** Amazon.co.jp の運営規約が定める開示文。運営者名はアカウント名と揃える。 */
  disclaimer: `Amazonのアソシエイトとして、${accountName}は適格販売により収入を得ています。`,
};

/** もしもアフィリエイト どこでもリンク生成ヘルパー（楽天市場検索URL等） */
export const createMoshimoRakutenUrl = (targetUrl: string): string => {
  const { aId, promotionId } = affiliateConfig.moshimo.rakuten;
  return `https://af.moshimo.com/af/c/click?a_id=${aId}&p_id=${promotionId}&pc_id=${promotionId}&pl_id=616&url=${encodeURIComponent(targetUrl)}`;
};

export const createRakutenSearchUrl = (query: string): string => {
  const rakutenSearch = `https://search.rakuten.co.jp/search/mall/${encodeURIComponent(query)}/`;
  return createMoshimoRakutenUrl(rakutenSearch);
};

const linkItemSources: LinkItem[] = [
  // 目元を休める（TikTok紹介4アイテム）
  {
    id: "nerugoo-eye-mask",
    category: "目元を休める",
    title: "nerugoo 充電式ホットアイマスク",
    description: "画面を見続けた夜、シルクの肌触りで目の奥をじんわり温めるマスク",
    searchQuery: "nerugoo ホットアイマスク 充電式",
    rakutenQuery: "nerugoo ホットアイマスク",
    isExternal: true,
  },
  {
    id: "niplux-eye-relax",
    category: "目元を休める",
    title: "NIPLUX EYE RELAX S アイウォーマー",
    description: "こめかみから目元まで、温熱とやさしい加圧でほぐしたい夜に",
    searchQuery: "NIPLUX EYE RELAX S アイウォーマー",
    rakutenQuery: "NIPLUX EYE RELAX S",
    isExternal: true,
  },
  {
    id: "silk-sleep-mask",
    category: "目元を休める",
    title: "シルク・ふんわり遮光アイマスク",
    description: "光をやさしく遮るマスクを、明かりが気になる夜に使っています",
    searchQuery: "シルク アイマスク 遮光 洗える",
    rakutenQuery: "シルク アイマスク 遮光",
    isExternal: true,
  },
  {
    id: "megurhythm-steam-mask",
    category: "目元を休める",
    title: "めぐりズム 蒸気でホットアイマスク",
    description: "袋を開けるだけで約40℃の蒸気に包まれる、使い切りタイプの定番",
    searchQuery: "めぐりズム 蒸気でホットアイマスク 完熟ゆず ラベンダー",
    rakutenQuery: "めぐりズム 蒸気でホットアイマスク",
    isExternal: true,
  },

  // 灯りと香り（TikTok紹介4アイテム）
  {
    id: "water-ripple-lamp",
    category: "灯りと香り",
    title: "水面波紋のアンビエントライト・間接照明",
    description: "寝る前、部屋の明かりを落として水面のゆらぎを眺めるライト",
    searchQuery: "水面 波紋 ライト 間接照明 ベッドサイド",
    rakutenQuery: "水面 波紋 ライト 間接照明",
    isExternal: true,
  },
  {
    id: "glass-aroma-candle",
    category: "灯りと香り",
    title: "夜のガラス製アロマキャンドル",
    description: "画面を閉じたあと、揺れる灯りと香りのある時間に",
    searchQuery: "アロマキャンドル ガラス ソイワックス リラックス",
    rakutenQuery: "アロマキャンドル ガラス リラックス",
    isExternal: true,
  },
  {
    id: "brass-incense-stand",
    category: "灯りと香り",
    title: "焚いているお香・真鍮ガラスのお香立て",
    description: "白檀やラベンダーの香りを、灰が散らないガラス筒のお香立てで",
    searchQuery: "真鍮 ガラス お香立て インセンスホルダー",
    rakutenQuery: "真鍮 ガラス お香立て",
    isExternal: true,
  },
  {
    id: "palo-santo-sticks",
    category: "灯りと香り",
    title: "パロサント香木スティック",
    description: "火を灯さず置いておくだけでも、森のような甘い香りが漂う香木",
    searchQuery: "パロサント スティック 香木 ペルー産",
    rakutenQuery: "パロサント スティック 香木",
    isExternal: true,
  },

  // 眠りとバスタイム（TikTok紹介3アイテム）
  {
    id: "imabari-towel-pillow",
    category: "眠りとバスタイム",
    title: "今治睡眠用タオル2（高さ調整タオル枕）",
    description: "その日の首の疲れに合わせて、巻くだけで高さを微調整できる今治タオル枕",
    searchQuery: "今治睡眠用タオル2 枕 Nelture",
    rakutenQuery: "今治睡眠用タオル2",
    isExternal: true,
  },
  {
    id: "zero-gravity-gel-pillow",
    category: "眠りとバスタイム",
    title: "ヒツジのいらない枕（無重力TPEジェル枕）",
    description: "頭を乗せた瞬間に圧力を分散し、熱がこもりにくい格子構造のジェル枕",
    searchQuery: "ヒツジのいらない枕 至極 TPE ジェル枕",
    rakutenQuery: "ヒツジのいらない枕",
    isExternal: true,
  },
  {
    id: "epsom-salt-bath",
    category: "眠りとバスタイム",
    title: "湯船用の国産エプソムソルト（シークリスタルス）",
    description: "湯船に入れて、ゆっくり温まる夜のバスタイムに",
    searchQuery: "シークリスタルス エプソムソルト 国産 入浴剤",
    rakutenQuery: "シークリスタルス エプソムソルト",
    isExternal: true,
  },

  // 夜の音
  {
    id: "audible-night-reading",
    category: "夜の音",
    title: "夜、寝る前に聴いているもの",
    description: "夜に聴く朗読や、静かな雨の音（Audible）",
    productUrl: "https://www.amazon.co.jp/audible",
    isExternal: true,
  },
  {
    id: "youtube-long-bgm",
    category: "夜の音",
    title: "長尺の睡眠用BGM（YouTube）",
    description: "1時間以上の静かな雨音と環境音",
    url: "https://www.youtube.com/@1min_mindful",
    isExternal: true,
  },
];

/**
 * リンク1件の公開URLを決める。
 * 優先順位は url、asin、productUrl、searchQuery。AmazonのURLにはアソシエイトタグを付ける。
 * @param item リンク定義。遷移先のいずれか1つが必要。
 * @returns ページの href に使うURL。
 */
export function resolveLinkHref(item: LinkItem): string {
  if (item.url) {
    return item.url;
  }

  const tag = affiliateConfig.amazon.tag;

  if (item.asin) {
    const asin = item.asin.trim().toUpperCase();
    if (!/^[A-Z0-9]{10}$/.test(asin)) {
      throw new Error(`ASINは英数字10桁で指定してください（${item.title}）`);
    }
    return `https://www.amazon.co.jp/dp/${asin}?tag=${tag}`;
  }

  if (item.productUrl) {
    return applyAmazonAssociateTag(item.productUrl, tag);
  }

  if (item.searchQuery) {
    return `https://www.amazon.co.jp/s?k=${encodeURIComponent(item.searchQuery)}&tag=${tag}`;
  }

  throw new Error(`リンク先がありません（${item.title}）`);
}

/**
 * amazon.co.jp のURLにアソシエイトタグを付ける。別の tag があっても設定値で上書きする。
 * @param rawUrl 商品ページなどのURL。
 * @param tag `affiliateConfig.amazon.tag`。
 * @returns タグ付きのURL。Amazon以外はそのまま返す。
 */
function applyAmazonAssociateTag(rawUrl: string, tag: string): string {
  let parsed: URL;
  try {
    parsed = new URL(rawUrl);
  } catch {
    throw new Error(`商品URLを解釈できません（${rawUrl}）`);
  }

  const host = parsed.hostname.toLowerCase();

  if (host === "amzn.to" || host === "amzn.asia" || host.endsWith(".amzn.to")) {
    throw new Error(
      `短縮URLにはタグを付けられません。ASINか amazon.co.jp の商品URLを指定してください: ${rawUrl}`,
    );
  }

  const isAmazon = host === "amazon.co.jp" || host.endsWith(".amazon.co.jp");
  if (!isAmazon) {
    return rawUrl;
  }

  parsed.searchParams.set("tag", tag);
  return parsed.toString();
}

export const linkItems: ResolvedLinkItem[] = linkItemSources.map((item) => {
  const href = resolveLinkHref(item);
  const rakutenUrl = item.rakutenQuery
    ? createRakutenSearchUrl(item.rakutenQuery)
    : undefined;
  let host = "";
  try {
    host = new URL(href).hostname.toLowerCase();
  } catch {
    host = "";
  }

  const isAffiliate = host === "amazon.co.jp" || host.endsWith(".amazon.co.jp");
  return { ...item, href, rakutenUrl, isAffiliate };
});

export const linkCategories: LinkCategory[] = [
  "目元を休める",
  "灯りと香り",
  "眠りとバスタイム",
  "夜の音",
];
