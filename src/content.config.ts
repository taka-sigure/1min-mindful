import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    heroImage: z.string().optional(),
    
    // 孫ギフト専用項目
    targetAge: z.array(z.string()), // 例: ['0〜1歳', '2〜3歳', '4〜6歳', '小学生低学年', '小学生高学年']
    category: z.enum(['テレビ話題', '知育玩具', 'おもちゃ・ゲーム', '入学・入園', 'イベント・季節']),
    isTrend: z.boolean().default(false), // 急上昇・テレビ話題フラグ
    
    // メイン商品情報（冒頭の結論枠・クイックサマリー用）
    primaryItem: z.object({
      name: z.string(),
      rakutenUrl: z.string(),
      amazonUrl: z.string(),
      priceText: z.string().optional(), // 例: "約3,980円"
      isOfficialShop: z.boolean().default(true),
    }).optional(),
  }),
});

export const collections = { posts };
