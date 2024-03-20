# pdf_to_docx.py

from pdf2docx import Converter
import sys

def pdf_to_docx(pdf_file_path):
    # Extract the file name without the extension and directory path
    base_name = pdf_file_path.rsplit('.', 1)[0]
    docx_file_path = f"{base_name}.docx"

    # Initialize converter
    cv = Converter(pdf_file_path)

    # Convert PDF to DOCX
    cv.convert(docx_file_path, start=0, end=None)
    
    # Release resources
    cv.close()

    print(f"Converted '{pdf_file_path}' to '{docx_file_path}'.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <PDF file path>")
        sys.exit(1)
        
    pdf_file_path = sys.argv[1]
    pdf_to_docx(pdf_file_path)
