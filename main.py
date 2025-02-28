# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()

# client = OpenAI()

# import ollama

from IPython.display import display, Image, Audio
import cv2 
import base64
import time
from openai import OpenAI
import os
import requests
from dotenv import load_dotenv
# import PIL import Image


load_dotenv()

key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# chat = ollama.chat(model="")

video = cv2.VideoCapture("./hazards/hazard0.mp4")

base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()
print(len(base64Frames), "frames read")

display_handle = display(None, display_id=True)
for img in base64Frames:
    curr_frame = base64.b64decode(img.encode("utf-8"))
    display_handle.update(Image(data=curr_frame))
    time.sleep(0.025)

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are videos of human driven cars. Generate a description of the video with all the road conditions, hazards to the car including other objects, or cars",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
        ],
    },
]
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)


