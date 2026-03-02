import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

import LoginView from "../views/LoginView.vue";
import SignupView from "../views/SignupView.vue";
import DashboardView from "../views/DashboardView.vue";
import PromptEngView from "../views/PromptEngView.vue";
import FineTuningView from "../views/FineTuningView.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "Login", component: LoginView, meta: { guest: true } },
  { path: "/signup", name: "Signup", component: SignupView, meta: { guest: true } },
  { path: "/dashboard", name: "Dashboard", component: DashboardView, meta: { auth: true } },
  { path: "/prompt-engineering", name: "PromptEng", component: PromptEngView, meta: { auth: true } },
  { path: "/fine-tuning", name: "FineTuning", component: FineTuningView, meta: { auth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.auth && !auth.isLoggedIn) return { name: "Login" };
  if (to.meta.guest && auth.isLoggedIn) return { name: "Dashboard" };
});

export default router;
