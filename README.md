# 문서 기반 LLM 프로젝트

## Architecture

- 백엔드 : FastAPI, LangChain
- 프론트엔드 : Vuejs

![그림1](https://github.com/user-attachments/assets/54332452-06c7-42ff-bb6b-44989644e3a9)

## Results
<img width="1782" alt="스크린샷" src="https://github.com/user-attachments/assets/d3c2849f-e5c2-4962-a6fc-d286f3c4fa84">

## 백엔드

[백엔드 READMD](https://github.com/yanghyesun89/MydataProject/blob/main/backend/README.md)

## 프론트엔드

[프론트엔드 READMD](https://github.com/yanghyesun89/MydataProject/blob/main/frontend/README.md)

## 참고 사항

- AWS의 Bedrock 서비스를 최근 출시, S3를 통해 문서를 저장해 해당 문서를 기반으로 RAG를 보다 간편하게 구성할 수 있다.

## 추가 구현/미흡한 부분

- llm model 다른 여러 모델이 가능한 구조 만들기
- text splits, embedding 등 여러 라이브러리를 자유롭게 바꿔서 사용하는 구조 만들기
- 멀티 모달 만들기
