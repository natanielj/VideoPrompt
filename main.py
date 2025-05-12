from IPython.display import display, Image, Audio
import cv2 
import base64
import time
from openai import OpenAI
import os
# import requests
from dotenv import load_dotenv
# import PIL import Image

# load api key from .env file
load_dotenv()

key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# load video
video = cv2.VideoCapture("./hazards/Hazard_Car 8.mp4")

# read each video frames and add each frame to a list after converting to base64
base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release() # release/end video capture
print(len(base64Frames), "frames read")

# Display each frame seperately in the video
for img in base64Frames:
    display(Image(data=base64.b64decode(img.encode("utf-8")), format='jpeg'))
    time.sleep(0.025)

# Go through each frame and generate a description of the video
PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are videos of human driven cars. Generate a description of the video with all the road conditions, hazards to the car including other objects, or cars. Identify all possible dangers to the car and the driver. Preferably output in list form",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
        ],
    },
]
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}
# Define Hazard, Position of each actor

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)


