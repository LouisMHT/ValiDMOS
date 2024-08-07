import fitz  # PyMuPDF



def extract_text_with_details(pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)
    detailed_text = []

    # Iterate through each page
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)  # Load each page
        blocks = page.get_text("dict")["blocks"]  # Get text as dictionary

        for block in blocks:
            if "lines" in block:  # Check if the block contains lines of text
                for line in block["lines"]:
                    line_dict = {
                        "page": page_num + 1,
                        "bbox": line["bbox"],  # Bounding box of the text line
                        "text": "".join([span["text"] for span in line["spans"]]),  # The actual text
                        "font": [span["font"] for span in line["spans"]],  # Font used
                        "size": [span["size"] for span in line["spans"]],  # Font size
                    }
                    detailed_text.append(line_dict)

    return detailed_text



pdf_path = "DMOS2.pdf"
text_details = extract_text_with_details(pdf_path)

# Affichage des détails
for detail in text_details:
    #print(f"Page: {detail['page']}, BBox: {detail['bbox']}, Font: {detail['font']}, Size: {detail['size']}")
    print(f"Text: {detail['text']}\n")

print(text_details)
