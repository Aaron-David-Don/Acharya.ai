#with help of ollama replicate and translate building a sanksrit chatbot
import replicate
import sys
import io
from translate import Translator

# Set UTF-8 encoding for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

replicate_client = replicate.Client(api_token="use your api key")

def split_into_sentences(text):
    return text.split('.')

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

def translate_to_sanskrit(text):
    translator = Translator(to_lang="sa")
    return translator.translate(text)

val = input("Enter your prompt: ")

replicate_output = get_replicate_output(val)

sentences = split_into_sentences(replicate_output)

with open("output.txt", "w", encoding="utf-8") as file:
    file.write("Original Output :\n")
    
    for i, sentence in enumerate(sentences):
        if sentence.strip():  # Avoid writing empty sentences
            file.write(sentence.strip() + ".\n")
    
    file.write("\nSanskrit Output:\n")
    
    for i, sentence in enumerate(sentences):
        if sentence.strip(): 
            translated_sentence = translate_to_sanskrit(sentence.strip() + ".")
            file.write(translated_sentence + "\n")

print("Results have been saved to output.txt")
