from fastapi import APIRouter, UploadFile, File, Request, Form
import cv2
import numpy as np
import easyocr
from fastapi.templating import Jinja2Templates
import os

router = APIRouter(prefix="/invoice", tags=["invoice"])

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../templates'))

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...), langs: str = Form('en')):
    image_bytes = await file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    lang_list = [l.strip() for l in langs.split(',') if l.strip()]

    if 'ja' in lang_list and 'vi' in lang_list:
        reader_vi = easyocr.Reader([l for l in lang_list if l in ['en', 'vi']])
        result_vi = reader_vi.readtext(img)
        text_vi = [item[1] for item in result_vi]
        reader_ja = easyocr.Reader([l for l in lang_list if l in ['en', 'ja']])
        result_ja = reader_ja.readtext(img)
        text_ja = [item[1] for item in result_ja]
        all_text = list(dict.fromkeys(text_vi + text_ja))
        text = '\n'.join(all_text)
    else:
        reader = easyocr.Reader(lang_list)
        result = reader.readtext(img)
        text = '\n'.join([item[1] for item in result])

    return {"text": text}

@router.get("/upload-page")
def invoice_upload_page(request: Request):
    return templates.TemplateResponse("invoice_upload.html", {"request": request}) 