<script setup>
import { useI18n } from "vue-i18n";

const { locale } = useI18n();

const languages = [
  { code: "en", label: "EN" },
  { code: "es", label: "ES" },
  { code: "ca", label: "CA" },
  { code: "de", label: "DE" },
  { code: "fr", label: "FR" },
  { code: "ar", label: "AR" },
  { code: "ur", label: "UR" },
  { code: "hi", label: "HI" },
];

const rtlLocales = new Set(["ar", "ur"]);

function setLocale(code) {
  locale.value = code;
  localStorage.setItem("locale", code);
  document.documentElement.dir = rtlLocales.has(code) ? "rtl" : "ltr";
}
</script>

<template>
  <div class="lang-switcher">
    <button
      v-for="lang in languages"
      :key="lang.code"
      class="lang-btn"
      :class="{ active: locale === lang.code }"
      @click="setLocale(lang.code)"
    >
      {{ lang.label }}
    </button>
  </div>
</template>

<style scoped>
.lang-switcher {
  display: flex;
  gap: 2px;
  background: var(--bg-tertiary);
  border-radius: var(--radius);
  padding: 2px;
}
.lang-btn {
  padding: 4px 10px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: var(--text-muted);
  font-size: 0.75rem;
  font-weight: 600;
  transition: all var(--transition);
}
.lang-btn:hover {
  color: var(--text-primary);
}
.lang-btn.active {
  background: var(--accent);
  color: #fff;
}
</style>
