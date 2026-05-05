import axios from 'axios';
import { router } from '../router';

const api = axios.create({
    baseURL: 'https://api-builder.touch-craft.com/api/v1'
});

// Глобальная переменная для хранения функции получения токена (установим в App.vue)
let getAccessToken = null;
export const setTokenFetcher = (fetcher) => { getAccessToken = fetcher; };

export const setAuthToken = (token) => {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
};

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (error.response && error.response.status === 401 && !originalRequest._retry && getAccessToken) {
            originalRequest._retry = true;
            try {
                const newToken = await getAccessToken({ ignoreCache: true });
                setAuthToken(newToken);
                originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
                return api(originalRequest);
            } catch (refreshError) {
                console.error("Session expired");
            }
        }

        if (error.response && error.response.status === 403) {
            router.push('/waiting');
        }
        return Promise.reject(error);
    }
);

export default api;