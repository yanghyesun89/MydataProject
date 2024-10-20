# 문서 기반 LLM 프로젝트\_프론트엔드

- Vuejs 프레임워크 통해서 화면 개발

## Results
<img width="1782" alt="스크린샷" src="https://github.com/user-attachments/assets/d3c2849f-e5c2-4962-a6fc-d286f3c4fa84">

1. 홈화면

## Run it

```shell
npm install
npm run serve
```

## package.json

```json
{
  "axios": "^1.7.7",
  "core-js": "^3.8.3",
  "vue": "^3.2.13",
  "vue-router": "^4.0.3",
  "vuex": "^4.0.0"
}
```

## 구현 설명

1. 서버와 통신

- axios 라이브러리 이용해서 통신
- api 모듈 생성해서 통신을 하나의 모듈로 관리

2. 화면

- 질문과 답변을 리스트로 관리하여 모두 보여줄 수 있도록 구현
- 반응형으로 구현
