<script setup>
import { onMounted, ref } from "vue";
import { useChatStore } from "../stores/chat";
import MethodDescriptions from "../components/MethodDescriptions.vue";
import ChatWindow from "../components/ChatWindow.vue";
import ParameterPanel from "../components/ParameterPanel.vue";

const chat = useChatStore();
const chatWindowRef = ref(null);

onMounted(async () => {
  await chat.fetchProviders();
  await chat.fetchSessions();
});

function handleCopyToChat(text) {
  if (chatWindowRef.value) {
    chatWindowRef.value.setInput(text);
  }
}
</script>

<template>
  <div class="prompt-eng">
    <aside class="left-panel">
      <MethodDescriptions @copy-to-chat="handleCopyToChat" />
    </aside>

    <section class="center-panel">
      <ChatWindow ref="chatWindowRef" />
    </section>

    <aside class="right-panel">
      <ParameterPanel />
    </aside>
  </div>
</template>

<style scoped>
.prompt-eng {
  flex: 1;
  display: grid;
  grid-template-columns: 280px 1fr 300px;
  gap: 0;
  height: calc(100vh - 56px);
  overflow: hidden;
}
.left-panel {
  border-right: 1px solid var(--border);
  overflow-y: auto;
  padding: 20px;
  background: var(--bg-secondary);
}
.center-panel {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.right-panel {
  border-left: 1px solid var(--border);
  overflow-y: auto;
  padding: 20px;
  background: var(--bg-secondary);
}

@media (max-width: 1024px) {
  .prompt-eng {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }
  .left-panel {
    display: none;
  }
  .right-panel {
    border-left: none;
    border-top: 1px solid var(--border);
    max-height: 300px;
  }
}
</style>
