<template>
  <div class="home">
    <div class="header">
      <div>
        * 마이데이터 공식 문서를 기반으로 정책과 기술 사양 등을 답변해주는
        에이전트
      </div>
    </div>
    <div class="chat-list">
      <div
        v-for="(item, idx) in chatList"
        :key="idx"
        class="chat-item"
        :class="{ my: item.id === 1 }"
      >
        <div v-if="item.id === 1" class="who">YOU</div>
        <div v-else class="who">CHAT</div>
        <div>{{ item.message }}</div>
      </div>
    </div>
    <div class="question">
      <input
        type="text"
        v-model="question"
        placeholder="메세지 입력"
        @keyup.enter="addChat"
      />
      <button @click="addChat">➤</button>
    </div>
  </div>
  <div class="loading-bg" v-if="isLoading">
    <div id="loading"></div>
  </div>
</template>

<script>
import { postChat } from "@/api/index.js";
export default {
  name: "HomeView",
  data() {
    return {
      isLoading: false,
      question: "",
      chatList: [],
    };
  },
  methods: {
    async reqQuestion() {
      this.isLoading = true;
      await postChat(this.question).then((result) => {
        const data = result.data;
        const status = result.status;
        if (status === 200) {
          if (data.code === 200) {
            this.chatList.push({
              id: 2,
              message: data.data.answer,
            });
          }
        }
      });
      this.isLoading = false;
    },
    addChat() {
      //질문을 입력하지 않았을 경우
      if (this.question.trim().length === 0) {
        return;
      }
      //질문을 진행하고 있는 경우
      if (this.isLoading) {
        return;
      }
      this.chatList.push({
        id: 1,
        message: this.question,
      });
      this.reqQuestion(this.question);
      this.question = "";
    },
  },
};
</script>

<style>
.home {
  height: 100%;
  max-width: 700px;
  margin: 0 auto;
  padding: 0 8px;
}
.header {
  color: #f3f3f3;
  height: 36px;
  display: flex;
  align-items: center;
}
.chat-list {
  height: calc(100% - 124px);
  overflow: scroll;
}
.chat-list .chat-item {
  color: #f3f3f3;
  margin-top: 16px;
  padding: 8px 16px;
}
.chat-list .my {
  background-color: #4f4f4f;
  border-radius: 999px;
}
.chat-list .chat-item .who {
  color: #777777;
  padding-bottom: 4px;
  font-size: 12px;
}
.question {
  height: 40px;
  display: flex;
  padding: 16px 0 32px;
}
.question input {
  border: none;
  border-radius: 999px;
  background-color: #4f4f4f;
  color: #f3f3f3;
  flex: 1;
  margin-right: 8px;
  padding: 0 16px;
}
.question button {
  border: none;
  background-color: #4f4f4f;
  color: #f3f3f3;
  border-radius: 999px;
  padding: 0 16px;
  cursor: pointer;
}
/* loading */
.loading-bg {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
#loading {
  display: inline-block;
  width: 50px;
  height: 50px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  -webkit-animation: spin 1s ease-in-out infinite;
}
@keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
@-webkit-keyframes spin {
  to {
    -webkit-transform: rotate(360deg);
  }
}
</style>
