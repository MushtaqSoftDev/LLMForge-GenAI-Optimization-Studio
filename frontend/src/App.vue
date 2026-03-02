<script setup>
import NavBar from "./components/NavBar.vue";
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();
auth.tryLoadToken();
</script>

<template>
  <div class="app-shell" :dir="['ar', 'ur'].includes($i18n.locale) ? 'rtl' : 'ltr'">
    <NavBar v-if="auth.isLoggedIn" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
