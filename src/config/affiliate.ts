// アフィリエイト設定・各ASPの識別子管理
export const affiliateConfig = {
  // バリューコマース: LinkSwitch用PID（管理画面から取得したPIDを設定すると自動リンク化が有効になります）
  valueCommerce: {
    enabled: true,
    pid: "YOUR_VALUECOMMERCE_PID", // あなたのバリューコマースPID
  },

  // もしもアフィリエイト: かんたんリンク / アカウント設定
  moshimo: {
    enabled: true,
    aId: "YOUR_MOSHIMO_A_ID", // もしもアフィリエイトID
  },

  // A8.net: メディアID等
  a8: {
    enabled: true,
  },

  // afb: アカウント設定
  afb: {
    enabled: true,
  },
};
