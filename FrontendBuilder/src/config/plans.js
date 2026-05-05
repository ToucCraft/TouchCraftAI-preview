export const PLAN_LIMITS = {
    freemium: {
        max_sites: 1,
        max_languages: 1,
        custom_domains: false,
        ai_generations: false,
        lead_forms: false,
        catalogs: false
    },
    starter: {
        max_sites: 5,
        max_languages: 3,
        custom_domains: true,
        ai_generations: true,
        lead_forms: true,
        catalogs: false
    },
    pro: {
        max_sites: 10,
        max_languages: 7,
        custom_domains: true,
        ai_generations: true,
        lead_forms: true,
        catalogs: true
    }
};