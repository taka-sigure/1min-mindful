// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://taka-sigure.github.io',
  base: '/1min-mindful',
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()],
  },
});