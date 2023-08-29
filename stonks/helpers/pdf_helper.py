import pypdfium2 as pdfium
from pytesseract import image_to_string
from PIL import Image
from io import BytesIO
from colorama import Fore, Style

def convert_pdf_to_images(file_path, scale=300/72):
    """ Convert PDF file into images via pypdfium2"""
    pdf_file = pdfium.PdfDocument(file_path)

    page_indices = [i for i in range(len(pdf_file))]

    renderer = pdf_file.render(
        pdfium.PdfBitmap.to_pil,
        page_indices=page_indices,
        scale=scale,
    )

    final_images = []

    for i, image in zip(page_indices, renderer):

        image_byte_array = BytesIO()
        image.save(image_byte_array, format='jpeg', optimize=True)
        image_byte_array = image_byte_array.getvalue()
        final_images.append(dict({i: image_byte_array}))

    return final_images

def extract_text_from_img(list_dict_final_images):
    """Extract text from images via pytesseract"""
    image_list = [list(data.values())[0] for data in list_dict_final_images]
    image_content = []

    for index, image_bytes in enumerate(image_list):
        image = Image.open(BytesIO(image_bytes))
        raw_text = str(image_to_string(image))
        image_content.append(raw_text)

    return "\n".join(image_content)

def extract_content_from_url(url: str):
    """connect pdf to image and image to text functions to generate pdf -> image -> text"""
    print(f"{Fore.GREEN} running convert_pdf_to_images with file path {url} {Style.RESET_ALL}")
    images_list = convert_pdf_to_images(url)
    
    print(f"{Fore.GREEN} running extract_text_from_img {Style.RESET_ALL}")
    text_with_pytesseract = extract_text_from_img(images_list)

    return text_with_pytesseract