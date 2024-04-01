from fastapi import FastAPI, HTTPException, Form
import httpx

app = FastAPI()

MIDJOURNEY_API_URL = "https://api.userapi.ai/midjourney/v2"
MIDJOURNEY_API_KEY = "81ffded2-61b6-4f25-a75f-49a11ff2478b"

async def post_request(url, data, headers):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, headers=headers)
    return response.json()

async def get_request(url, headers):
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    return response.json()

@app.post("/imagine")
async def imagine(
    prompt: str = Form(...),
    webhook_url: str = Form(None),
    webhook_type: str = Form("result"),
    account_hash: str = Form(None),
    is_disable_prefilter: bool = Form(False),
):
    url = f"{MIDJOURNEY_API_URL}/imagine"
    headers = {"api-key": MIDJOURNEY_API_KEY}
    data = {
        "prompt": prompt,
        "webhook_url": webhook_url,
        "webhook_type": webhook_type,
        "account_hash": account_hash,
        "is_disable_prefilter": is_disable_prefilter,
    }
    response_data = await post_request(url, data, headers)
    task_hash = response_data.get("hash")
    return await get_task_status(task_hash)

async def get_task_status(task_hash: str):
    status_url = f"{MIDJOURNEY_API_URL}/status?hash={task_hash}"
    headers = {
        "api-key": MIDJOURNEY_API_KEY,
        "Content-Type": "application/json"
    }
    while True:
        status_response_data = await get_request(status_url, headers)
        if status_response_data.get("status") == "done":
            urls = status_response_data.get("result", {}).get("url")
            return {"urls": urls}


