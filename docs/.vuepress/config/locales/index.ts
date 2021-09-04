import { LocaleConfig } from "@vuepress/shared";
import { DefaultThemeLocaleOptions } from "@vuepress/theme-default";
import navbar from "./navbar";

const localesEn: DefaultThemeLocaleOptions = {
	navbar: navbar.en,
};

const localesPt: DefaultThemeLocaleOptions = {
	// Navbar
	navbar: navbar.pt,
	selectLanguageName: "Português (Brasil)",
	selectLanguageText: "Linguagens",
	selectLanguageAriaLabel: "Português (Brasil)",

	// Cards
	tip: "Dica",
	warning: "Aviso",
	danger: "Cuidado",

	// Page meta
	editLinkText: "Edite esta página no GitHub",
	lastUpdatedText: "Última atualização em",
	contributorsText: "Contribuidores",

	// 404 page
	notFound: [
		"Página não encontrada",
		"Como chegou aqui?",
		"Isto é um erro Quatro-Zero-Quatro",
		"Vish",
	],
	backToHome: "Me leve de volta",

	// Ally
	openInNewWindow: "Abrir em uma nova guia",
	toggleDarkMode: "Alternar para modo escuro",
	toggleSidebar: "Alternar barra lateral",

	serviceWorker: {
		updatePopup: {
			message: "Novo conteúdo está disponível.",
			buttonText: "Atualizar",
		},
	},
};

export const locales: LocaleConfig = {
	locales: {
		"/": localesEn,
		"/pt/": localesPt,
	},
};
