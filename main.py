import openai
import streamlit as st
from streamlit_chat import message

st.title("Deloitte Consultant GPT")

# Move the OpenAI API key input to the sidebar
with st.sidebar:
    my_key = st.text_input(label=":key: OpenAI Key:", 
                           help="Please ensure you have an OpenAI API account with credit. ChatGPT Plus subscription does not include API access.",
                           type="password")

# Check if the key is provided and set it for openai
if my_key:
    openai.api_key = my_key

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    # Setting up the introductory message from the consultant
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": ("Hello! I'm your virtual Deloitte management consultant. "
                        "Please share your business concerns, and I'll analyze them.")
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Client, how can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
