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
    url: "https://www.youtube.com/",
    isExternal: true,
  },
  {
    title: "焚いているお香・パロサント",
    description: "気持ちを切り替えたいときに使っている香り",
    url: "https://www.amazon.co.jp/s?k=パロサント",
    isExternal: true,
  },
  {
    title: "使っている枕",
    description: "頭に熱がこもらない通気性のいい枕",
    url: "https://item.rakuten.co.jp/",
    isExternal: true,
  },
  {
    title: "シルクのアイマスク",
    description: "光をしっかり遮りたい夜に使っています",
    url: "https://item.rakuten.co.jp/",
    isExternal: true,
  },
];
