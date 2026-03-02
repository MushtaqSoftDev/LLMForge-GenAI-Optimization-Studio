import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "../services/api";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(null);
  const user = ref(null);

  const isLoggedIn = computed(() => !!token.value);

  function tryLoadToken() {
    const saved = localStorage.getItem("token");
    if (saved) {
      token.value = saved;
      fetchUser();
    }
  }

  async function login(username, password) {
    const { data } = await api.post("/api/auth/login", { username, password });
    token.value = data.access_token;
    localStorage.setItem("token", data.access_token);
    await fetchUser();
  }

  async function signup(username, email, password) {
    const { data } = await api.post("/api/auth/signup", { username, email, password });
    token.value = data.access_token;
    localStorage.setItem("token", data.access_token);
    await fetchUser();
  }

  async function fetchUser() {
    try {
      const { data } = await api.get("/api/auth/me");
      user.value = data;
    } catch {
      logout();
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem("token");
  }

  return { token, user, isLoggedIn, tryLoadToken, login, signup, logout };
});
