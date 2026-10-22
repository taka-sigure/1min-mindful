import { affiliateConfig } from "../config/affiliate";

export type LinkCategory = "目元を休める" | "灯りと香り" | "夜の音";

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
  {
    id: "megurhythm-steam-eye-mask",
    category: "目元を休める",
    title: "寝る前の蒸気アイマスク（めぐりズム）",
    description: "袋を開けた夜、あたたかい蒸気が目元を包む使い切りのアイマスク",
    asin: "B0FKB678DY",
    isExternal: true,
  },
  {
    id: "moon-garden-herbal-tea",
    category: "灯りと香り",
    title: "夜のノンカフェインハーブティー（ムーンガーデン）",
    description: "夜、湯を注いでハーブの香りを待つティーバッグ",
    asin: "B0GZGFZ2TS",
    isExternal: true,
  },
  {
    id: "silentia-earplugs",
    category: "夜の音",
    title: "静かな夜の耳栓（サイレンシア）",
    description: "夜、耳へそっと入れるレギュラーサイズの耳栓",
    asin: "B0B5L876DT",
    isExternal: true,
  },

  // 夜の音（商品以外）
  {
    id: "audible-night-reading",
    category: "夜の音",
    title: "夜、寝る前に聴いているもの",
    description: "夜に聴く朗読や、静かな雨の音（Audible）",
    productUrl: "https://www.amazon.co.jp/audible",
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
  "夜の音",
];
