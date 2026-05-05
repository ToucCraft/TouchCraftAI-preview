import json
import os

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates", "vue_v1")


def flatten_for_lang(data, lang, fallback="en"):
    if isinstance(data, dict):
        keys = set(data.keys())
        if keys.intersection(['en', 'es', 'ru', 'fr', 'de', 'it', 'pt']):
            return data.get(lang, data.get(fallback, ""))
        return {k: flatten_for_lang(v, lang, fallback) for k, v in data.items()}
    elif isinstance(data, list):
        return [flatten_for_lang(item, lang, fallback) for item in data]
    return data


def generate_project_files(site_data: dict):
    translations = site_data.get("translations", {})
    if isinstance(translations, dict):
        available_langs = list(translations.keys())
    else:
        available_langs = []

    if not available_langs:
        available_langs = ["en"]

    main_lang = available_langs[0]

    base_data = flatten_for_lang(site_data, main_lang)

    business_name = str(base_data.get('business_name', 'Client Site'))

    safe_pkg_name = "".join(c for c in business_name.lower().replace(" ", "-") if c.isalnum() or c == '-')
    if not safe_pkg_name:
        safe_pkg_name = "site"

    palette = base_data.get('palette', {})
    if not isinstance(palette, dict):
        palette = {}

    font = str(base_data.get('font', 'Inter'))
    font_formatted = font.replace(' ', '+')

    analytics_id = base_data.get('analytics_id', '').strip()

    analytics_script = ""
    body_scripts = ""

    # 1. Google Analytics 4
    if analytics_id:
        analytics_script += f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={analytics_id}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());
          gtag('config', '{analytics_id}');
        </script>
    """

    style_css = f"""
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {{
  --color-primary: {palette.get('primary', '#3B82F6')};
  --color-secondary: {palette.get('secondary', '#10B981')};
  --color-bg: {palette.get('background', '#FFFFFF')};
  --color-text: {palette.get('text', '#1F2937')};
}}

html, body, #app {{
  background-color: var(--color-bg);
  color: var(--color-text);
  font-family: '{font}', sans-serif !important; 
}}"""

    package_json = {
        "name": f"site-{safe_pkg_name}",
        "version": "1.0.0",
        "type": "module",
        "scripts": {"dev": "vite", "build": "vite build", "preview": "vite preview"},
        "dependencies": {"vue": "^3.3.4", "axios": "^1.6.0"},
        "devDependencies": {
            "@vitejs/plugin-vue": "^4.2.3",
            "autoprefixer": "^10.4.14",
            "postcss": "^8.4.24",
            "tailwindcss": "^3.3.2",
            "vite": "^4.3.9"
        }
    }

    vite_config = "import { defineConfig } from 'vite'; import vue from '@vitejs/plugin-vue'; export default defineConfig({ plugins: [vue()], server: { host: '0.0.0.0', port: 80 }, preview: { host: '0.0.0.0', port: 80 } });"
    tailwind_config = f"""export default {{ 
            content: ['./index.html', './**/*.vue'], 
            theme: {{ 
                extend: {{ 
                    colors: {{ primary: 'var(--color-primary)', secondary: 'var(--color-secondary)', bg: 'var(--color-bg)', text: 'var(--color-text)' }},
                    fontFamily: {{ sans: ['"{font}"', 'sans-serif'] }},
                    animation: {{
                        'fade-in-up': 'fadeInUp 0.8s ease-out forwards',
                    }},
                    keyframes: {{
                        fadeInUp: {{
                            '0%': {{ opacity: '0', transform: 'translateY(20px)' }},
                            '100%': {{ opacity: '1', transform: 'translateY(0)' }},
                        }}
                    }}
                }} 
            }}, 
            plugins: [] 
        }}"""

    postcss_config = "export default { plugins: { tailwindcss: {}, autoprefixer: {} } }"

    favicon_url = str(base_data.get('favicon', '/vite.svg'))
    index_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{business_name}</title>
    <link rel="icon" href="{favicon_url}" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family={font_formatted}:wght@400;600;900&display=swap" rel="stylesheet">
    {analytics_script}
  </head>
  <body>
    <div id="app"></div>
    {body_scripts}
    <script type="module" src="/main.js"></script>
  </body>
</html>"""

    # 3. App.vue
    app_vue_path = os.path.join(TEMPLATES_DIR, "App.vue.template")
    if os.path.exists(app_vue_path):
        with open(app_vue_path, "r", encoding="utf-8") as f:
            app_vue = f.read()
            app_vue = app_vue.replace("{{ AVAILABLE_LANGUAGES_JSON }}", json.dumps(available_langs))
    else:
        app_vue = "<template><div>Error: App.vue.template missing</div></template>"

    # 4. Component Reader
    def read_component(category, name):
        if category:
            path_standard = os.path.join(TEMPLATES_DIR, "components", category, f"{name}.vue")
        else:
            path_standard = os.path.join(TEMPLATES_DIR, "components", f"{name}.vue")

        path_root = os.path.join(TEMPLATES_DIR, "components", f"{name}.vue")

        if os.path.exists(path_standard):
            with open(path_standard, "r", encoding="utf-8") as f:
                return f.read()
        elif os.path.exists(path_root):
            with open(path_root, "r", encoding="utf-8") as f:
                return f.read()

        print(f"⚠️ MISSING COMPONENT: {category}/{name}")
        return "<template><div class='p-4 border border-red-500 text-red-500'>Component Not Found: " + name + "</div></template>"

    # 5. Dockerfile
    dockerfile = """
FROM node:18-slim as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
RUN echo 'server { listen 80; root /usr/share/nginx/html; index index.html; location /assets/ { expires 1y; add_header Cache-Control "public, immutable"; } location / { try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""

    result_files = {
        "index.html": index_html,
        "robots.txt": "User-agent: *\nAllow: /\n",
        "main.js": "import { createApp } from 'vue'; import './style.css'; import App from './App.vue'; createApp(App).mount('#app');",
        "App.vue": app_vue,
        "style.css": style_css,
        "vite.config.js": vite_config,
        "tailwind.config.js": tailwind_config,
        "postcss.config.js": postcss_config,
        "package.json": json.dumps(package_json, indent=2),
        "Dockerfile": dockerfile,
        "site_config.json": json.dumps(site_data, indent=2, ensure_ascii=False),
    }

    for lang in available_langs:
        localized_site_data = flatten_for_lang(site_data, lang)

        if 'products' in site_data:
            filtered_products = []
            for prod in site_data['products']:
                if lang not in prod.get('excluded_langs', []):
                    flat_prod = flatten_for_lang(prod, lang)
                    filtered_products.append(flat_prod)
            localized_site_data['products'] = filtered_products

        result_files[f"site_{lang}.json"] = json.dumps(localized_site_data, indent=2, ensure_ascii=False)

    result_files["components/Header.vue"] = read_component("", "Header")

    for block in base_data.get('blocks', []):
        cat = block.get('category')
        typ = block.get('type')
        if cat and typ:
            path = f"components/{cat}/{typ}.vue"
            if path not in result_files:
                result_files[path] = read_component(cat, typ)

    result_files["components/Footer.vue"] = read_component("", "Footer")

    return result_files