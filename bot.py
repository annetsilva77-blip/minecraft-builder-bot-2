import time
import http.server
import threading
import re
import os
from javascript import require, On
from google import genai

mineflayer = require('mineflayer')

# --- DUMMY WEB SERVER FOR RENDER FREE TIER ---
def run_dummy_server():
    class SimpleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"AI Builder Bot Live!")
            
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Dummy web server listening on port {port}")
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# --- CONFIGURATION ---
SERVER_IP = "thekingsserver.aternos.me"
SERVER_PORT = 31641
BOT_NAME = "TheKingBuilder"
PASSWORD = "BuildPassword123"
GEMINI_API_KEY = "AQ.Ab8RN6IcIIhXvnzDfRliqGgDod2ma9nb7H8d2ibgD6pUo-RlZg"

# Initialize Google Gemini Client
ai_client = genai.Client(api_key=GEMINI_API_KEY)

def create_bot():
    print(f"Connecting {BOT_NAME} to {SERVER_IP}:{SERVER_PORT}...")
    bot = mineflayer.createBot({
        'host': SERVER_IP,
        'port': SERVER_PORT,
        'username': BOT_NAME,
        'auth': 'offline',   # Required for cracked Aternos servers
        'version': False  
    })

    @On(bot, 'spawn')
    def handle_spawn(*args):
        print(f"{BOT_NAME} has spawned into the server!")
        time.sleep(2)
        bot.chat(f"/register {PASSWORD} {PASSWORD}")
        time.sleep(1)
        bot.chat(f"/login {PASSWORD}")

    @On(bot, 'chat')
    def handle_chat(this, username, message, *args):
        if username == BOT_NAME:
            return
            
        message_clean = message.lower().strip()

        # Command to teleport the bot to you
        if message_clean == "!here":
            bot.chat(f"/tp {BOT_NAME} {username}")
            return

        # Check for YouTube link
        yt_match = re.search(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+', message)
        if yt_match:
            yt_url = yt_match.group(0)
            bot.chat("YouTube link received! Asking AI to extract building layout...")
            
            # Switch into creative mode to execute /fill commands cleanly
            bot.chat(f"/gamemode creative {BOT_NAME}")
            time.sleep(1)
            
            ask_ai_to_build(bot, yt_url)

    @On(bot, 'end')
    def handle_disconnect(*args):
        print("Disconnected from server. Reconnecting in 30 seconds...")
        time.sleep(30)
        create_bot()

def ask_ai_to_build(bot, url):
    prompt = f"""
    The user wants to build a structure based on this Minecraft tutorial video: {url}.
    Generate a sequence of exactly 3 to 5 realistic standard Minecraft /fill or /setblock commands 
    using relative coordinates (~) to build a matching shelter or layout concept.
    Output ONLY the raw slash commands separated by newlines, nothing else. Do not include markdown codeblocks or explanations.
    """
    
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        commands = response.text.strip().split("\n")
        bot.chat("Blueprint generated! Starting construction...")
        
        for cmd in commands:
            if cmd.strip().startswith("/"):
                bot.chat(cmd.strip())
                time.sleep(1.5) # Protects against chat message spam limits
                
        bot.chat("AI structural build completed!")
    except Exception as e:
        bot.chat("AI could not read the layout parameters for this video right now.")
        print(f"Exception details: {e}")

create_bot()
