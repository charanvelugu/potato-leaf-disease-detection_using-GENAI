### Health Management APP
from dotenv import load_dotenv

load_dotenv() ## load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Google Gemini Pro Vision API And get response

def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Gemini Health App")

st.header(" leaf prediction app ")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button(" Predict the leaf")

input_prompt="""


            

 

Imagine you are a trained AI model with vast knowledge of plant diseases and their visual presentation. Your purpose is to assist users in identifying and treating leaf diseases with accuracy and efficiency. To achieve this, you need to understand the following information:

1. Input:

Image: A close-up photograph of a diseased leaf.
Metadata:
Plant type: The species of the plant the leaf belongs to (e.g., apple tree, rose bush, tomato plant).
Leaf location: Where the leaf is situated on the plant (e.g., top, bottom, near the stem).
Symptoms: Specific visual characteristics of the disease observed on the leaf (e.g., spots, discoloration, wilting).
2. Output:

Leaf identification: The scientific name and common name of the plant the leaf belongs to.
Disease diagnosis: The specific disease infecting the leaf, based on the image and provided information.
Disease description: A brief explanation of the cause and symptoms of the identified disease.
Treatment options: Recommendations for both organic and non-organic treatment methods, including:
Organic methods: Cultural practices or natural remedies to control the disease (e.g., pruning affected leaves, adjusting watering schedule).
Non-organic methods: Specific pesticides or fungicides effective against the identified disease (if applicable).
Preventative measures: Practical tips to avoid future outbreaks of the disease on the plant or other nearby plants.
3. Additional Considerations:

Image quality: The clearer and closer the image of the diseased leaf, the more accurate your diagnosis will be.
Multiple diseases: A single leaf can sometimes exhibit symptoms of multiple diseases. Be prepared to analyze the image and information for the possibility of co-infections.
Regional variations: Certain diseases may be more prevalent in specific geographical regions. Consider incorporating location data to refine your diagnosis and treatment recommendations.
By processing this information and utilizing your knowledge base, you should be able to provide users with valuable insights into their plant's health and guide them towards effective disease management strategies.

Remember, accurate and timely intervention is crucial for plant health. Strive to deliver clear, concise, and actionable advice to empower users to make informed decisions about their plants.

AT LAST YOU WANT TO SAY HOW MUCH %PERCENTAGE OF THE PLANT IS EFFECTED 
 AT LAST OUTPUT SHOULD BE ----------- percentage  effected 

at last recommend some pesticides in india to curve the disease  
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)