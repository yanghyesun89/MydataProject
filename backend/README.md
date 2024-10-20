# 문서 기반 LLM 프로젝트\_백엔드

- FastAPI 웹 프레임워크를 통해 백엔드 개발

## Run it

```shell
$ cd app
$ pip install -r requirements.txt
$ python main.py
```

## Requirements

```yml
langchain==0.3.3
langchain-community==0.3.2
langchain-core==0.3.10
langchain-openai==0.2.2
langchain-text-splitters==0.3.0
langchainhub==0.1.21
beautifulsoup4==4.12.3
faiss-cpu==1.9.0
fastapi==0.115.0
uvicorn==0.31.1
urllib3==2.2.2
PyMuPDF==1.24.11
pypdf===5.0.1
sentence-transformers==3.2.0
pytest===8.3.3
pytest-asyncio===0.24.0
```

## Configuration

- OPENAI API 키를 발급하여 .env 파일에서 입력

## 프로젝트 구조

```
app
 ┣ api
 ┃ ┣ __init__.py
 ┃ ┣ chat.py
 ┃ ┗ main.py
 ┣ data
 ┃ ┣ __init__.py
 ┃ ┣ reqChat.py
 ┃ ┗ resChat.py
 ┣ db
 ┣ exception
 ┃ ┣ __init__.py
 ┃ ┗ exception.py
 ┣ pdf
 ┃ ┣ (221115 수정배포) (2022.10) 금융분야 마이데이터 기술 가이드라인.pdf
 ┃ ┗ (수정게시) 금융분야 마이데이터 표준 API 규격 v1.pdf
 ┣ service
 ┃ ┣ __init__.py
 ┃ ┗ chatService.py
 ┣ tests
 ┃ ┗ testChat.py
 ┣ .env
 ┣ __init__.py
 ┣ main.py
 ┗ requirements.txt
```

## RAG 구성

1. pdf loader : 문서를 불러오는 작업

- PyPDFDirectoryLoader 라이브러리 사용, 디렉토리 하위 파일 불러오기

```python
loader = PyPDFDirectoryLoader('./pdf/')
docs = loader.load()
```

2. text splitter : 불러온 문서의 텍스트를 쪼개는 작업

- RecursiveCharacterTextSplitter 라이브러리 사용, chunk size는 1000자로 설정

```python
textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = textSplitter.split_documents(docs)
```

3. embedding : 문서의 내용을 수치적인 벡터로 변환하는 과정

- OpenAIEmbeddings 라이브러리 이용, model은 openAI의 'text-embedding-3-large'를 사용

```python
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
```

4. vector store : 벡터 저장소에 저장

- FAISS 라이브러리 사용(페이스북에서 개발), 로컬에 파일 저장

```python
vectordb = FAISS.from_documents(
    documents = splits,
    embedding = embeddings
)
```

5. retreiver : 사용자의 질문과 가장 유사한 문장을 검색

- BM25Retriever, EnsembleRetriever 라이브러리 사용
- MMR는 특정 쿼리에 대해 관련성이 높으면서도 서로 다양한 문서들을 선택하는 알고리즘, k는 k개의 문서를 반환
- BM25Retriever는 주어진 쿼리에 대해 문서와의 연관성을 평가하는 랭킹 함수로 사용되는 검색기
- EnsembleRetriever는 여러 검색기를 결합하여 더 강력한 검색 결과를 제공하는 검색기
- BM25Retriever, FAISS 검색기 검색기 각각의 가중치 설정

```python
retriever = vectordb.as_retriever(serarch_type="mmr", search_kwargs={'k': 1})

bm25Retriever = BM25Retriever.from_documents(splits)
bm25Retriever.k = 1

ensembleRetriever = EnsembleRetriever(
    retrievers=[bm25Retriever, retriever], weights=[0.5, 0.5]
)
```

## LLM 구성

1. llm model 불러오기

- llm model은 gpt-3.5-turbo-0125 사용

```python
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
```

2. prompt 입력

- 사용자 또는 시스템에서 제공하는 입력으로, LLM에게 특정 작업을 수행하도록 요청하는 지시문 등록
- system: 시스템 설정 메세지, human: 사용자 입력 메세지, ai: AI의 답변 메세지
- MessagePlaceholder: 포맷하는 동안 렌더링할 메시지를 완전히 제어
- 치환될 변수를 {} 안에 정의

```python
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)
```

3. 메모리 설정 (이전 대화 기억을 위한 메모리)

- ConversationSummaryMemory 라이브러리 사용
- 대화 요약 메모리는 대화가 진행되는 동안 대화를 요약하고 현재 요약을 메모리에 저장, 80 토큰 저장으로 제한
- 메모리에서 얻은 값을 chat_history 변수에 할당
- 대화 내용은 memory.save_context() 를 통해 저장, 대화 내용은 memory.load_memory_variables로 로드

```python
memory = ConversationSummaryMemory(
    llm=llm,
    max_token_limit=80,
    return_messages=True,
    memory_key="chat_history"
)
runnable = RunnablePassthrough.assign(
    chat_history=RunnableLambda(memory.load_memory_variables)| itemgetter("chat_history")
)
```

4. chain

- 프롬프트, 메모리, 모델 등 연결하여 설정

```python
chain = (
    {
        "context": retriever,
        "input": RunnablePassthrough(),
    }
    | runnable
    | prompt
    | llm
    | output_parser
)
```

## FastAPI 구성

- FastAPI 파이썬 프레임워크 사용, 빠르고 쉽게 구현 가능

1. 초기화

```python
app = FastAPI(
    title="OpenAI Server",
    version="1.0.0",
    description="문서 기반 OpenAI Server",
)
```

2. 라우터 추가

```python
@app.get("/")
async def root():
    return {"message": "welcome to chat"}
```

3. exception 처리

```python
@app.exception_handler(ValidException)
async def validationException(request: Request, exc: ValidException):
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "msg": f"{exc.req} 값을 입력하세요."
        }
    )
```

## 테스트 코드

- FastAPI의 testclient 이용하여 테스트 코드 작성

```python
def test_chat(client: TestClient):
  data = {"message": "안녕"}
  response = client.post(
        "/chat",
        json=data,
    )
  assert response.status_code == 200
  content = response.json()
  assert "code" in content
  assert "data" in content
```

- 테스트 방법 : pytest test/testChat.py 입력

```shell
$ pytest tests/testChat.py
============================================================================================== test session starts ==============================================================================================
platform darwin -- Python 3.12.4, pytest-8.3.3, pluggy-1.5.0
rootdir: /Users/yanghyesun/dev/project/backend/app
plugins: asyncio-0.24.0, anyio-4.2.0
asyncio: mode=Mode.STRICT, default_loop_scope=None
collected 3 items

tests/testChat.py ..
```

- 비동기 테스트 : @pytest.mark.asyncio를 통해 비동기 테스트 진행
