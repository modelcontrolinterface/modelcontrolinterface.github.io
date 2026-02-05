import { defineConfig } from "astro/config";

import icon from "astro-icon";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

import rehypeSlug from "rehype-slug";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeCallouts from "rehype-callouts";
import rehypeExternalLinks from "rehype-external-links";
import rehypeAutolinkHeadings from "rehype-autolink-headings";

export default defineConfig({
  site: "https://modelcontrolinterface.github.io",
  base: "/blog",
  markdown: {
    shikiConfig: {
      wrap: false,
      themes: {
        dark: "catppuccin-mocha",
        light: "catppuccin-latte",
      },
    },
    remarkPlugins: [remarkMath],
    rehypePlugins: [
      rehypeSlug,
      [
        rehypeExternalLinks,
        { target: "_blank", rel: ["noopener", "noreferrer"] },
      ],
      rehypeKatex,
      rehypeCallouts,
      [
        rehypeAutolinkHeadings,
        { behavior: "wrap", properties: { className: "heading-anchor" } },
      ],
    ],
  },
  vite: { plugins: [tailwindcss()] },
  integrations: [mdx(), sitemap(), icon()],
});
