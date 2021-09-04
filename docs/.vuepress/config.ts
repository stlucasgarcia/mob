import { defineUserConfig } from "vuepress";
import type { DefaultThemeOptions } from "vuepress";

export default defineUserConfig<DefaultThemeOptions>({
	lang: "en-US",
	title: "Mob Docs",
	description: "Just playing around",

	base: "/mob/",

	themeConfig: {
		docsRepo: "lsglucas/mob",
		docsBranch: "feature/docs",
		navbar: [
			{
				text: "Guide",
				link: "/guide/",
			},
			{
				text: "API",
				children: [
					{ text: "Home", link: "/api/" },
					{ text: "Contributing", link: "/api/contributing.md" },
				],
			},
		],
	},

	bundler: "@vuepress/vite",
});
