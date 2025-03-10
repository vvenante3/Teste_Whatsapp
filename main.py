from fastapi import FastAPI, Request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = FastAPI()

WHATSAPP_TOKEN = "EAAObuZAFhItsBO9Tn8r71Tt9wP3i4bsBkK1pb6ug6NLQh2jnatAuMcdNLFh8ZAt5tUtO2kZCe2ZBNzZAp3jy7CLJ2VOHNypiBsEGL7Ejm9DbrSGiZA175rI6ZB0sL9Y70wSsVKeK7YRzVH4QTUPBIKFMxFVUPLXWE8LhEmW6KNFXLZBhaZBldrgMoDGZAtdOj1ZAWhyoB1rhcq8mklOZBdX740b7PUiRyZB0ZD"
VERIFY_TOKEN = "batman"


@app.get("/")
def home():
    return {"stauts": "Servidor rodando!"}

@app.get("/webhook")
def verify_webhook(hub_mode: str, hub_challenge: int, hub_verify_token: str):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    return {"status": "Falha na verificação"}

@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    try:
        messages = data["entry"][0]["changes"][0]["value"]["messages"]
        for msg in messages:
            phone = msg["from"]
            text = msg["text"]["body"]

            send_message(phone, f"Você disse: {text}")
    except KeyError:
        pass
    return {"status": "Recebido"}

def send_message(phone, message):
    url = "https://graph.facebook.com/v17.0/SEU_NUMERO_ID/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }
    requests.post(url, json=data, headers=headers)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)