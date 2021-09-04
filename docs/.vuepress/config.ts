import { defineUserConfig } from "vuepress";
import type { DefaultThemeOptions } from "vuepress";
import { locales } from './config/locales'

export default defineUserConfig<DefaultThemeOptions>({
	base: "/mob/",

	head: [
    [
      'link',
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '16x16',
        href: '/images/icons/favicon-16x16.png',
      },
    ],
    [
      'link',
      {
        rel: 'icon',
        type: 'image/png',
        sizes: '32x32',
        href: '/images/icons/favicon-32x32.png',
      },
    ],
    ['link', { rel: 'manifest', href: '/manifest.webmanifest' }],
    ['meta', { name: 'application-name', content: 'Mob' }],
    ['meta', { name: 'apple-mobile-web-app-title', content: 'Mob' }],
    [
      'meta',
      { name: 'apple-mobile-web-app-status-bar-style', content: 'black' },
    ],
    [
      'link',
      { rel: 'apple-touch-icon', href: `/images/icons/apple-touch-icon.png` },
    ],
  ],


	themeConfig: {
		docsRepo: "lsglucas/mob",
		docsBranch: "master",
		repoLabel: "lsglucas/mob",
		lastUpdated: true,


		logo: 'images/rlogo.png',


		...locales,

	},

	locales: {
		"/": {
			lang: "en-US",
			title: "Mob",
			description: "Moodle Organizer bot documentation",
		},
		"/pt/": {
			lang: "pt-BR",
			title: "Mob",
			description: "Documentação do Moodle organizer bot",
		}
	},

	// plugins: [
  //   [
  //     '@vuepress/plugin-search',
  //     {
  //       locales: {
  //         '/': {
  //           placeholder: 'Search',
  //         },
  //         '/pt/': {
  //           placeholder: 'Buscar',
  //         },
  //       },
  //     },
  //   ],
	// ],
	
	bundlerConfig: {
    viteOptions: {
			logLevel: 'warning',
    },
  },


	bundler: "@vuepress/vite",
});
