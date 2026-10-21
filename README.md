# 1分マインドフルネス リンク集

TikTok [@1min_mindful](https://www.tiktok.com/@1min_mindful) / YouTube [@1min_mindful](https://www.youtube.com/@1min_mindful) のバイオリンクです。  
公開URL: https://taka-sigure.github.io/1min-mindful/

商品リンクは Amazon アソシエイト（タグ `takasigure101-22`）です。タグの値は `src/config/affiliate.ts` の `affiliateConfig.amazon.tag` で管理し、リンクごとに手書きしません。

## 商品リンクを個別ページに差し替える

文言とリンク先は `src/data/links.ts` の `linkItems` です。初期状態は1商品ごとの検索結果へのリンクで、商品が決まったら、その項目に `asin` か `productUrl` を足してください。どちらも空なら、これまでどおり `searchQuery` の検索URLになります。

優先順位:

1. `url` — YouTube など Amazon 以外。書いたURLをそのまま使います（タグは付きません）
2. `asin` — `https://www.amazon.co.jp/dp/{ASIN}?tag=（設定のタグ）`
3. `productUrl` — 商品ページのURL。`amazon.co.jp` ならタグを付けます。別の `tag` が付いていても、設定のタグで上書きします
4. `searchQuery` — 検索URL。タグ付き

`asin` と `productUrl` を両方書いたときは `asin` を使います。ASIN は英数字10桁です。`amzn.to` などの短縮URLはタグを付けられないため使えません。

```ts
{
  id: "nerugoo-eye-mask",
  category: "目元を休める",
  title: "nerugoo 充電式ホットアイマスク",
  description: "画面を見続けた夜、シルクの肌触りで目の奥をじんわり温めるマスク",
  searchQuery: "nerugoo ホットアイマスク 充電式",
  // 商品が決まったら、どちらか一方のコメントを外す（asin が優先）
  // asin: "B0XXXXXXXX",
  // productUrl: "https://www.amazon.co.jp/dp/B0XXXXXXXX",
}
```

## 広告表示

ページ上部に「PR / 商品リンクは広告です」を出しています。フッターの開示文は次の一文です。運営者名は `profileData.accountName`（1分マインドフルネス）と揃えています。

> Amazonのアソシエイトとして、1分マインドフルネスは適格販売により収入を得ています。

楽天など、ページに無いサービスの名前は書かないでください。

## コマンド

| Command           | Action                                      |
| :---------------- | :------------------------------------------ |
| `npm install`     | 依存関係を入れる                            |
| `npm run dev`     | 開発サーバー（`localhost:4321`）            |
| `npm run build`   | `./dist/` へ本番ビルド                      |
| `npm run preview` | ビルド結果をローカルで確認                  |

サイトのベースパスは `/1min-mindful` です。ローカルでは `http://localhost:4321/1min-mindful/` を開いてください。

## 動画生成パイプライン（TikTok / Shorts 60秒縦型動画）

- `scripts/products_catalog.json`: TikTok Shop ショーケース 11商品の価格・検索クエリ・特徴を一元管理するマスターデータ
- `scripts/lib/video_common.py`: FFmpeg + Pillow による字幕レンダリング・素材パス解決（`assets/` 優先、`/tmp` フォールバック、自動プレースホルダー生成）
- `scripts/render_safe_profile_videos.py`: プロフィールリンク誘導型の静かな60秒動画（4本）
- `scripts/render_eyecare_videos.py`: 目元ケア特化の60秒動画（3本）
- `scripts/render_all_showcase_videos.py`: ショーケース全11商品の60秒動画一括生成
