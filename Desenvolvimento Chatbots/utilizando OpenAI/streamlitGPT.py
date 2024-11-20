import streamlit as st
from openai import OpenAI

st.title("ChatGPT Like")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    instructions = """Você é um secretário de uma clinica médica. Você atendem várias especialidades médicas.
    Interaja com o usuário e responda normalmente as perguntas dele, quando ele quiser marcar uma consulta pergunte na ordem. 1. Qual plano de saude ele possui
    2. Melhor data e horário para consulta. Se o plano de saúde for o Notredame, informe ao usuário que não atendemos esse plano."""
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "user", "content": prompt},
                {"role": "system", "content": instructions}
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})    
