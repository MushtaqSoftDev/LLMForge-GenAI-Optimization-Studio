<script setup>
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import LanguageSwitcher from "./LanguageSwitcher.vue";

const { t } = useI18n();
const router = useRouter();
const auth = useAuthStore();

function logout() {
  auth.logout();
  router.push("/login");
}
</script>

<template>
  <nav class="navbar">
    <div class="nav-left">
      <router-link to="/dashboard" class="nav-brand">{{ t("app.title") }}</router-link>
      <router-link to="/dashboard" class="nav-link">{{ t("nav.dashboard") }}</router-link>
      <router-link to="/prompt-engineering" class="nav-link">{{ t("nav.promptEng") }}</router-link>
      <router-link to="/fine-tuning" class="nav-link">{{ t("nav.fineTuning") }}</router-link>
    </div>
    <div class="nav-right">
      <LanguageSwitcher />
      <span class="nav-user">{{ auth.user?.username }}</span>
      <button class="btn btn-secondary btn-sm" @click="logout">{{ t("nav.logout") }}</button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 56px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}
.nav-left,
.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}
.nav-brand {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--accent);
}
.nav-brand:hover {
  text-decoration: none;
}
.nav-link {
  font-size: 0.88rem;
  color: var(--text-secondary);
  transition: color var(--transition);
}
.nav-link:hover,
.nav-link.router-link-active {
  color: var(--text-primary);
  text-decoration: none;
}
.nav-user {
  font-size: 0.85rem;
  color: var(--text-secondary);
}
.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}
</style>
