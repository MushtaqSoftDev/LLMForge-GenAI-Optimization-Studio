import { defineStore } from "pinia";
import { ref } from "vue";
import api from "../services/api";
import { getFriendlyAuthError } from "../utils/errors";

function toFriendlyError(msg) {
  if (typeof msg !== "string") return "Something went wrong";
  const m = msg.toLowerCase();
  if (
    m.includes("401") ||
    m.includes("authentication fail") ||
    (m.includes("invalid") && (m.includes("api key") || m.includes("authentication")))
  ) {
    return "Invalid or expired API key. Try another provider (e.g. Groq or free HuggingFace), or check your API key in .env.";
  }
  if (m.includes("429") || m.includes("rate limit") || m.includes("quota")) {
    return "Rate limit or free tier exhausted. Try another provider, or wait a moment and try again.";
  }
  return msg;
}

export const useChatStore = defineStore("chat", () => {
  const sessions = ref([]);
  const currentSession = ref(null);
  const messages = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const providers = ref([]);
  const providersLoading = ref(false);
  const providersError = ref(null);

  /** Fallback so the dropdown is never empty if the API fails or is slow */
  const FALLBACK_PROVIDERS = [
    { name: "huggingface", label: "HuggingFace (free)", available: true },
    { name: "openai", label: "OpenAI", available: false },
    { name: "groq", label: "Groq", available: false },
    { name: "deepseek", label: "DeepSeek", available: false },
    { name: "gemini", label: "Gemini", available: false },
  ];

  const params = ref({
    provider: "huggingface",
    max_tokens: 64,
    temperature: 0.7,
    top_p: 0.9,
    top_k: 50,
  });

  async function fetchProviders() {
    providersLoading.value = true;
    providersError.value = null;
    try {
      const { data } = await api.get("/api/providers/");
      if (Array.isArray(data) && data.length) {
        providers.value = data;
        const available = data.find((p) => p.available);
        if (available) params.value.provider = available.name;
      } else if (providers.value.length === 0) {
        providers.value = FALLBACK_PROVIDERS;
      }
    } catch (e) {
      providersError.value = getFriendlyAuthError(e, "Could not load providers.");
      // Keep existing list so Prompt-eng is not affected by fine-tune or temporary 502
      if (providers.value.length === 0) {
        providers.value = FALLBACK_PROVIDERS;
      }
    } finally {
      providersLoading.value = false;
    }
  }

  async function fetchSessions() {
    const { data } = await api.get("/api/chat/sessions");
    sessions.value = data;
  }

  async function loadSession(sessionId) {
    const { data } = await api.get(`/api/chat/sessions/${sessionId}`);
    currentSession.value = data;
    messages.value = data.messages;
  }

  function newChat() {
    currentSession.value = null;
    messages.value = [];
    error.value = null;
  }

  async function sendMessage(text) {
    error.value = null;
    loading.value = true;

    messages.value.push({ role: "user", content: text, id: Date.now() });

    try {
      const { data } = await api.post("/api/chat/send", {
        session_id: currentSession.value?.id || null,
        provider: params.value.provider,
        message: text,
        params: {
          max_tokens: params.value.max_tokens,
          temperature: params.value.temperature,
          top_p: params.value.top_p,
          top_k: params.value.top_k,
        },
      });

      if (!currentSession.value) {
        currentSession.value = { id: data.session_id };
        await fetchSessions();
      }

      messages.value.push(data.reply);
    } catch (err) {
      const raw = err.response?.data?.detail ?? err.message ?? "Something went wrong";
      error.value = toFriendlyError(Array.isArray(raw) ? raw[0]?.msg ?? String(raw) : raw);
    } finally {
      loading.value = false;
    }
  }

  async function deleteSession(sessionId) {
    await api.delete(`/api/chat/sessions/${sessionId}`);
    if (currentSession.value?.id === sessionId) newChat();
    await fetchSessions();
  }

  return {
    sessions,
    currentSession,
    messages,
    loading,
    error,
    providers,
    providersLoading,
    providersError,
    params,
    fetchProviders,
    fetchSessions,
    loadSession,
    newChat,
    sendMessage,
    deleteSession,
  };
});
