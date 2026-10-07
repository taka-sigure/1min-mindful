// アフィリエイト連携データ定義

export interface BaseItem {
  id: string;
  title: string;
  description: string;
}

export interface StandardLinkItem extends BaseItem {
  type: 'link';
  url: string;
  isExternal?: boolean;
}

export interface LeadItem extends BaseItem {
  type: 'lead';
  tagline?: string;
  microCopy: string;
  ctaText: string;
  affiliateUrl: string;
  highlight?: boolean;
  badge?: string;
}

export interface ProductItem extends BaseItem {
  type: 'product';
  price?: string;
  amazonUrl?: string;
  rakutenUrl?: string; // もしもアフィリエイトまたは楽天
  yahooUrl?: string;   // バリューコマースまたはもしも
  badge?: string;
}

export type FeedItem = StandardLinkItem | LeadItem | ProductItem;

export const profileData = {
  accountName: "1分マインドフルネス",
  handle: "@1min_mindful",
  description: "夜、頭が静かになる1分を。\n呼吸と、少しの言葉。",
  footerMessage: "今日もおつかれさまでした。",
  disclaimer: "※各リンクはAmazonアソシエイト・楽天・もしも・A8・バリューコマース等のアフィリエイトを利用しています",
};

// 高CVR化された導線一覧
export const feedItems: FeedItem[] = [
  // 1. 最優先導線（無料体験リード型 / A8.net または Amazonアソシエイト）: CVR 5〜10%
  {
    id: "audible-trial",
    type: "lead",
    tagline: "無料体験で聴く",
    title: "夜、寝る前に聴いているもの（Audible）",
    description: "ベッドに入ったまま声や音に身を委ねられるオーディオブック。眠れない夜の朗読・自然音を多数収録。",
    microCopy: "30日間無料体験・いつでも解約OK",
    ctaText: "まずは無料で1冊聴いてみる",
    affiliateUrl: "https://www.amazon.co.jp/b?node=5843468051", // A8.netまたはAmazonアソシエイトのAudible紹介URL
    highlight: true,
    badge: "人気 No.1",
  },
  // 2. 自社コンテンツ（YouTube）
  {
    id: "youtube-long",
    type: "link",
    title: "長めの音（YouTube）",
    description: "雨の音や静かな環境音を置いています",
    url: "https://www.youtube.com/",
    isExternal: true,
  },
  // 3. 物販系アイテム（もしも・バリューコマース・Amazonの3大モール一括）
  {
    id: "item-incense",
    type: "product",
    title: "焚いているお香・パロサント",
    description: "気分を静めて眠りのスイッチを入れる、天然の優しいウッディな香り。",
    price: "約1,500円〜",
    amazonUrl: "https://www.amazon.co.jp/s?k=パロサント",
    rakutenUrl: "https://search.rakuten.co.jp/search/mall/パロサント/", // もしもアフィリエイト経由に差し替え可能
    yahooUrl: "https://shopping.yahoo.co.jp/search?p=パロサント",       // バリューコマースLinkSwitchで自動化
    badge: "愛用品",
  },
  {
    id: "item-pillow",
    type: "product",
    title: "熱がこもらない高通気枕",
    description: "頭の熱を逃がし、スムーズな寝返りと深い休息をサポートする枕。",
    price: "約8,000円〜",
    amazonUrl: "https://www.amazon.co.jp/s?k=ブレインスリープ+ピロー",
    rakutenUrl: "https://search.rakuten.co.jp/search/mall/通気性+枕/",
    yahooUrl: "https://shopping.yahoo.co.jp/search?p=通気性+枕",
  },
  {
    id: "item-eyemask",
    type: "product",
    title: "遮光シルクアイマスク",
    description: "目元に余計な圧迫感を与えず、朝の光を100%遮断するシルク素材。",
    price: "約2,000円〜",
    amazonUrl: "https://www.amazon.co.jp/s?k=シルク+アイマスク+遮光",
    rakutenUrl: "https://search.rakuten.co.jp/search/mall/シルク+アイマスク+遮光/",
    yahooUrl: "https://shopping.yahoo.co.jp/search?p=シルク+アイマスク+遮光",
  },
];

// 後方互換用
export const linkItems = feedItems.map((item) => {
  if (item.type === 'link') {
    return { title: item.title, description: item.description, url: item.url, isExternal: item.isExternal };
  } else if (item.type === 'lead') {
    return { title: item.title, description: item.description, url: item.affiliateUrl, isExternal: true };
  } else {
    return { title: item.title, description: item.description, url: item.amazonUrl || item.rakutenUrl || item.yahooUrl || '#', isExternal: true };
  }
});
