<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const techniques = [
  "technique1",
  "technique2",
  "technique3",
  "technique4",
  "technique5",
];
const prompting = [
  { key: "zeroShot", hasExample: true },
  { key: "fewShot", hasExample: true },
  { key: "chainOfThought", hasExample: true },
];
const params = ["temperature", "maxTokens", "topP", "topK"];

const openSections = ref({
  techniquesSection: false,
  promptingSection: false,
  paramsSection: false,
});
const openItems = ref({});

function toggleSection(key) {
  openSections.value[key] = !openSections.value[key];
}

function toggleItem(key) {
  openItems.value[key] = !openItems.value[key];
}

function isSectionOpen(key) {
  return !!openSections.value[key];
}
function isItemOpen(key) {
  return !!openItems.value[key];
}

const emit = defineEmits(["copy-to-chat"]);

function copyToChat(text) {
  emit("copy-to-chat", text);
}
</script>

<template>
  <div class="method-panel">
    <!-- 1. Techniques for Structuring Prompts -->
    <section class="guide-section">
      <button class="section-header" @click="toggleSection('techniquesSection')">
        <span>{{ t("methods.techniquesSectionTitle") }}</span>
        <span class="chevron">{{ isSectionOpen('techniquesSection') ? "&#9650;" : "&#9660;" }}</span>
      </button>
      <div v-if="isSectionOpen('techniquesSection')" class="section-body">
        <p class="section-intro">{{ t("methods.techniquesIntro") }}</p>
        <div
          v-for="key in techniques"
          :key="key"
          class="method-item"
          :class="{ open: isItemOpen(key) }"
        >
          <button class="method-header" @click="toggleItem(key)">
            <span>{{ t(`methods.${key}Title`) }}</span>
            <span class="chevron">{{ isItemOpen(key) ? '&#9650;' : '&#9660;' }}</span>
          </button>
          <div v-if="isItemOpen(key)" class="method-body">
            {{ t(`methods.${key}Desc`) }}
          </div>
        </div>
      </div>
    </section>

    <!-- 2. Prompting Techniques with examples -->
    <section class="guide-section">
      <button class="section-header" @click="toggleSection('promptingSection')">
        <span>{{ t("methods.promptingSectionTitle") }}</span>
        <span class="chevron">{{ isSectionOpen('promptingSection') ? "&#9650;" : "&#9660;" }}</span>
      </button>
      <div v-if="isSectionOpen('promptingSection')" class="section-body">
        <div
          v-for="item in prompting"
          :key="item.key"
          class="method-item"
          :class="{ open: isItemOpen(item.key) }"
        >
          <button class="method-header" @click="toggleItem(item.key)">
            <span>{{ t(`methods.${item.key}Title`) }}</span>
            <span class="chevron">{{ isItemOpen(item.key) ? '&#9650;' : '&#9660;' }}</span>
          </button>
          <div v-if="isItemOpen(item.key)" class="method-body">
            <p>{{ t(`methods.${item.key}Desc`) }}</p>

            <template v-if="item.hasExample">
              <p class="example-label">{{ t("methods.tryIt") }}</p>
              <pre class="example-box">{{ t(`methods.${item.key}Example`) }}</pre>
              <button
                class="btn btn-secondary btn-xs"
                @click="copyToChat(t(`methods.${item.key}Example`))"
              >
                Copy to chat
              </button>
              <p class="suggested-params">{{ t("methods.suggestedParams") }} {{ t(`methods.${item.key}Params`) }}</p>
            </template>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Parameters for Controlling Output -->
    <section class="guide-section">
      <button class="section-header" @click="toggleSection('paramsSection')">
        <span>{{ t("methods.paramsSectionTitle") }}</span>
        <span class="chevron">{{ isSectionOpen('paramsSection') ? "&#9650;" : "&#9660;" }}</span>
      </button>
      <div v-if="isSectionOpen('paramsSection')" class="section-body">
        <div
          v-for="key in params"
          :key="key"
          class="method-item"
          :class="{ open: isItemOpen(key) }"
        >
          <button class="method-header" @click="toggleItem(key)">
            <span>{{ t(`methods.${key}Title`) }}</span>
            <span class="chevron">{{ isItemOpen(key) ? '&#9650;' : '&#9660;' }}</span>
          </button>
          <div v-if="isItemOpen(key)" class="method-body">
            {{ t(`methods.${key}Desc`) }}
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.method-panel {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.guide-section {
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--bg-card);
}
.section-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 14px;
  background: var(--bg-tertiary);
  border: none;
  color: var(--accent);
  font-size: 0.9rem;
  font-weight: 700;
  text-align: left;
  cursor: pointer;
}
.section-header:hover {
  background: var(--border);
}
.section-body {
  padding: 10px 12px 14px;
}
.section-intro {
  font-size: 0.82rem;
  color: var(--text-secondary);
  line-height: 1.55;
  margin-bottom: 10px;
  padding: 0 4px;
}
.method-item {
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  margin-top: 8px;
  transition: border-color var(--transition);
}
.method-item.open {
  border-color: var(--accent-hover);
}
.method-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 14px;
  background: var(--bg-tertiary);
  border: none;
  color: var(--text-primary);
  font-size: 0.88rem;
  font-weight: 600;
  text-align: left;
  cursor: pointer;
}
.chevron {
  font-size: 0.65rem;
  color: var(--text-muted);
}
.method-body {
  padding: 12px 14px;
  font-size: 0.82rem;
  color: var(--text-secondary);
  line-height: 1.6;
  background: var(--bg-card);
}
.method-body p {
  margin: 0 0 8px;
}
.example-label {
  font-weight: 600;
  color: var(--accent);
  font-size: 0.8rem;
  margin-top: 10px;
}
.example-box {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 10px 12px;
  font-size: 0.78rem;
  line-height: 1.5;
  white-space: pre-wrap;
  color: var(--text-primary);
  margin: 6px 0 8px;
  overflow-x: auto;
}
.suggested-params {
  font-size: 0.75rem;
  color: var(--text-muted);
  font-style: italic;
  margin-top: 6px;
}
.btn-xs {
  padding: 4px 10px;
  font-size: 0.72rem;
}
</style>
