import { createApp } from 'vue';
import { createAuth0 } from '@auth0/auth0-vue';
import App from './App.vue';
import { router } from './router';
import './style.css';

const app = createApp(App);

app.use(
    createAuth0({
        domain: "dev-jj4vizuw0itq724l.us.auth0.com",
        clientId: "OgyAUbhKzGpy0hhnMsY4oOkLYeH1acjl",
        authorizationParams: {
            redirect_uri: window.location.origin,
            audience: "https://api-builder.touch-craft.com",
            scope: "openid profile email offline_access"
        },
        cacheLocation: 'localstorage',
        useRefreshTokens: true,

        onRedirectCallback: (appState) => {
            router.push(appState?.target || '/dashboard');
        }
    })
);

app.use(router);
app.mount('#app');