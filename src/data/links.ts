import { affiliateConfig } from "../config/affiliate";

/** リンク集の1件。商品ページはあとから asin か productUrl を足す。 */
export interface LinkItem {
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
  isExternal?: boolean;
}

/** ページに渡す、遷移先が決まったリンク。 */
export interface ResolvedLinkItem extends LinkItem {
  /** 実際に開くURL。 */
  href: string;
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

const linkItemSources: LinkItem[] = [
  {
    title: "ホットアイマスク・アイウォーマー",
    description: "画面を見続けた夜に、目元へあてておく温かいマスク（nerugoo / NIPLUX）",
    searchQuery: "ホットアイマスク 充電式 NIPLUX nerugoo",
    isExternal: true,
  },
  {
    title: "シルク・ふんわり遮光アイマスク",
    description: "光をやさしく遮るマスクを、明かりが気になる夜に使っています",
    searchQuery: "シルク アイマスク 遮光 洗える",
    isExternal: true,
  },
  {
    title: "水面波紋のアンビエントライト・間接照明",
    description: "寝る前、部屋の明かりを落として水面のゆらぎを眺めるライト",
    searchQuery: "水面 波紋 ライト 間接照明 ベッドサイド",
    isExternal: true,
  },
  {
    title: "夜のガラス製アロマキャンドル",
    description: "画面を閉じたあと、揺れる灯りと香りのある時間に",
    searchQuery: "アロマキャンドル ガラス リラックス",
    isExternal: true,
  },
  {
    title: "タオル枕・無重力ジェル枕",
    description: "首の高さにやさしく馴染む今治睡眠用タオル枕・通気性のいいジェル枕",
    searchQuery: "今治睡眠用タオル2 無重力 ジェル枕",
    isExternal: true,
  },
  {
    title: "焚いているお香・真鍮ガラスのお香立て",
    description: "香木やラベンダーの香りを、夜の部屋に",
    searchQuery: "お香 白檀 ラベンダー 真鍮 ガラス お香立て",
    isExternal: true,
  },
  {
    title: "湯船用の国産エプソムソルト",
    description: "湯船に入れて、ゆっくり温まる夜のバスタイムに",
    searchQuery: "国産 エプソムソルト 入浴剤",
    isExternal: true,
  },
  {
    title: "夜、寝る前に聴いているもの",
    description: "夜に聴く朗読や、静かな雨の音（Audible）",
    productUrl: "https://www.amazon.co.jp/audible",
    isExternal: true,
  },
  {
    title: "長めの音（YouTube）",
    description: "雨の音や静かな環境音を置いています",
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
  let host = "";
  try {
    host = new URL(href).hostname.toLowerCase();
  } catch {
    host = "";
  }

  const isAffiliate = host === "amazon.co.jp" || host.endsWith(".amazon.co.jp");
  return { ...item, href, isAffiliate };
});
