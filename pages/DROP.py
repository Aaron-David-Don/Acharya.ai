import streamlit as st
import io
import pdfplumber
import docx2txt
import time
from deep_translator import GoogleTranslator
from openai import OpenAI

def questionfunc(api_key,question,raw_text):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)    
    # Define the system message template
    system_message = ("You are a highly knowledgeable Sanskrit scholar with deep expertise in Sanskrit literature, grammar, and philosophy." 
                      "You have been provided with a [text_excerpt], which may include Sanskrit verses, prose, or explanations, and your task is to analyze" 
                      "and interpret its contents based on the [question] posed by a student." 
                      "You will carefully consider the grammatical structures, meanings, philosophical concepts, and cultural context of the text." 
                      "Provide clear, precise, and accurate explanations, ensuring that the student can fully understand the meaning and significance of the Sanskrit content.")
     
    # Create the user message for few-shot prompting
    user_message_tuning=(f"""text: "श्लोक संग्रह १" contains a collection of common Sanskrit shlokas used for recitation. Here are some key shlokas included in the document:

Ganesha Shloka: "वक्रतुंड महाकाय सूर्यकोटि समप्रभ ।
निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा ॥"

Saraswati Shloka: "या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता ।
या वीणावरदण्डमण्डितकरा या श्वेतपद्मासना ॥"

Guru Shloka: "गुरुर्ब्रह्मा गुरुर्विष्णुः गुरुर्देवो महेश्वरः ।
गुरु: साक्षात् परब्रह्म तस्मै श्री गुरवे नमः ॥"

Vishnu Shloka: "शान्ताकारं भुजगशयनं पद्मनाभं सुरेशम् ।
विश्वाधारं गगनसदृशं मेघवर्णं शुभाङ्गम् ॥"

Sarve Bhavantu Sukhinah: "सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः ।
सर्वे भद्राणि पश्यन्तु मा कश्चिद् दुःखभाग्भवेत् ॥"

Other Shlokas:

Prayers to Devi, Vishnu, Shiva, Rama, and others.
"कराग्रे वसते लक्ष्मीः करमध्ये सरस्वती ।"
"ॐ असतो मा सद्गमय । तमसो मा ज्योतिर्गमय ।"
                             question: Count the number of key vedas in this document?
                         """)
                                     
    #Create assistant response for user_message_tuning
    assistant_message_tuning=("""The number of key shlokas provided in the above text is five. Here is the breakdown:

Ganesha Shloka:
"वक्रतुंड महाकाय सूर्यकोटि समप्रभ ।
निर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा ॥"

Saraswati Shloka:
"या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता ।
या वीणावरदण्डमण्डितकरा या श्वेतपद्मासना ॥"

Guru Shloka:
"गुरुर्ब्रह्मा गुरुर्विष्णुः गुरुर्देवो महेश्वरः ।
गुरु: साक्षात् परब्रह्म तस्मै श्री गुरवे नमः ॥"

Vishnu Shloka:
"शान्ताकारं भुजगशयनं पद्मनाभं सुरेशम् ।
विश्वाधारं गगनसदृशं मेघवर्णं शुभाङ्गम् ॥"

Sarve Bhavantu Sukhinah:
"सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः ।
सर्वे भद्राणि पश्यन्तु मा कश्चिद् दुःखभाग्भवेत् ॥"

These are the key shlokas explicitly listed.""")
    
    #input question submitted by user 
    user_message=(f"text_excerpt: {raw_text} \n question: {question} ")
    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.35,
        n=1,
        max_tokens=1000,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )
    # Extract the response content
    result=response.choices[0].message.content
    return result

def explainfunc(api_key,raw_text):
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    # Define the system message template
    system_message = (  "You are a Sanskrit scholar with extensive knowledge of Sanskrit language, grammar, and literature. "
                      "You are tasked with reading and understanding documents that may contain a mix of both English and Sanskrit text. "
                      "Your role is to clearly explain and interpret the content of the document in a way that helps a student learn and comprehend the material."
                       " When the document contains Sanskrit text, provide accurate translations and explanations of key concepts, grammatical structures, and meanings, making "
                       "sure that the student can follow and grasp the subject matter.")                     
    # Create the user message for few-shot prompting
    user_message_tuning=("""common shlokas used for recitationset 1
 
 Document Information
 Text title : shloka
 File name : shloka1.itx
 Category : misc, shloka
 Location : doc_z_misc_general
 Transliterated by : sa.ngraha 1
 Proofread by : sa.ngraha 1
 Latest update : November 1, 2010
 Send corrections to : sanskrit at cheerful dot c om
                         This text is prepared by volunteers and is to be used for personal study and research. The
 f
 ile is not to be copied or reposted without permission, for promotion of any website or
 individuals or for commercial purpose.
 Please help to maintain respect for volunteer spirit.
 Please note that proofreading is done using Devanagari version and other language/scripts
 are generated using sanscript
                         The following are the sanskrit shlokas:
                         स्वभावो नोपदेशेन शक्यते कर्तुमन्यथा ।
सुतप्तमपि पानीयं पुनर्गच्छति शीतताम् ॥
                         अनाहूतः प्रविशति अपृष्टो बहु भाषते ।
अविश्वस्ते विश्वसिति मूढचेता नराधमः ॥
                         यथा चित्तं तथा वाचो यथा वाचस्तथा क्रियाः ।
चित्ते वाचि क्रियायांच साधुनामेक्रूपता ॥
                         षड् दोषाः पुरुषेणेह हातव्या भूतिमिच्छता ।
निद्रा तद्रा भयं क्रोधः आलस्यं दीर्घसूत्रता ॥
                         द्वौ अम्भसि निवेष्टव्यौ गले बद्ध्वा दृढां शिलाम् ।
धनवन्तम् अदातारम् दरिद्रं च अतपस्विनम् ॥
                         अलसस्य कुतो विद्या , अविद्यस्य कुतो धनम् |
अधनस्य कुतो मित्रम् , अमित्रस्य कुतः सुखम् ||
                         आलस्यं हि मनुष्याणां शरीरस्थो महान् रिपुः |
नास्त्युद्यमसमो बन्धुः कृत्वा यं नावसीदति ||
                          यस्तु सञ्चरते देशान् सेवते यस्तु पण्डितान् !
तस्य विस्तारिता बुद्धिस्तैलबिन्दुरिवाम्भसि !!
                         विद्वत्वं च नृपत्वं च नैव तुल्यं कदाचन !
स्वदेशे पूज्यते राजा विद्वान् सर्वत्र पूज्यते !!
                         उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः !
न हि सुप्तस्य सिंहस्य प्रविशन्ति मुखे मृगाः !!
                         """)
    #Create assistant response for user_message_tuning
    assistant_message_tuning=("""
                                This document provides a collection of Sanskrit shlokas (verses) commonly used for recitation, 
                              along with some contextual information about the file. Let me break down the relevant sections and
                               the meanings of the shlokas:
                              Document Overview:
Title: shloka (a collection of Sanskrit verses)
File Name: shloka1.itx
                              Transliterated by: sa.ngraha 1
Proofread by: sa.ngraha 1
                              Note: This document is prepared by volunteers for personal study and research. It should not be copied or used for commercial purposes without permission. It has been proofread using the Devanagari script.
                              The Sanskrit Shlokas and their Meanings:
स्वभावो नोपदेशेन शक्यते कर्तुमन्यथा ।
सुतप्तमपि पानीयं पुनर्गच्छति शीतताम् ॥

Meaning: A person’s inherent nature cannot be changed through instruction. Just as water, no matter how much it is heated, will eventually return to its cold state.
Lesson: This shloka highlights that a person's fundamental nature or character is hard to alter permanently through external means.
अनाहूतः प्रविशति अपृष्टो बहु भाषते ।
अविश्वस्ते विश्वसिति मूढचेता नराधमः ॥

Meaning: A fool is one who enters without invitation, speaks too much without being asked, and trusts those who are untrustworthy.
Lesson: This verse critiques foolish behavior, emphasizing the importance of discretion and wisdom in social interactions.
यथा चित्तं तथा वाचो यथा वाचस्तथा क्रियाः ।
चित्ते वाचि क्रियायांच साधुनामेक्रूपता ॥

Meaning: For good people, their thoughts are aligned with their speech, and their speech aligns with their actions. There is consistency among the mind, speech, and actions of the virtuous.
Lesson: This shloka emphasizes integrity and the harmony between thought, word, and deed in virtuous individuals.
षड् दोषाः पुरुषेणेह हातव्या भूतिमिच्छता ।
निद्रा तन्द्रा भयं क्रोधः आलस्यं दीर्घसूत्रता ॥

Meaning: A person who seeks success must give up six vices: excessive sleep, laziness, fear, anger, procrastination, and indecision.
Lesson: This verse advises that these six negative traits hinder progress and should be avoided to achieve success.
द्वौ अम्भसि निवेष्टव्यौ गले बद्ध्वा दृढां शिलाम् ।
धनवन्तम् अदातारम् दरिद्रं च अतपस्विनम् ॥

Meaning: Two kinds of people should be cast into the water with a heavy stone tied around their neck: a wealthy person who does not give and a poor person who refuses to work hard.
Lesson: This shloka criticizes both stinginess and laziness, suggesting that both are detrimental to society.
अलसस्य कुतो विद्या , अविद्यस्य कुतो धनम् |
अधनस्य कुतो मित्रम् , अमित्रस्य कुतः सुखम् ||

Meaning: How can a lazy person gain knowledge? How can an uneducated person gain wealth? How can a poor person have friends? And how can a person without friends find happiness?
Lesson: The verse highlights the interconnectedness of effort, knowledge, wealth, friendship, and happiness.
आलस्यं हि मनुष्याणां शरीरस्थो महान् रिपुः |
नास्त्युद्यमसमो बन्धुः कृत्वा यं नावसीदति ||

Meaning: Laziness is a great enemy within the human body. There is no better friend than effort, which never lets a person fail.
Lesson: This shloka underscores the destructive nature of laziness and the value of persistent effort.
यस्तु सञ्चरते देशान् सेवते यस्तु पण्डितान् !
तस्य विस्तारिता बुद्धिस्तैलबिन्दुरिवाम्भसि !!

Meaning: A person who travels to different places and serves the learned will have an expanded intellect, just as oil spreads out when it falls into water.
Lesson: This shloka encourages learning through exploration and interaction with wise individuals.
विद्वत्वं च नृपत्वं च नैव तुल्यं कदाचन !
स्वदेशे पूज्यते राजा विद्वान् सर्वत्र पूज्यते !!

Meaning: Knowledge and kingship can never be compared. A king is honored only in his own country, whereas a learned person is respected everywhere.
Lesson: The shloka glorifies the power of knowledge, which transcends borders and commands respect universally.
उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः !
न हि सुप्तस्य सिंहस्य प्रविशन्ति मुखे मृगाः !!

Meaning: Tasks are accomplished through effort, not mere wishes. Even for a lion, prey does not walk into its mouth while it sleeps.
Lesson: This shloka stresses the importance of active effort rather than passive dreaming in achieving success.
Conclusion:
This collection of shlokas provides profound moral and practical lessons, emphasizing virtues like hard work, consistency in 
                              thought and action, wisdom, and the dangers of laziness and foolishness. 
                              These teachings are timeless and offer guidance for personal development and success in life.""")
    #Create the user message for generating itinerary
    user_message=(f"Given Text: {raw_text}")

    # Call OpenAI API to generate options
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message_tuning},
            {"role": "assistant", "content":assistant_message_tuning},
            {"role": "user", "content": user_message}
        ],
        temperature=0.35,
        n=1,
        max_tokens=1000,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the response content
    result=response.choices[0].message.content
    return result

def main():
    api_key="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"
    st.sidebar.title("MENU")
    st.sidebar.image("Picture1.png", use_column_width=True)
    st.sidebar.markdown("<hr>",unsafe_allow_html=True)
    st.subheader("Drop Files Here")
    raw_files=st.file_uploader('Upload your files', type=['txt','docx','pdf'], accept_multiple_files=True)
    #Reading File Data
    if raw_files is not None:
        raw_text = ""  # Initialize an empty string to accumulate text from all documents
        for uploaded_file in raw_files:  # Loop through each uploaded file
            if uploaded_file.type == "text/plain":
                try:
                    text = str(uploaded_file.read(), "utf-8")
                    raw_text += text  # Concatenate the text from the current document
                except:
                    st.error(".txt file fetching problem!\ncheck your file again and try re-uploading")
            elif uploaded_file.type == "application/pdf":
                try:
                    pdf_reader = pdfplumber.open(uploaded_file)
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        raw_text += page.extract_text()  # Concatenate the text from the current page
                except:
                    st.error(".pdf file fetching problem!\ncheck your file again and try re-uploading")
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                try:
                    raw_text += docx2txt.process(uploaded_file)  # Concatenate the text from the current document
                except:
                    st.error(".docx file fetching problem!\ncheck your file again and try re-uploading")
            else:
                st.error("Please Upload a File to continue!")

    st.markdown("<hr>",unsafe_allow_html=True)
    st.info("What do you want to do with your document?")
    menu=["Ask a question","Explain","Translate"]
    choice=st.selectbox("",menu)
    st.markdown("<hr>",unsafe_allow_html=True)
    if choice=="Ask a question":
        question=st.text_area("Enter your question")
        if st.button("Submit"):
            response1=questionfunc(api_key,question,raw_text)
            st.info(response1)
    if choice=="Explain":
        response2=explainfunc(api_key,raw_text)
        st.info(response2)
    if choice=="Translate":
        target_lang = st.selectbox("Choose Language", ["Tamil", "Sanskrit"])
        display_target_lang=target_lang
        if target_lang == "Tamil":
            target_lang = 'ta'
        elif target_lang=="Sanskrit":
            target_lang = 'sa'
        
        if st.button("Translate"):
            if len(raw_text) < 3:
                st.warning("Sorry! You need to provide a text with at least 3 characters")
            else:
                my_bar = st.progress(0)
                message_slot = st.empty()
                message_slot.text('Translating...')

                for value in range(50):
                    time.sleep(0.01)
                    my_bar.progress(value + 1)

                if my_bar.progress(100):
                    message_slot.empty()  # Clear the "Translating..." message
                    st.success("Your Text Has Been Translated successfully!")
                    
                translator = GoogleTranslator(source="auto", target=target_lang)
                translated_text = translator.translate(raw_text)
                st.info("Original text: "+raw_text)
                st.warning("language selected is: "+display_target_lang)
                st.info("Translated text: "+translated_text)
        

if __name__=="__main__":
    main()
