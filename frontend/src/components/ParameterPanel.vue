<script setup>
import { useI18n } from "vue-i18n";
import { useChatStore } from "../stores/chat";

const { t } = useI18n();
const chat = useChatStore();
</script>

<template>
  <div class="param-panel">
    <h3 class="panel-title">{{ t("params.title") }}</h3>

    <!-- Provider -->
    <div class="param-group">
      <label>{{ t("params.provider") }}</label>
      <select v-model="chat.params.provider" class="input-field" :disabled="chat.providersLoading">
        <option v-if="chat.providers.length === 0" value="huggingface">{{ chat.providersLoading ? "Loading…" : "HuggingFace (free)" }}</option>
        <option
          v-for="p in chat.providers"
          :key="p.name"
          :value="p.name"
          :disabled="!p.available"
        >
          {{ p.label }}
          <template v-if="!p.available"> ({{ t("provider.unavailable") }})</template>
        </option>
      </select>
      <p v-if="chat.providersError" class="param-hint param-error">{{ chat.providersError }}</p>
      <p v-else class="param-hint">{{ t("params.apiKeyHint") }}</p>
    </div>

    <!-- Temperature -->
    <div class="param-group">
      <label>
        {{ t("params.temperature") }}
        <span class="param-value">{{ chat.params.temperature.toFixed(1) }}</span>
      </label>
      <input
        v-model.number="chat.params.temperature"
        type="range"
        min="0"
        max="2"
        step="0.1"
        class="slider"
      />
      <div class="range-labels">
        <span>0.0</span><span>1.0</span><span>2.0</span>
      </div>
    </div>

    <!-- Max Tokens -->
    <div class="param-group">
      <label>
        {{ t("params.maxTokens") }}
        <span class="param-value">{{ chat.params.max_tokens }}</span>
      </label>
      <input
        v-model.number="chat.params.max_tokens"
        type="range"
        min="1"
        max="4096"
        step="1"
        class="slider"
      />
      <div class="range-labels">
        <span>1</span><span>2048</span><span>4096</span>
      </div>
    </div>

    <!-- Top P -->
    <div class="param-group">
      <label>
        {{ t("params.topP") }}
        <span class="param-value">{{ chat.params.top_p.toFixed(2) }}</span>
      </label>
      <input
        v-model.number="chat.params.top_p"
        type="range"
        min="0"
        max="1"
        step="0.05"
        class="slider"
      />
      <div class="range-labels">
        <span>0.0</span><span>0.5</span><span>1.0</span>
      </div>
    </div>

    <!-- Top K -->
    <div class="param-group">
      <label>
        {{ t("params.topK") }}
        <span class="param-value">{{ chat.params.top_k }}</span>
      </label>
      <input
        v-model.number="chat.params.top_k"
        type="range"
        min="1"
        max="100"
        step="1"
        class="slider"
      />
      <div class="range-labels">
        <span>1</span><span>50</span><span>100</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.param-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.panel-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--accent);
}
.param-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.param-group label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-secondary);
}
.param-value {
  font-family: monospace;
  color: var(--accent);
  font-size: 0.9rem;
}
.param-hint {
  font-size: 0.7rem;
  color: var(--text-muted);
  line-height: 1.3;
  margin: 0;
}
.param-error {
  color: var(--danger, #c00);
}

/* Slider */
.slider {
  -webkit-appearance: none;
  appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: var(--bg-tertiary);
  outline: none;
}
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid var(--bg-secondary);
  transition: transform var(--transition);
}
.slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
}
.slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid var(--bg-secondary);
}

.range-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: var(--text-muted);
}
</style>
