import streamlit as st
from openai import OpenAI

st.title("ChatGPT Like")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])