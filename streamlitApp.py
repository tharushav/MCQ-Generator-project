import os
import traceback
import json
import pandas as pd
import time
from dotenv import load_dotenv
from langchain.chains import LLMChain, SequentialChain
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from src.mcq_generator.utils import read_file, get_table_data
from src.mcq_generator.logger import logging
from src.mcq_generator.mcq_generator import generate_evaluate_chain
import streamlit as st


#loading json file
with open("Response.json", "r") as file:
    response_json = json.load(file)
    
# Creating a title for the app
st.title("MCQ Generator App with LangChain 📋⛓️")

# Create a form
with st.form('user_inputs'):
    #file upload
    uploaded_file = st.file_uploader("Upload a text file")
    
    #input fields
    mcq_count = st.number_input("Number of MCQs to generate", min_value=3, max_value=20)
    
    #Subject
    subject = st.text_input("Subject", max_chars=20)
    
    # Quiz difficulty
    tone = st.selectbox("Quiz Tone", ["Easy", "Medium", "Hard"])
    
    # Submit button
    submit_button = st.form_submit_button("Generate MCQs")
    
    # Check if the submit button is clicked and all the fields are filled
    if submit_button and uploaded_file is not None and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                text = read_file(uploaded_file)
                # Track execution time for Hugging Face model
                start_time = time.time()
                response = generate_evaluate_chain(
                    {
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": json.dumps(response_json)
                            }
                )
                end_time = time.time()
                execution_time = end_time - start_time
            except StopIteration as e:
                st.error("🚫 Model provider unavailable. Please try again later or contact support.")
                st.info("💡 The Hugging Face inference service may be temporarily down for this model.")    
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"An error occurred: {e}")
                
            else:
                # Display basic metrics for Hugging Face
                st.info(f"✅ MCQs generated successfully in {execution_time:.2f} seconds")
                
                if isinstance(response, dict):
                    # extract the quiz data from the response
                    quiz_data = response.get("quiz",None)
                    if quiz_data is not None:
                        # Add debugging info
                        with st.expander("Debug Info"):
                            st.write("Raw quiz response:")
                            st.code(quiz_data)
                            
                        table_data=get_table_data(quiz_data)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index + 1
                            st.table(df)
                            # Display the review
                            st.text_area(label="Quiz Review", value=response["review"])
                            
                            # Display response metrics
                            with st.expander("Response Metrics"):
                                quiz_length = len(quiz_data)
                                review_length = len(response.get("review", ""))
                                st.write(f"**Quiz Response Length:** {quiz_length} characters")
                                st.write(f"**Review Response Length:** {review_length} characters")
                                st.write(f"**Total Response Length:** {quiz_length + review_length} characters")
                        else:
                            st.error("Error parsing quiz data. The LLM may have returned invalid JSON format.")
                            st.write("Raw response:")
                            st.code(quiz_data)
                    else:
                        st.error("No quiz data found in the response.")
                else:
                    st.write(response)