#!/usr/bin/env python
# coding: utf-8

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

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


def ask(question, llm):
    TEMPLATE = """
    Você é um especialista em legistalação e tecnologia. Responda a pergunta abaixo utilizando o contexto informado

    Contexto: {context}
    
    Pergunta: {question}
    """
    prompt = PromptTemplate(input_variables=["context", "question"], template=TEMPLATE)
    sequence = RunnableSequence(prompt | llm)
    context = getRelevantDocs(question)
    response = sequence.invoke({"context": context,"question": question})
    return response
