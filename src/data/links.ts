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
    title: "目元を温めるホットアイマスク・アイウォーマー",
    description: "画面を見続けた夜、目の奥をじんわり緩める温熱マスク（nerugoo / NIPLUX）",
    url: `https://www.amazon.co.jp/s?k=${encodeURIComponent("ホットアイマスク 充電式 NIPLUX nerugoo")}&tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "シルク・ふんわり遮光アイマスク",
    description: "光をやさしく遮って、目を休めたい夜に使っています",
    url: `https://www.amazon.co.jp/s?k=${encodeURIComponent("シルク アイマスク 遮光 洗える")}&tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "水面波紋のアンビエントライト・間接照明",
    description: "寝る前、部屋の明かりを落として水面のゆらぎで目を休めるライト",
    url: `https://www.amazon.co.jp/s?k=${encodeURIComponent("水面 波紋 ライト 間接照明 ベッドサイド")}&tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "夜のガラス製アロマキャンドル",
    description: "画面を閉じたあと、揺れる灯りと香りで目を休める時間に",
    url: `https://www.amazon.co.jp/s?k=${encodeURIComponent("アロマキャンドル ガラス リラックス")}&tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "首・肩を休めるタオル枕・無重力ジェル枕",
    description: "首の高さにやさしく馴染む今治睡眠用タオル枕・通気性のいいジェル枕",
    url: `https://www.amazon.co.jp/s?k=${encodeURIComponent("今治睡眠用タオル2 無重力 ジェル枕")}&tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "焚いているお香・真鍮ガラスのお香立て",
    description: "考えごとを切り替えて、夜の静けさに入るための香り（香木・ラベンダー）",
    url: `https://www.amazon.co.jp/s?k=${encodeURIComponent("お香 白檀 ラベンダー 真鍮 ガラス お香立て")}&tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "湯船でゆるむ国産エプソムソルト",
    description: "体の芯まで疲れが残る夜、ゆっくり温まるバスタイムに",
    url: `https://www.amazon.co.jp/s?k=${encodeURIComponent("国産 エプソムソルト 入浴剤")}&tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "夜、寝る前に聴いているもの",
    description: "眠れない夜の朗読・静かな雨の音（Audible）",
    url: `https://www.amazon.co.jp/audible?tag=${affiliateConfig.amazon.tag}`,
    isExternal: true,
  },
  {
    title: "長めの音（YouTube）",
    description: "雨の音や静かな環境音を置いています",
    url: "https://www.youtube.com/@1min_mindful",
    isExternal: true,
  },
];

