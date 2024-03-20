import fitz  # PyMuPDF
import sys

def merge_pairs_in_pdf(pdf_path, output_path):
    # Open the original PDF
    doc = fitz.open(pdf_path)
    
    # Create a new PDF document for the output
    new_doc = fitz.open()

    for i in range(0, len(doc), 2):
        if i + 1 < len(doc):  # If there is a pair to process 
            first_page = doc[i]
            second_page = doc[i + 1]
            # Use the cropbox which usually defines the content area
            first_cropbox = first_page.cropbox
            second_cropbox = second_page.cropbox
            # The new height is the sum of the cropbox heights
            new_height = first_cropbox.height + second_cropbox.height
            
            # Add a blank page with the combined height
            new_page = new_doc.new_page(-1, width=first_cropbox.width, height=new_height)
            
            # Render the first and second pages on the new page
            new_page.show_pdf_page(fitz.Rect(0, 0, first_cropbox.width, first_cropbox.height), doc, i)
            new_page.show_pdf_page(fitz.Rect(0, first_cropbox.height, second_cropbox.width, new_height), doc, i + 1)
        else:
            # Handling the last page if the number of pages is odd
            last_page = doc[i]
            last_cropbox = last_page.cropbox
            new_page = new_doc.new_page(-1, width=last_cropbox.width, height=last_cropbox.height)
            new_page.show_pdf_page(fitz.Rect(0, 0, last_cropbox.width, last_cropbox.height), doc, i)

    new_doc.save(output_path)
    new_doc.close()
    doc.close()
    
    print("Joined PDF saved in " + output_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <PDF file path>")
        sys.exit(1)
        
    pdf_path = str(sys.argv[1])
    merge_pairs_in_pdf(pdf_path, pdf_path[:-4] + "-joined.pdf")