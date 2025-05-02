import requests
from config import MODELSLAB_API_KEY


def query_img2img_modelslab(image_url: str, prompt: str) -> bytes:
    url = "https://modelslab.com/api/v6/realtime/img2img"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "key": MODELSLAB_API_KEY,
        "init_image": image_url,
        "prompt": prompt,
        "scheduler": "Euler",
        "num_inference_steps": 30,
        "guidance_scale": 7.5,
        "strength": 0.7,
        "samples": 1
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        if 'output' in result and result['output']:
            image_url = result['output'][0]
            image_response = requests.get(image_url)
            return image_response.content
        else:
            raise Exception("API hech qanday rasm qaytarmadi.")
    else:
        raise Exception(f"API xatosi: {response.status_code} - {response.text}")
