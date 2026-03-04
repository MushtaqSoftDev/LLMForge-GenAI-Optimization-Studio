<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useAuthStore } from "../stores/auth";
import { getFriendlyAuthError } from "../utils/errors";
import api from "../services/api";
import LanguageSwitcher from "../components/LanguageSwitcher.vue";

const { t } = useI18n();
const router = useRouter();
const auth = useAuthStore();

const username = ref("");
const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const demoModeNote = ref(false);
onMounted(async () => {
  try {
    const { data } = await api.get("/api/config");
    if (data && data.persist_accounts === false) demoModeNote.value = true;
  } catch {
    // ignore
  }
});

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.signup(username.value, email.value, password.value);
    router.push({ path: "/login", query: { registered: "1" } });
  } catch (err) {
    error.value = getFriendlyAuthError(err, "We couldn't create your account. Please try again.");
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-wrapper">
      <div class="lang-corner"><LanguageSwitcher /></div>

      <div class="auth-card card">
        <h1 class="auth-title">{{ t("app.title") }}</h1>
        <h2 class="auth-subtitle">{{ t("auth.signup") }}</h2>
        <p v-if="demoModeNote" class="demo-mode-note">{{ t("auth.demoModeNote") }}</p>

        <form @submit.prevent="submit" class="auth-form">
          <div class="field">
            <label>{{ t("auth.username") }}</label>
            <input
              v-model="username"
              type="text"
              class="input-field"
              required
              autocomplete="username"
            />
          </div>
          <div class="field">
            <label>{{ t("auth.email") }}</label>
            <input
              v-model="email"
              type="email"
              class="input-field"
              required
              autocomplete="email"
            />
          </div>
          <div class="field">
            <label>{{ t("auth.password") }}</label>
            <input
              v-model="password"
              type="password"
              class="input-field"
              required
              minlength="6"
              autocomplete="new-password"
            />
          </div>

          <p v-if="error" class="error-msg">{{ error }}</p>

          <button type="submit" class="btn btn-primary full-w" :disabled="loading">
            {{ loading ? "…" : t("auth.signupBtn") }}
          </button>
        </form>

        <p class="auth-switch">
          {{ t("auth.haveAccount") }}
          <router-link to="/login">{{ t("auth.login") }}</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
}
.auth-wrapper {
  position: relative;
  width: 100%;
  max-width: 420px;
  padding: 20px;
}
.lang-corner {
  position: absolute;
  top: 0;
  right: 20px;
}
.auth-card {
  text-align: center;
}
.auth-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 4px;
}
.auth-subtitle {
  font-size: 1rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: 24px;
}
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.field {
  text-align: left;
}
.field label {
  display: block;
  font-size: 0.85rem;
  color: var(--text-secondary);
  margin-bottom: 6px;
}
.full-w {
  width: 100%;
}
.demo-mode-note {
  font-size: 0.8rem;
  color: var(--text-muted);
  line-height: 1.4;
  margin-bottom: 12px;
  padding: 8px 10px;
  background: var(--bg-tertiary, #f0f0f0);
  border-radius: var(--radius, 6px);
}
.error-msg {
  color: var(--danger);
  font-size: 0.85rem;
}
.auth-switch {
  margin-top: 16px;
  font-size: 0.85rem;
  color: var(--text-secondary);
}
</style>
