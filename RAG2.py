import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import requests
import time

# Load environment variables
load_dotenv()

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context and provide the output in Sanskrit:

{context}

---

Answer the question based on the above context: {question}
"""

# Streamlit setup
st.set_page_config(
    page_title="Acharya.Ai",
    page_icon="🧘‍♂️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Acharya.Ai")
st.write("Ask any question, and I will respond in Sanskrit based on a context search!")

# Function to generate audio from text
def generate_audio(text, filename="output.mp3"):
    CHUNK_SIZE = 1024
    url = "https://api.elevenlabs.io/v1/text-to-speech/enter ur required api" 
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY")  
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v1", 
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, json=data, headers=headers)
    
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
    
    return os.path.abspath(filename)


def search_and_answer(query_text):
    
    embedding_function = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        return "Unable to find matching results."

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Generate the response
    model = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"))
    response_text = model.predict(prompt)

    # Collect sources
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\n\nSources: {sources}"
    return response_text, sources


query_text = st.sidebar.text_input("Enter your question", value="")

if st.sidebar.button("Ask"):
    if query_text:
        with st.spinner("Searching the database and generating the response..."):
            response_text, sources = search_and_answer(query_text)
            st.write(f"**Response in Sanskrit:** {response_text}")
            st.write(f"**Sources:** {sources}")

            # Generate and display audio
            st.write("Generating audio... Please wait.")
            audio_file_path = generate_audio(response_text)
            time.sleep(10)  # Simulate processing delay

            # Display the audio
            audio_file = open(audio_file_path, "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
