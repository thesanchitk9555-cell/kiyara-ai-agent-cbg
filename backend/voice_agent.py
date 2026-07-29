import asyncio
import os
from dotenv import load_dotenv
from videosdk_agents import VoiceAgent, VideoSDKConfig # VideoSDK's native agent framework
from videosdk_agents.models import GeminiRealtimeModel # Native Gemini Realtime integration

# Load environment variables
load_dotenv()

async def start_kiyara_voice_agent():
    print("Initializing Kiyara Voice Agent...")
    
    # 1. Setup VideoSDK Configuration
    vsdk_config = VideoSDKConfig(
        api_key=os.getenv("VIDEOSDK_API_KEY"),
        secret_key=os.getenv("VIDEOSDK_SECRET"),
        room_id="kiyara_autonomous_room"
    )
    
    # 2. Setup Google Gemini Realtime API (No ElevenLabs needed)
    # Gemini Realtime directly handles speech-to-speech with ultra-low latency
    gemini_model = GeminiRealtimeModel(
        api_key=os.getenv("GEMINI_API_KEY"),
        model_name="gemini-1.5-pro-realtime",
        system_instruction="You are Kiyara, the official female tele-counselor for Chandra Bhanu Gupt Agriculture PG College. Speak warmly and naturally in Hinglish.",
        voice="Aoede" # One of Gemini's native human-like female voices
    )
    
    # 3. Create and Connect the Voice Agent
    agent = VoiceAgent(
        config=vsdk_config,
        llm_model=gemini_model
    )
    
    print("Kiyara is now ONLINE and listening for calls using Gemini Realtime API...")
    await agent.connect()
    
    # Keep the async loop running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    # Using AsyncIO as specified in the tech stack
    asyncio.run(start_kiyara_voice_agent())
