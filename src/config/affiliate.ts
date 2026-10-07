// アフィリエイト設定・各ASPの識別子管理（「1分マインドフルネス」公式登録ID）
export const affiliateConfig = {
  // バリューコマース: LinkSwitch / サイトID: 3783908
  valueCommerce: {
    enabled: true,
    siteId: "3783908",
    pid: "892722183", // 1分マインドフルネス専用PID
  },

  // Amazonアソシエイト設定
  amazon: {
    enabled: true,
    tag: "takasigure101-22", // AmazonアソシエイトID
  },

  // もしもアフィリエイト: メディアID: 691751
  moshimo: {
    enabled: true,
    shopSiteId: "691751",
    // 提携済みプロモーションID
    rakuten: {
      promotionId: "54",
      aId: "5837465", // 楽天市場専用a_id
    },
    amazon: {
      promotionId: "170",
      status: "pending", // 審査完了後にa_id発行
    },
  },

  // A8.net: メディアID / サイトID
  a8: {
    enabled: true,
    mediaId: "a19112417395",
    siteId: "007", // 1分マインドフルネス
  },

  // afb: アカウント設定
  afb: {
    enabled: true,
    status: "applied", // 審査待ち（即日〜1営業日）
  },
};

