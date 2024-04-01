from fastapi import FastAPI, HTTPException, Form
import requests

app = FastAPI()

MIDJOURNEY_API_URL = "https://api.userapi.ai/midjourney/v2"
MIDJOURNEY_API_KEY = "81ffded2-61b6-4f25-a75f-49a11ff2478b"

@app.post("/imagine")
async def imagine(
    prompt: str = Form(...),
    webhook_url: str = Form(None),
    webhook_type: str = Form("result"),
    account_hash: str = Form(None),
    is_disable_prefilter: bool = Form(False),
):
    url = f"{MIDJOURNEY_API_URL}/imagine"
    headers = {
        "api-key": MIDJOURNEY_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "webhook_url": webhook_url,
        "webhook_type": webhook_type,
        "account_hash": account_hash,
        "is_disable_prefilter": is_disable_prefilter,
    }
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    task_hash = response_data.get("hash")
    status_url = f"{MIDJOURNEY_API_URL}/status?hash={task_hash}"
    while True:
        status_response = requests.get(status_url, headers=headers)
        status_response_data = status_response.json()
        if status_response_data.get("status") == "done":
            urls = status_response_data.get("result", {}).get("url")
            return {"urls": urls}
