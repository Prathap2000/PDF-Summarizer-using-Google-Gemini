import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDF text extraction

# Load environment variables from .env file
load_dotenv()

# Configure API key for Google Gemini
genai.configure(api_key=os.getenv('API_KEY'))

# Streamlit app layout
st.title('PDF Summarizer using Google Gemini')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_file:
        for page in pdf_file:
            text += page.get_text()
    return text

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
if uploaded_file is not None:
    # Save the uploaded file temporarily
    pdf_path = "temp_pdf.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("PDF uploaded successfully!")

    # Allow user to specify the number of lines for the summary
    num_lines = st.number_input("Number of lines for summary:", min_value=1, max_value=20, value=5)

    # Create a GenerativeModel instance
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Button to generate summary
    if st.button("Get Summary"):
        # Upload the PDF file to the Gemini API
        try:
            sample_pdf = genai.upload_file(pdf_path)  # Use the correct path for the uploaded file
            
            # Generate content (summary) using the Gemini API
            response = model.generate_content([
                f"Give me a summary of this PDF file in {num_lines} lines.", 
                sample_pdf
            ])

            # Display the summary
            st.subheader("Summary Result:")
            if hasattr(response, 'text') and response.text:
                st.markdown(response.text)  # Show the summary in markdown for better readability
            else:
                st.error("No summary returned. Please check the PDF content or try another document.")

        except Exception as e:
            st.error(f"An error occurred while generating the summary: {str(e)}")
