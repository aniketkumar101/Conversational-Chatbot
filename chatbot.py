from dotenv import load_dotenv
load_dotenv()
import os
import streamlit as st
import google.generativeai as genai


# Configure the API key for the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize our streamlit app
st.set_page_config(page_title="Chatbot")
st.header("Conversational Chatbot")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Function to get response from Gemini Pro model and get response
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# User input section
input = st.text_input("Input:", key="input")
submit = st.button("Submit")

if input and submit:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You", input))
    
    # Display response
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Display chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
