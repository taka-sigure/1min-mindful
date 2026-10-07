import { affiliateConfig } from "../config/affiliate";

export interface LinkItem {
  title: string;
  description: string;
  url: string;
  isExternal?: boolean;
}

export const profileData = {
  accountName: "1分マインドフルネス",
  handle: "@1min_mindful",
  description: "夜、頭が静かになる1分を。\n呼吸と、少しの言葉。",
  footerMessage: "今日もおつかれさまでした。",
  disclaimer: "※各リンクはAmazonアソシエイト・楽天等のアフィリエイトを利用しています",
};

// もしもアフィリエイト どこでもリンク生成ヘルパー
const createMoshimoRakutenUrl = (targetUrl: string) => {
  const { aId, promotionId } = affiliateConfig.moshimo.rakuten;
  return `https://af.moshimo.com/af/c/click?a_id=${aId}&p_id=${promotionId}&pc_id=${promotionId}&pl_id=616&url=${encodeURIComponent(targetUrl)}`;
};

export const linkItems: LinkItem[] = [
  {
    title: "夜、寝る前に聴いているもの",
    description: "眠れない夜の朗読・静かな雨の音（Audible）",
    url: "https://www.amazon.co.jp/b?node=5843468051",
    isExternal: true,
  },
  {
    title: "長めの音（YouTube）",
    description: "雨の音や静かな環境音を置いています",
    url: "https://www.youtube.com/@1min_mindful",
    isExternal: true,
  },
  {
    title: "焚いているお香・パロサント",
    description: "気持ちを切り替えたいときに使っている香り",
    url: "https://www.amazon.co.jp/s?k=%E3%83%91%E3%82%ED%81%95%E3%83%B3%E3%83%88",
    isExternal: true,
  },
  {
    title: "使っている枕",
    description: "頭に熱がこもらない通気性のいい枕",
    url: createMoshimoRakutenUrl("https://search.rakuten.co.jp/search/mall/%E9%80%9A%E6%B0%97%E6%80%A7+%E6%9E%95/"),
    isExternal: true,
  },
  {
    title: "シルクのアイマスク",
    description: "光をしっかり遮りたい夜に使っています",
    url: createMoshimoRakutenUrl("https://search.rakuten.co.jp/search/mall/%E3%82%B7%E3%83%AB%E3%82%AF+%E3%82%A2%E3%82%A4%E3%83%9E%E3%82%B9%E3%82%AF+%E9%81%AE%E5%85%89/"),
    isExternal: true,
  },
];
