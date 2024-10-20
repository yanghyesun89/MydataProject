import os
from dotenv import load_dotenv
from operator import itemgetter
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationSummaryMemory

# load .env
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DB_PATH = "./db"
PDF_PATH = "./pdf/"

class ChatService():
    def __init__(self):
        # llm model 불러오기
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

        # memory 구성
        self.memory = ConversationSummaryMemory(
            llm=self.llm,
            max_token_limit=80,
            return_messages=True,
            memory_key="chat_history"
        )

        # 1. data load & 2. text splitter
        self.splits = self.dataLoad()

        # 3. embedding (init에서 초기화)
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        # 4. vectorstore
        self.saveVectorDB()

        # 5. retriever
        self.retriever = self.createRetriever()

    def dataLoad(self):
        # 1. data load (document loader)
        loader = PyPDFDirectoryLoader(PDF_PATH)
        docs = loader.load()

        # 2. text splitter
        textSplitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = textSplitter.split_documents(docs)

        return splits
    
    def saveVectorDB(self):
        vectordb = FAISS.from_documents(
            documents = self.splits,
            embedding = self.embeddings
        )
        # 로컬에 저장
        vectordb.save_local(DB_PATH)

    def createRetriever(self):
        vectordb = FAISS.load_local(DB_PATH, self.embeddings, allow_dangerous_deserialization=True)
        
        retriever = vectordb.as_retriever(serarch_type="mmr", search_kwargs={'k': 1})

        # ensemble_retriever 추가 (검색의 정확도를 높이기 위함)
        bm25Retriever = BM25Retriever.from_documents(self.splits)
        bm25Retriever.k = 1

        # ensemble_retriever 추가
        ensembleRetriever = EnsembleRetriever(
            retrievers=[bm25Retriever, retriever], weights=[0.5, 0.5]
        )
        return ensembleRetriever

    def question(self, query):
        # 1. 프롬프트
        template = """해당 질문에 대해서 주어진 {context}을 기반하여 답변을 작성해줘"):
        
        # <context>
        # {context}
        # </context>"""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", template),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        outputParser = StrOutputParser()

        # 메모리에서 얻은 값을 chat_history 변수에 할당
        runnable = RunnablePassthrough.assign(
            chat_history=RunnableLambda(self.memory.load_memory_variables)| itemgetter("chat_history")
        )

        # 2. LLM 체인을 구성하고 실행
        chain = (
            {
                "context": self.retriever,
                "input": RunnablePassthrough(), #입력한 값 바로 전달해주는 역할
            }
            | runnable
            | prompt 
            | self.llm 
            | outputParser
        )
        # 3. 질의
        response = chain.invoke(query)

        # 질문&대답 메모리에 저장
        self.memory.save_context(
            {"input": query},
            {"output": response},
        )
        self.memory.load_memory_variables({})

        return response