import runpod
import base64
import tempfile
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="en")

def handler(event):
    image_b64 = event["input"]["image"]

    img_bytes = base64.b64decode(image_b64)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as f:
        f.write(img_bytes)
        path = f.name

    result = ocr.ocr(path, cls=True)

    text = []
    for line in result[0]:
        text.append(line[1][0])

    return {
        "text": "\n".join(text)
    }

runpod.serverless.start({"handler": handler})
