import axios from "axios";

const axiosService = axios.create({
  headers: {
    ContentType: "application/json",
  },
});

const postChat = async (message) => {
  try {
    return await axiosService.post("/chat", { message: message });
  } catch (error) {
    if (error.response.status >= 500) {
      alert("서버 요청 중 에러가 발생했습니다. 다시 시도 부탁드립니다.");
    }
  }
};

export { postChat };
