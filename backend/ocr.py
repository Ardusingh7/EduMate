# Authentication to Google API
import os
from google.cloud import vision


class OCR:

    def __init__(self):
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] ='hackdu-414916-12efc7ed4d0e.json'
        self.client = vision.ImageAnnotatorClient()
    
    def detect_text(self,path):    

        with open(path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = self.client.document_text_detection(image=image)
        texts = response.text_annotations
        ocr_text = []

        for text in texts:
            ocr_text.append(f"{text.description}")

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )
        return ocr_text

