# THIS REPOSITORY IS FOR SANSKRIT CHATBOT USING RAG WITH AUDIO

## This repository contains codes that can be used to create a database, embeddings, rag, drop files and host it using Streamlit

## Before running the code, first create and venv with 
    '''python -m venv venv'''
    '''.\venv\Scripts\activate'''
    '''
## Then install all the requirements using this code also install streamlit
    '''pip install -r requirements.txt '''

## Now right click on any of the file and "Open in Integrated Terminal" and run this
    '''streamlit run RAG2.py'''

1. **.env**
   - This code contains the api key for all the required modules
     
2. **books**
   - This folder contains all the markdown files of Mahabharata to be used for RAG

3. **pages**
   - This folder contains the following codes
     a. **Basic_Chatbot.py**
        - This code is used for the basic chatbot where Llama 8b instruct api key through replicate is used to get the user input and feed to the GPT to get the output and the a translator module is
          used to the translate the generated text to Sanskrit. This is hosted as a website using streamlit
     b. **DROP.py**
        - This code enables the user the upload their document and 3 task can be performed by the code, the 3 functions are:
          1) First part of the code read the document content and replies anything based of the document. For eg: Upload a Sanskrit document and ask question about it.
          2) Second part of the code is for the explanation. It can take a sanskrit document and explain each part of the document to make the user understand
          3) Third part of code Translated everything presented in the document to a specific language picked by the user

4. **create_database.py**
   - This is one of the most important code file. This code uses LangChain and Chroma DB along with OpenAi api key to first split the contents in the markdown files into chunks and with OpenAi
     embeddings function converting the chunks to embeddings then storing it in the DB

5. **RAG2.py**
   - This is the main code of the project. This code takes the user prompt and with OpenAi embeddings converts it into embeddings and check it relevancy with the values in the DB and the top 3
     results are taken and all these are fed into GPT to generate a final answer and this final answer is sent to ElevenLabs to generate audio

6. **query_data.py**
   - This is the same code a RAG2.py but with the Streamlit interface

7. **compare_embeddings.py**
   - This is a rough code to understand embeddings and check out the differences in their values

8. **ChatBotV2.py**
   - This is a simple code using OpenAi and Streamlit that takes the user input and provides to GPT to provide solution in Sanskrit
