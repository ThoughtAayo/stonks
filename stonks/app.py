import atexit
from colorama import Fore, Style
from dotenv import load_dotenv
import glob
import multiprocessing
import os

from helpers import pdf_helper, vector_db_helper, ui_helper


load_dotenv()


######################################################################################################################################
# 1. Convert PDF file into images via pypdfium2
# 2. Extract text from images via pytesseract
# 3. Generate insights from OPEN AI using the extracted text

## To understand why image extraction is used, checkout:
# https://towardsdatascience.com/how-to-extract-text-from-any-pdf-and-image-for-large-language-model-2d17f02875e6
######################################################################################################################################


def main():
    """"""
    # add your own file path here
    file_path = os.environ["SAMPLE_FILE_PATH"]

    # Extract docs from pdf
    print(f"{Fore.GREEN} converting pdf to image and then to text {Style.RESET_ALL}")
    pdf_text_contents = pdf_helper.extract_content_from_url(file_path)
    print("\n".join(pdf_text_contents))

    # generate embeddings from docs and save to vector db
    vectorDb = vector_db_helper.VectorDbHelper(persist_to_disk=True)
    vectorDb.generate_embeddings_and_save_to_db(pdf_text_contents)

    ## uncomment wisely, will cost you money
    ## query LLM
    # chat_gpt_ans = gpt_helper.query('What is the total net sales for the quarter ending on April 1 2023?')
    # print(chat_gpt_ans)


def exit_handler():
    """"""
    print("stonks application is ending! Performing cleanups")
    temp_file_path = os.path.join(os.getcwd(), "stonks/storage/tempFiles")
    files = glob.glob(temp_file_path)
    try:
        for f in files:
            os.remove(f)
    except:
        print("Could not automatically delete temp files. Please remove them manually")


if __name__ == "__main__":
    atexit.register(exit_handler)
    multiprocessing.freeze_support()
    ## main()
    ui_helper.init(show_chat_history=True)
