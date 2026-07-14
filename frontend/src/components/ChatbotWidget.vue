<script setup>
import { ref, nextTick, computed } from "vue";
import { useRoute } from "vue-router";
import { fetchChatbotSummary } from "../api/chatbot";

const route = useRoute();

// 현재 라우트의 placeId 파라미터 → 있으면 Number, 없으면(지도 홈) null
const placeId = computed(() => {
  const raw = route.params.placeId;
  return raw != null ? Number(raw) : null;
});

const isOpen = ref(false);
const messages = ref([]); // { id, role: "user" | "bot", text }
const draft = ref("");
const isLoading = ref(false);
const hasLoadedInitial = ref(false);

const messageArea = ref(null);
const inputEl = ref(null);
let messageSeq = 0;

function scrollToBottom() {
  nextTick(() => {
    const el = messageArea.value;
    if (el) {
      el.scrollTop = el.scrollHeight;
    }
  });
}

function pushMessage(role, text) {
  messages.value.push({ id: ++messageSeq, role, text });
  scrollToBottom();
}

// 요약 요청 공통 처리 (question 없으면 기본 동향 요약)
async function requestSummary(question) {
  isLoading.value = true;
  try {
    const { summary } = await fetchChatbotSummary({
      place_id: placeId.value,
      question,
    });
    pushMessage("bot", summary);
  } catch (error) {
    if (error.response?.status === 500) {
      pushMessage("bot", "현재 일시적인 오류로 요약을 불러올 수 없습니다.");
    } else {
      pushMessage("bot", error.detail ?? "동향 요약을 불러오지 못했어요. 잠시 후 다시 시도해 주세요.");
    }
  } finally {
    isLoading.value = false;
  }
}

async function togglePanel() {
  isOpen.value = !isOpen.value;
  if (isOpen.value) {
    // 최초 열 때 기본 동향 요약 자동 호출 (와이어프레임 D 플로우)
    if (!hasLoadedInitial.value) {
      hasLoadedInitial.value = true;
      await requestSummary();
    }
    nextTick(() => inputEl.value?.focus());
  }
}

function closePanel() {
  isOpen.value = false;
}

async function sendQuestion() {
  const question = draft.value.trim();
  if (!question || isLoading.value) return;
  draft.value = "";
  pushMessage("user", question);
  await requestSummary(question);
}

function onKeydown(event) {
  if (event.key === "Escape" && isOpen.value) {
    closePanel();
  }
}
</script>

<template>
  <div class="chatbot" @keydown="onKeydown">
    <transition name="panel">
      <section
        v-if="isOpen"
        class="chatbot-panel card"
        role="dialog"
        aria-label="동향 요약 챗봇"
      >
        <header class="chatbot-header">
          <h4 class="chatbot-title">동향 요약</h4>
          <button
            type="button"
            class="chatbot-close"
            aria-label="챗봇 닫기"
            @click="closePanel"
          >
            &times;
          </button>
        </header>

        <div ref="messageArea" class="chatbot-messages">
          <div
            v-for="message in messages"
            :key="message.id"
            class="chatbot-row"
            :class="message.role === 'user' ? 'chatbot-row-user' : 'chatbot-row-bot'"
          >
            <p
              class="chatbot-bubble"
              :class="message.role === 'user' ? 'chatbot-bubble-user' : 'chatbot-bubble-bot'"
            >
              {{ message.text }}
            </p>
          </div>

          <div v-if="isLoading" class="chatbot-row chatbot-row-bot">
            <p class="chatbot-bubble chatbot-bubble-bot chatbot-bubble-loading">
              답변을 준비하고 있어요...
            </p>
          </div>
        </div>

        <form class="chatbot-input" @submit.prevent="sendQuestion">
          <input
            ref="inputEl"
            v-model="draft"
            class="field-input"
            type="text"
            placeholder="질문 입력..."
            aria-label="질문 입력"
            :disabled="isLoading"
          />
          <button
            type="submit"
            class="btn btn-primary chatbot-send"
            :disabled="isLoading || !draft.trim()"
          >
            전송
          </button>
        </form>
      </section>
    </transition>

    <button
      type="button"
      class="chatbot-toggle"
      :aria-label="isOpen ? '챗봇 닫기' : '동향 요약 챗봇 열기'"
      :aria-expanded="isOpen"
      @click="togglePanel"
    >
      <svg
        v-if="!isOpen"
        width="26"
        height="26"
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H8l-4 4V5a1 1 0 0 1 1-1Z"
          fill="currentColor"
        />
      </svg>
      <svg
        v-else
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
      >
        <path
          d="M6 6l12 12M18 6L6 18"
          stroke="currentColor"
          stroke-width="2.4"
          stroke-linecap="round"
        />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.chatbot {
  position: fixed;
  right: var(--space-xl);
  bottom: var(--space-xl);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-md);
}

.chatbot-toggle {
  width: 56px;
  height: 56px;
  border: none;
  border-radius: 50%;
  background: var(--color-primary);
  color: var(--color-on-primary);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 2px solid var(--color-canvas);
  transition: background-color 0.15s ease, transform 0.15s ease;
  align-self: flex-end;
}

.chatbot-toggle:hover {
  background: var(--color-primary-hover);
  transform: translateY(-2px);
}

.chatbot-panel {
  width: 360px;
  height: 480px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chatbot-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg);
  border-bottom: 1px solid var(--color-border);
}

.chatbot-title {
  font-size: var(--font-h4-size);
  font-weight: var(--font-h4-weight);
  color: var(--color-foreground);
}

.chatbot-close {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: var(--color-muted);
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  border-radius: var(--radius-sm);
}

.chatbot-close:hover {
  background: var(--color-surface);
  color: var(--color-body);
}

.chatbot-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.chatbot-row {
  display: flex;
}

.chatbot-row-user {
  justify-content: flex-end;
}

.chatbot-row-bot {
  justify-content: flex-start;
}

.chatbot-bubble {
  max-width: 80%;
  padding: var(--space-md) var(--space-lg);
  border-radius: var(--radius-button-lg);
  font-size: var(--font-body-small-size);
  line-height: var(--font-body-small-line-height);
  word-break: break-word;
  white-space: pre-wrap;
}

.chatbot-bubble-user {
  background: var(--color-primary);
  color: var(--color-on-primary);
  border-bottom-right-radius: var(--radius-sm);
}

.chatbot-bubble-bot {
  background: var(--color-surface);
  color: var(--color-body);
  border-bottom-left-radius: var(--radius-sm);
}

.chatbot-bubble-loading {
  color: var(--color-muted);
}

.chatbot-input {
  display: flex;
  gap: var(--space-md);
  padding: var(--space-lg);
  border-top: 1px solid var(--color-border);
}

.chatbot-input .field-input {
  height: 40px;
}

.chatbot-send {
  flex-shrink: 0;
  padding: 0 var(--space-lg);
}

.panel-enter-active,
.panel-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.panel-enter-from,
.panel-leave-to {
  opacity: 0;
  transform: translateY(12px);
}
</style>
