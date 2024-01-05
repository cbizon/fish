import os
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path):
    dname = pdf_path[:-4]
    os.mkdir(dname)
    images = convert_from_path(pdf_path)
    for index, image in enumerate(images):
        image.save(f'{dname}/{pdf_path}-{index}.png')

files=os.listdir()
for f in files:
    if f.endswith("pdf"):
        convert_pdf_to_images(f)
