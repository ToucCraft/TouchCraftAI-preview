import { ref } from 'vue';

const isOpen = ref(false);
const title = ref('');
const message = ref('');
const type = ref('info'); // 'success', 'error', 'warning', 'info'
const isConfirm = ref(false);
let resolvePromise = null;

export function useModal() {
    const showAlert = (newTitle, newMessage, newType = 'info') => {
        title.value = newTitle;
        message.value = newMessage;
        type.value = newType;
        isConfirm.value = false;
        isOpen.value = true;

        return new Promise((resolve) => {
            resolvePromise = resolve;
        });
    };

    const showConfirm = (newTitle, newMessage, newType = 'warning') => {
        title.value = newTitle;
        message.value = newMessage;
        type.value = newType;
        isConfirm.value = true;
        isOpen.value = true;

        return new Promise((resolve) => {
            resolvePromise = resolve;
        });
    };

    const closeAlert = (result = false) => {
        isOpen.value = false;
        if (resolvePromise) {
            resolvePromise(result);
            resolvePromise = null;
        }
    };

    return {
        isOpen,
        title,
        message,
        type,
        isConfirm,
        showAlert,
        showConfirm,
        closeAlert
    };
}