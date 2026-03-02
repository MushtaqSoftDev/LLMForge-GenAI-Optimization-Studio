<script setup>
import { ref, nextTick, watch } from "vue";
import { useI18n } from "vue-i18n";
import { useChatStore } from "../stores/chat";

const { t } = useI18n();
const chat = useChatStore();

const input = ref("");
const messagesEl = ref(null);

function scrollBottom() {
  nextTick(() => {
    if (messagesEl.value) {
      messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
    }
  });
}

watch(() => chat.messages.length, scrollBottom);

async function send() {
  const text = input.value.trim();
  if (!text || chat.loading) return;
  input.value = "";
  await chat.sendMessage(text);
}

function selectSession(s) {
  chat.loadSession(s.id);
}

function setInput(text) {
  input.value = text;
}

defineExpose({ setInput });
</script>

<template>
  <div class="chat-layout">
    <!-- Session sidebar -->
    <div class="sessions-bar">
      <button
        class="btn btn-primary btn-sm full-w"
        :title="t('chat.newChatHint')"
        @click="chat.newChat()"
      >
        + {{ t("chat.newChat") }}
      </button>
      <p class="new-chat-hint">{{ t("chat.newChatHint") }}</p>
      <div class="sessions-list">
        <div
          v-for="s in chat.sessions"
          :key="s.id"
          class="session-item"
          :class="{ active: chat.currentSession?.id === s.id }"
          @click="selectSession(s)"
        >
          <span class="session-title">{{ s.title }}</span>
          <button
            class="session-del"
            @click.stop="chat.deleteSession(s.id)"
            title="Delete"
          >
            &times;
          </button>
        </div>
      </div>
    </div>

    <!-- Chat area -->
    <div class="chat-area">
      <div class="messages" ref="messagesEl">
        <div v-if="chat.messages.length === 0" class="empty-chat">
          <p>{{ t("chat.noMessages") }}</p>
        </div>
        <div
          v-for="msg in chat.messages"
          :key="msg.id"
          class="message"
          :class="msg.role"
        >
          <div class="msg-role">{{ msg.role }}</div>
          <div class="msg-content">{{ msg.content }}</div>
        </div>
        <div v-if="chat.loading" class="message assistant">
          <div class="msg-role">assistant</div>
          <div class="msg-content thinking">{{ t("chat.thinking") }}</div>
        </div>
      </div>

      <div v-if="chat.error" class="chat-error">
        {{ t("chat.errorPrefix") }}: {{ chat.error }}
      </div>

      <form class="chat-input-bar" @submit.prevent="send">
        <input
          v-model="input"
          type="text"
          class="input-field"
          :placeholder="t('chat.placeholder')"
          :disabled="chat.loading"
        />
        <button type="submit" class="btn btn-primary" :disabled="chat.loading || !input.trim()">
          {{ t("chat.send") }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.chat-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* sessions sidebar */
.sessions-bar {
  width: 200px;
  border-right: 1px solid var(--border);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: var(--bg-primary);
  flex-shrink: 0;
  overflow-y: auto;
}
.new-chat-hint {
  font-size: 0.7rem;
  color: var(--text-muted);
  line-height: 1.35;
  margin: 0;
}
.sessions-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.session-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 10px;
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 0.82rem;
  color: var(--text-secondary);
  transition: background var(--transition);
}
.session-item:hover,
.session-item.active {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}
.session-title {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
}
.session-del {
  background: none;
  border: none;
  color: var(--text-muted);
  font-size: 1.1rem;
  padding: 0 4px;
  display: none;
}
.session-item:hover .session-del {
  display: block;
}

/* chat area */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.empty-chat {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
}
.message {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: var(--radius-lg);
  line-height: 1.5;
  font-size: 0.9rem;
  white-space: pre-wrap;
}
.message.user {
  align-self: flex-end;
  background: var(--accent);
  color: #fff;
}
.message.assistant {
  align-self: flex-start;
  background: var(--bg-tertiary);
  color: var(--text-primary);
}
.msg-role {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  opacity: 0.6;
  margin-bottom: 4px;
}
.thinking {
  animation: pulse 1.2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.chat-error {
  padding: 8px 20px;
  background: rgba(239, 83, 80, 0.12);
  color: var(--danger);
  font-size: 0.85rem;
}

.chat-input-bar {
  display: flex;
  gap: 8px;
  padding: 12px 20px;
  border-top: 1px solid var(--border);
  background: var(--bg-secondary);
}
.chat-input-bar .input-field {
  flex: 1;
}
.btn-sm {
  padding: 6px 12px;
  font-size: 0.8rem;
}
.full-w {
  width: 100%;
}

@media (max-width: 1024px) {
  .sessions-bar {
    display: none;
  }
}
</style>
