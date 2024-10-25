import replicate
import streamlit as st
from translate import Translator


replicate_client = replicate.Client(api_token="enter your api key")


def split_into_sentences(text):
    return text.split('.')

# Function to get the output from replicate model
def get_replicate_output(val):
    result = ""
    for event in replicate_client.stream(
        "meta/meta-llama-3-8b-instruct",
        input={
            "top_k": 0,
            "top_p": 0.95,
            "prompt": val,
            "max_tokens": 512,
            "temperature": 0.7,
            "system_prompt": "You are a helpful assistant",
            "length_penalty": 1,
            "max_new_tokens": 512,
            "stop_sequences": "<|end_of_text|>,<|eot_id|>",
            "prompt_template": "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n",
            "presence_penalty": 0,
            "log_performance_metrics": False
        },
    ):
        result += str(event)
    return result

# Function to translate text to Sanskrit
def translate_to_sanskrit(text):
    translator = Translator(to_lang="sa")
    return translator.translate(text)

# Streamlit application layout
st.set_page_config(
    page_title="Sanskrit Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
)

def main():
    st.sidebar.title("MENU")
    st.sidebar.markdown("<hr>", unsafe_allow_html=True)

    st.title("Acharya.Ai")

    # Input text from user
    user_input = st.text_area("Enter your prompt:")

    if st.button("Translate"):
        if user_input:
            # Get the output from the model
            replicate_output = get_replicate_output(user_input)

            # Split the output into sentences
            sentences = split_into_sentences(replicate_output)

            # Display original output
            #st.subheader("Original Output:")
            #for sentence in sentences:
            #    if sentence.strip():  # Avoid empty sentences
            #        st.write(sentence.strip() + ".")

            # Translate each sentence and display the results
            st.subheader("Translated Output (Sanskrit):")
            for sentence in sentences:
                if sentence.strip():  # Avoid empty sentences
                    translated_sentence = translate_to_sanskrit(sentence.strip() + ".")
                    st.write(translated_sentence)

if __name__ == "__main__":
    main()
