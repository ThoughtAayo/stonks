import os

from helpers import gpt_helper,pdf_helper
import multiprocessing
import streamlit as st
from tempfile import NamedTemporaryFile
from pathlib import Path
from colorama import Fore, Style

from dotenv import load_dotenv
load_dotenv()


######################################################################################################################################
# 1. Convert PDF file into images via pypdfium2
# 2. Extract text from images via pytesseract
# 3. Generate insights from OPEN AI using the extracted text

## To understand why image extraction is used, checkout:
# https://towardsdatascience.com/how-to-extract-text-from-any-pdf-and-image-for-large-language-model-2d17f02875e6 
######################################################################################################################################


def main_with_ui():
    """WIP"""
    st.set_page_config(page_title="ठटायो Stonks ", page_icon=":bird:")
    st.header("ठटायो Stonks :bird:")
    
    uploaded_files = st.file_uploader(
        "upload PDFs", accept_multiple_files=True, type=["pdf"])

    if uploaded_files is not None:
        for file in uploaded_files:
            st.write("Uploaded PDF file:", file.name)
            ## path provided as an example. Add the same file or replace with a new one
            with NamedTemporaryFile(dir='.', suffix='.csv') as f:
                print("{Fore.GREEN} getting buffer {Style.RESET_ALL}")
                f.write(file.getbuffer())
                print("{Fore.GREEN}converting pdf to image and then to text {Style.RESET_ALL}")
                pdf_text_content = pdf_helper.extract_content_from_url(f.name)
                print(pdf_text_content)
                # analysis = gpt_helper.extract_structured_data(pdf_text_content)

def main(): 
    # add your own file path here
    file_path = os.environ['SAMPLE_FILE_PATH']
    
    print(f"{Fore.GREEN} converting pdf to image and then to text {Style.RESET_ALL}")
    pdf_text_content = pdf_helper.extract_content_from_url(file_path)
    print(pdf_text_content)
    
    ## uncomment wisely, will cost you money
    # analysis = gpt_helper.extract_structured_data(pdf_text_content)
    #print(f"{Fore.GREEN} Calling open ai to get structured text from the text {Style.RESET_ALL}")
    # print(analysis)
    

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
