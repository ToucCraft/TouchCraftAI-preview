import { ref, computed } from 'vue';
import { PLAN_LIMITS } from '../config/plans';

const showUpgradeModal = ref(false);
const upgradeMessage = ref('');
const requiredTier = ref('starter');
const currentUserTier = ref('freemium');
const currentUserStats = ref({ project_count: 0, active_project_count: 0, ai_generations_used: 0 });

export function useSubscription() {
    const currentLimits = computed(() => PLAN_LIMITS[currentUserTier.value] || PLAN_LIMITS.freemium);

    const updateUserData = (userData) => {
        currentUserTier.value = (userData.subscription_tier || 'freemium').toLowerCase();
        currentUserStats.value.project_count = userData.project_count || 0;
        currentUserStats.value.active_project_count = userData.active_project_count || 0;
        currentUserStats.value.ai_generations_used = userData.ai_generations_used || 0;
    };

    const triggerUpgrade = (message, tier = 'starter') => {
        upgradeMessage.value = message;
        requiredTier.value = tier;
        showUpgradeModal.value = true;
    };

    const checkLimit = (feature) => {
        const limits = currentLimits.value;

        if (typeof limits[feature] === 'boolean') {
            return limits[feature];
        }

        if (typeof limits[feature] === 'number') {
            if (feature === 'max_sites') {
                return currentUserStats.value.active_project_count < limits[feature];
            }
        }
        return true;
    };

    return {
        showUpgradeModal,
        upgradeMessage,
        requiredTier,
        currentUserTier,
        currentLimits,
        checkLimit,
        triggerUpgrade,
        updateUserData,
        currentUserStats
    };
}