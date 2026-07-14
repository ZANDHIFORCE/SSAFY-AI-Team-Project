<script setup>
import { computed, ref, watch } from "vue";
import { useRouter } from "vue-router";
import { fetchPlace } from "../api/places";
import { fetchPost, createPost, updatePost } from "../api/posts";

const props = defineProps({
  placeId: { type: [String, Number], required: true },
  postId: { type: [String, Number], default: null },
});

const router = useRouter();

const isEdit = computed(() => props.postId != null);

const placeName = ref("");

const nickname = ref("");
const password = ref("");
const title = ref("");
const content = ref("");

const submitting = ref(false);
const formError = ref("");
const prefillError = ref("");

const passwordValid = computed(() => /^\d{4}$/.test(password.value));
const canSubmit = computed(
  () =>
    passwordValid.value &&
    title.value.trim() !== "" &&
    content.value.trim() !== "" &&
    !submitting.value,
);

async function loadPlace() {
  try {
    const place = await fetchPlace(props.placeId);
    placeName.value = place.name;
  } catch {
    placeName.value = "";
  }
}

async function loadPostForEdit() {
  prefillError.value = "";
  try {
    const post = await fetchPost(props.placeId, props.postId);
    title.value = post.title;
    content.value = post.content;
  } catch (err) {
    prefillError.value = err.detail ?? "게시글을 불러오지 못했습니다.";
  }
}

function onPasswordInput(event) {
  password.value = event.target.value.replace(/\D/g, "").slice(0, 4);
}

async function onSubmit() {
  if (!canSubmit.value) return;

  submitting.value = true;
  formError.value = "";

  try {
    if (isEdit.value) {
      await updatePost(props.placeId, props.postId, {
        password: password.value,
        title: title.value.trim(),
        content: content.value.trim(),
      });
      router.push({
        name: "post-detail",
        params: { placeId: props.placeId, postId: props.postId },
      });
    } else {
      await createPost(props.placeId, {
        nickname: nickname.value.trim() || "익명",
        password: password.value,
        title: title.value.trim(),
        content: content.value.trim(),
      });
      router.push({ name: "board-list", params: { placeId: props.placeId } });
    }
  } catch (err) {
    if (err.response?.status === 403) {
      formError.value = "비밀번호가 일치하지 않습니다.";
    } else {
      formError.value = err.detail ?? "요청을 처리하지 못했습니다.";
    }
  } finally {
    submitting.value = false;
  }
}

function onCancel() {
  router.back();
}

watch(
  () => [props.placeId, props.postId],
  () => {
    loadPlace();
    if (isEdit.value) loadPostForEdit();
  },
  { immediate: true },
);
</script>

<template>
  <section class="write">
    <div class="write__inner">
      <h2 class="write__heading">
        {{ isEdit ? "게시글 수정" : "게시글 작성" }}
      </h2>
      <p class="write__place text-body-small">
        지역: {{ placeName || "게시판" }}
      </p>

      <p v-if="formError" class="write__error">{{ formError }}</p>
      <p v-else-if="prefillError" class="write__error">{{ prefillError }}</p>

      <form class="write__form" @submit.prevent="onSubmit">
        <div v-if="!isEdit" class="write__field">
          <label class="write__label" for="nickname">닉네임</label>
          <input
            id="nickname"
            v-model="nickname"
            class="field-input"
            type="text"
            placeholder="익명"
            maxlength="20"
          />
        </div>

        <div class="write__field">
          <label class="write__label" for="password">
            {{ isEdit ? "작성 시 비밀번호" : "비밀번호" }}
          </label>
          <input
            id="password"
            class="field-input"
            type="password"
            inputmode="numeric"
            maxlength="4"
            placeholder="숫자 4자리"
            :value="password"
            @input="onPasswordInput"
          />
          <p class="write__hint text-body-small">
            게시글 수정/삭제 시 사용됩니다
          </p>
        </div>

        <div class="write__field">
          <label class="write__label" for="title">제목</label>
          <input
            id="title"
            v-model="title"
            class="field-input"
            type="text"
            placeholder="제목을 입력하세요"
          />
        </div>

        <div class="write__field">
          <label class="write__label" for="content">내용</label>
          <textarea
            id="content"
            v-model="content"
            class="field-input write__textarea"
            rows="10"
            placeholder="내용을 입력하세요"
          ></textarea>
        </div>

        <div class="write__actions">
          <button type="button" class="btn" @click="onCancel">취소</button>
          <button
            type="submit"
            class="btn btn-primary btn-lg"
            :disabled="!canSubmit"
          >
            {{
              submitting
                ? isEdit
                  ? "수정 중..."
                  : "등록 중..."
                : isEdit
                  ? "수정"
                  : "등록"
            }}
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<style scoped>
.write {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: var(--space-xl) var(--space-lg);
}

.write__inner {
  max-width: 800px;
  margin: 0 auto;
}

.write__heading {
  margin-bottom: var(--space-xs);
}

.write__place {
  color: var(--color-muted);
  margin-bottom: var(--space-xl);
}

.write__error {
  padding: var(--space-md) var(--space-lg);
  margin-bottom: var(--space-lg);
  border-radius: var(--radius-md);
  background: #fdeced;
  color: var(--color-danger);
  font-size: var(--font-body-small-size);
}

.write__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
}

.write__field {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.write__label {
  font-weight: 600;
  color: var(--color-foreground);
}

.write__hint {
  color: var(--color-muted);
}

.write__textarea {
  line-height: 1.6;
}

.write__actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-md);
  margin-top: var(--space-lg);
}
</style>
