# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# # Load the pre-trained model and tokenizer
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

# # Create a translation pipeline
# translator = pipeline(
#     'translation', 
#     model=model, 
#     tokenizer=tokenizer, 
#     src_lang="fra_Latn", 
#     tgt_lang='eng_Latn', 
#     max_length=400
# )

# # Translate a sample text
# translated_text = translator(" De l'espèce oncorhynchus mykiss pesant plus de 400 g pièce:")
# print(translated_text)

#########################################(for pdf)
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# import fitz  # PyMuPDF
# # import pdfplumber

# # Load the pre-trained model and tokenizer
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

# # Create a translation pipeline
# translator = pipeline(
#     'translation', 
#     model=model, 
#     tokenizer=tokenizer, 
#     src_lang="heb_Hebr", 
#     tgt_lang='eng_Latn', 
#     max_length=1024
# )

# def extract_text_from_pdf(pdf_path):
#     """Extract text from a PDF file."""
#     text = ""
#     # Using PyMuPDF (fitz)
#     with fitz.open(pdf_path) as doc:
#         for page in doc:
#             text += page.get_text()
    
#     # Alternative using pdfplumber
#     # with pdfplumber.open(pdf_path) as pdf:
#     #     for page in pdf.pages:
#     #         text += page.extract_text()

#     return text

# def translate_text(text):
#     """Translate the provided text using the translation pipeline."""
#     return translator(text)

# def main(pdf_path):
#     text = extract_text_from_pdf(pdf_path)
#     if text:
#         translated_text = translate_text(text)
#         print(translated_text)
#     else:
#         print("No text found in the PDF.")

# # Example usage
# pdf_path = r"C:\Users\AMALVIYA\Downloads\hebrew_removed_removed.pdf"  # Replace with your PDF file path
# main(pdf_path)





###############(with excel)
# import pandas as pd
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# # Load the pre-trained model and tokenizer
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

# # Create a translation pipeline
# translator = pipeline(
#     'translation', 
#     model=model, 
#     tokenizer=tokenizer, 
#     src_lang="spa_Latn", 
#     tgt_lang='eng_Latn', 
#     max_length=400
# )

# # Path to the Excel file
# file_path = r"C:\Users\AMALVIYA\Downloads\HS Description Translation.xlsx"

# # Read the Excel file
# df = pd.read_excel(file_path, sheet_name='1')

# # Ensure the 'native_langauge' column exists
# if 'native_langauge' not in df.columns:
#     raise ValueError("The column 'native_langauge' does not exist in the sheet")

# # Translate the text in the 'native_langauge' column
# def translate_text(text):
#     # Handling empty or NaN values
#     if pd.isna(text):
#         return text
#     translated = translator(text)
#     return translated[0]['translation_text']

# # Apply translation to the column
# df['translated_text'] = df['native_langauge'].apply(translate_text)

# # Write the updated DataFrame back to the Excel file
# # Note: Make sure to use 'openpyxl' engine to handle xlsx format
# df.to_excel(file_path, sheet_name='1', index=False, engine='openpyxl')

# print("Translation completed and saved successfully.")



#######(with ui for text pdf and excel)
import streamlit as st
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import fitz  # PyMuPDF

# Load the pre-trained model and tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

# Create a translation pipeline
def get_translator(src_lang, tgt_lang):
    return pipeline(
        'translation',
        model=model,
        tokenizer=tokenizer,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
        max_length=400
    )

def translate_text(text, translator):
    if pd.isna(text):
        return text
    translated = translator(text)
    return translated[0]['translation_text']

# Streamlit UI
st.title("Multilingual Translation Tool")

option = st.selectbox("Select Translation Mode", ["Text", "PDF", "Excel"])

src_lang = st.text_input("Source Language Code (e.g., 'spa_Latn' for Spanish)", "spa_Latn")
tgt_lang = st.text_input("Target Language Code (e.g., 'eng_Latn' for English)", "eng_Latn")

translator = get_translator(src_lang, tgt_lang)

if option == "Text":
    text_input = st.text_area("Enter Text to Translate")
    if st.button("Translate"):
        if text_input:
            translated_text = translate_text(text_input, translator)
            st.write("Translated Text:")
            st.write(translated_text)
        else:
            st.warning("Please enter some text for translation.")

elif option == "PDF":
    pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])
    if pdf_file:
        # Extract text from PDF
        text = ""
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

        if text:
            translated_text = translate_text(text, translator)
            st.write("Translated Text:")
            st.write(translated_text)
        else:
            st.warning("No text found in the PDF.")

elif option == "Excel":
    excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if excel_file:
        sheet_name = st.text_input("Enter Sheet Name")
        column_name = st.text_input("Enter Column Name")
        if st.button("Translate Excel"):
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            if column_name in df.columns:
                df['translated_text'] = df[column_name].apply(lambda x: translate_text(x, translator))
                output_file_path = "translated_" + excel_file.name
                df.to_excel(output_file_path, sheet_name=sheet_name, index=False, engine='openpyxl')
                st.success("Translation completed and saved successfully.")
                st.write(f"File has been saved as {output_file_path}. You can download it below:")
                st.download_button("Download Translated Excel File", data=open(output_file_path, "rb").read(), file_name=output_file_path)
            else:
                st.error(f"Column '{column_name}' does not exist in the sheet '{sheet_name}'.")


# import streamlit as st
# import pandas as pd
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
# import fitz  # PyMuPDF
# import config  # Import the config.py file

# # Load the pre-trained model and tokenizer
# model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
# tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")

# # Create a translation pipeline
# def get_translator(src_lang, tgt_lang):
#     return pipeline(
#         'translation',
#         model=model,
#         tokenizer=tokenizer,
#         src_lang=src_lang,
#         tgt_lang=tgt_lang,
#         max_length=400
#     )

# def translate_text(text, translator):
#     if pd.isna(text):
#         return text
#     translated = translator(text)
#     return translated[0]['translation_text']

# def show_language_codes():
#     st.write("### Language Codes")
#     codes_df = pd.DataFrame(list(config.LANGUAGE_CODES.items()), columns=["Language", "Code"])
#     st.dataframe(codes_df)

# # Streamlit UI
# st.title("Multilingual Translation Tool")

# option = st.selectbox("Select Translation Mode", ["Text", "PDF", "Excel"])

# if st.button("Show Language Codes"):
#     show_language_codes()

# src_lang = st.text_input("Source Language Code (e.g., 'spa_Latn' for Spanish)")
# tgt_lang = st.text_input("Target Language Code (e.g., 'eng_Latn' for English)")

# translator = get_translator(src_lang, tgt_lang)

# if option == "Text":
#     text_input = st.text_area("Enter Text to Translate")
#     if st.button("Translate"):
#         if text_input:
#             translated_text = translate_text(text_input, translator)
#             st.write("Translated Text:")
#             st.write(translated_text)
#         else:
#             st.warning("Please enter some text for translation.")

# elif option == "PDF":
#     pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])
#     if pdf_file:
#         # Extract text from PDF
#         text = ""
#         with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
#             for page in doc:
#                 text += page.get_text()

#         if text:
#             translated_text = translate_text(text, translator)
#             st.write("Translated Text:")
#             st.write(translated_text)
#         else:
#             st.warning("No text found in the PDF.")

# elif option == "Excel":
#     excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])
#     if excel_file:
#         sheet_name = st.text_input("Enter Sheet Name")
#         column_name = st.text_input("Enter Column Name")
#         if st.button("Translate Excel"):
#             df = pd.read_excel(excel_file, sheet_name=sheet_name)
#             if column_name in df.columns:
#                 df['translated_text'] = df[column_name].apply(lambda x: translate_text(x, translator))
#                 output_file_path = "translated_" + excel_file.name
#                 df.to_excel(output_file_path, sheet_name=sheet_name, index=False, engine='openpyxl')
#                 st.success("Translation completed and saved successfully.")
#                 st.write(f"File has been saved as {output_file_path}. You can download it below:")
#                 st.download_button("Download Translated Excel File", data=open(output_file_path, "rb").read(), file_name=output_file_path)
#             else:
#                 st.error(f"Column '{column_name}' does not exist in the sheet '{sheet_name}'.")
