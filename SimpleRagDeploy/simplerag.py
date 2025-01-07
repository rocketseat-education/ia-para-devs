#!/usr/bin/env python
# coding: utf-8

# ## Usando arquivo .env para controlar variaveis de ambiente
# Para evitar exposição da chave `OPENAI_API_KEY` optei por utilizar arquivo `.env` com a informação da chave.
# 
# Para seguir o mesmo método basta criar um arquivo `.env` no mesmo diretório do arquivo `Solucao RAG.ipynb`.
# A importação da chave será feita através da célula abaixo que faz a instalação de um biblioteca para carregar
# os valores do arquivo `.env`.


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.question_answering import load_qa_chain
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Load dos modelos (Embeddings e LLM)
embeddings_model = OpenAIEmbeddings()
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    max_tokens=200,
    
)


def loadData():
    # Carregar o PDF
    pdf_link = "DOC-SF238339076816-20230503.pdf"
    loader = PyPDFLoader(pdf_link, extract_images=False)
    pages = loader.load_and_split()

    # Separar em Chunks (Pedaços de documento)
    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_spliter.split_documents(pages)
    vectordb = Chroma.from_documents(chunks, embedding=embeddings_model)

    # Load Retriever
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    return retriever


def getRelevantDocs(question):
    retriever = loadData()
    context = retriever.invoke(question)
    return context


# Chain - Contrução da cadeira de prompt para chamada do LLM
chain = load_qa_chain(llm, chain_type="stuff")


def ask(question):

    answer = (chain({"input_documents": context, "question": question}, return_only_outputs=True))["output_text"]
    return answer, context


user_question = input("User: ")
answer, context = ask(user_question)
print("Answer: ", answer)


for c in context:
    print(c)

