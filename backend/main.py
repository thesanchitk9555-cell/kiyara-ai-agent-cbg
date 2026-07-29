import os
import resend
import httpx
from fastapi import FastAPI, Request, BackgroundTasks
from litellm import completion
from database import init_db

app = FastAPI(title="Kiyara AI Agent")
resend.api_key = os.getenv("RESEND_API_KEY")

KIYARA_MASTER_PROMPT = """
You are Kiyara, the official tele-counselor, admission advisor, and administrative assistant for Chandra Bhanu Gupt Agriculture Post Graduate College (located in BKT, Lucknow). 
You are a real human female staff member. You are speaking to students, parents, or callers over a live phone call or WhatsApp chat.

YOUR PERSONALITY & TONE:
- Tone: Warm, polite, professional, and empathetic.
- Language: Natural conversational Hinglish (A seamless mix of Hindi and English).
- Voice/Chat format: Keep your responses short, conversational, and easy to understand (maximum 2 to 3 short sentences per turn).

STRICT RULES YOU MUST FOLLOW:
1. NEVER REVEAL YOU ARE AN AI: Act 100% human.
2. CONVERSATION FLOW: Always guide the conversation. Ask a gentle follow-up question at the end.
3. HANDLING MISSING INFO: If a user asks a highly specific question that you don't know, DO NOT make up answers. Say: "Maaf kijiye, iski exact details abhi mere paas nahi hain. Main office se confirm karke update kar deti hoon."

CORE COLLEGE KNOWLEDGE BASE:
- Affiliation: Lucknow University.
- Courses: B.Sc. (Hons) Agriculture (4 years) & M.Sc. Agriculture (2 years).
- Facilities: Own agricultural farm for practicals, well-equipped labs, library, and active NSS units.
- Fees & Finance: Self-financed (approx 25k-35k per semester). UP Dashmottar Scholarship is available based on income certificates.
"""

@app.on_event("startup")
async def on_startup():
    await init_db()

def get_ai_response(prompt: str) -> str:
    models = ["gemini/gemini-1.5-pro-latest", "openai/gpt-4o", "deepseek/deepseek-chat"]
    for model in models:
        try:
            response = completion(
                model=model,
                messages=[
                    {"role": "system", "content": KIYARA_MASTER_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                timeout=7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue
    return "Maaf kijiye, network mein thodi samasya hai. Kya aap apna sawal dohra sakte hain?"

def send_data_to_email(data: dict):
    html_content = f"<h3>New Data Collected by Kiyara AI</h3><p><strong>Phone:</strong> {data.get('phone')}</p><p><strong>Message:</strong> {data.get('message')}</p>"
    try:
        resend.Emails.send({
            "from": "Kiyara AI <kiyara@yourcollege.edu>",
            "to": "admin@college.edu",
            "subject": "New College Inquiry via AI Agent",
            "html": html_content
        })
    except Exception as e:
        print(f"Email error: {e}")

@app.post("/whatsapp/webhook")
async def whatsapp_webhook(request: Request, bg_tasks: BackgroundTasks):
    try:
        data = await request.json()
        
        message_data = data.get("message", {})
        user_msg = message_data.get("body")
        user_phone = message_data.get("from")
        
        # Ignore automated bot messages
        if message_data.get("fromMe") or not user_msg:
            return {"status": "ignored"}

        reply = get_ai_response(user_msg)
        bg_tasks.add_task(send_data_to_email, {"phone": user_phone, "message": user_msg})
        
        # Waapi.app Send Message Action
        waapi_url = f"https://waapi.app/api/v1/instances/{os.getenv('WAAPI_INSTANCE_ID')}/client/action/send-message"
        headers = {
            "Authorization": f"Bearer {os.getenv('WAAPI_API_TOKEN')}",
            "Content-Type": "application/json"
        }
        payload = {
            "chatId": user_phone,
            "message": reply
        }
        
        async with httpx.AsyncClient() as client:
            await client.post(waapi_url, headers=headers, json=payload)
            
        return {"status": "success", "ai_reply": reply}
    except Exception as e:
        print(f"Waapi Webhook Error: {e}")
        return {"status": "error"}
