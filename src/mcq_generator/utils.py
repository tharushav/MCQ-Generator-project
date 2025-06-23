import os
import json
import PyPDF2
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader=PyPDF2.PdfFileReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
            
        except Exception as e:
            raise Exception("error reading the PDF file")
        
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception(
            "unsupported file format only pdf and text file suppoted"
            )

def get_table_data(quiz_str):
    try:
        # Check if quiz_str is empty or None
        if not quiz_str or not quiz_str.strip():
            print("Warning: Empty quiz string received")
            return None
        
        # Extract JSON content from the response string
        # Look for the first '{' and last '}' to extract the JSON portion
        start_idx = quiz_str.find('{')
        end_idx = quiz_str.rfind('}')
        
        if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
            print("Warning: No valid JSON structure found in quiz string")
            return None
        
        # Extract only the JSON portion
        json_str = quiz_str[start_idx:end_idx + 1]
        
        # convert the quiz from a str to dict
        quiz_dict=json.loads(json_str)
        quiz_table_data=[]
        
        # iterate over the quiz dictionary and extract the required information
        for key,value in quiz_dict.items():
            mcq=value["mcq"]
            options=" || ".join(
                [
                    f"{option}-> {option_value}" for option, option_value in value["options"].items()
                 
                 ]
            )
            
            correct=value["correct"]
            quiz_table_data.append({"MCQ": mcq,"Choices": options, "Correct": correct})
        
        return quiz_table_data
        
    except Exception as e:
        print(f"Error in get_table_data: {str(e)}")
        print(f"Quiz string received: {repr(quiz_str)}")
        traceback.print_exception(type(e), e, e.__traceback__)
        return None




