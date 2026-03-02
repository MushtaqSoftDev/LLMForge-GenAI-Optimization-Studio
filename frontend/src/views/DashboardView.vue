<script setup>
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const { t } = useI18n();
const router = useRouter();
const auth = useAuthStore();

const modules = [
  {
    key: "promptEng",
    route: "/prompt-engineering",
    icon: "&#9881;",
    active: true,
  },
  {
    key: "fineTuning",
    route: "/fine-tuning",
    icon: "&#128295;",
    active: true,
  },
  {
    key: "rl",
    route: null,
    icon: "&#129302;",
    active: false,
  },
];
</script>

<template>
  <div class="dashboard">
    <header class="dash-header">
      <h1>{{ t("dashboard.welcome", { name: auth.user?.username || "" }) }}</h1>
      <p class="subtitle">{{ t("dashboard.subtitle") }}</p>
    </header>

    <div class="module-grid">
      <div
        v-for="mod in modules"
        :key="mod.key"
        class="module-card card"
        :class="{ disabled: !mod.active }"
        @click="mod.active && router.push(mod.route)"
      >
        <div class="module-icon" v-html="mod.icon"></div>
        <h2>{{ t(`dashboard.${mod.key}Title`) }}</h2>
        <p>{{ t(`dashboard.${mod.key}Desc`) }}</p>
        <button v-if="mod.active" class="btn btn-primary">
          {{ t("dashboard.start") }}
        </button>
        <span v-else class="badge-soon">{{ t("dashboard.comingSoon") }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 960px;
  margin: 0 auto;
  padding: 40px 20px;
}
.dash-header {
  text-align: center;
  margin-bottom: 40px;
}
.dash-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
}
.subtitle {
  color: var(--text-secondary);
  margin-top: 8px;
}
.module-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
}
.module-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 12px;
  cursor: pointer;
  transition: border-color var(--transition), transform var(--transition);
}
.module-card:hover:not(.disabled) {
  border-color: var(--accent);
  transform: translateY(-2px);
}
.module-card.disabled {
  opacity: 0.5;
  cursor: default;
}
.module-icon {
  font-size: 2.5rem;
}
.module-card h2 {
  font-size: 1.15rem;
  font-weight: 600;
}
.module-card p {
  color: var(--text-secondary);
  font-size: 0.88rem;
  flex: 1;
}
.badge-soon {
  display: inline-block;
  padding: 4px 14px;
  border-radius: 20px;
  background: var(--bg-tertiary);
  color: var(--text-muted);
  font-size: 0.8rem;
  font-weight: 600;
}
</style>
