import time
import http.server
import threading
import re
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
    import os
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(("0.0.0.0", port), SimpleHandler)
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
        'auth': 'offline',   # Critical parameter for cracked aternos authentication
        'version': False  
    })

    @On(bot, 'spawn')
    def handle_spawn(*args):
        print(f"{BOT_NAME} has spawned into world matrix coordinates successfully.")
        time.sleep(2)
        bot.chat(f"/register {PASSWORD} {PASSWORD}")
        bot.chat(f"/login {PASSWORD}")

    @On(bot, 'chat')
    def handle_chat(this, username, message, *args):
        if username == BOT_NAME:
            return
            
        message_clean = message.lower().strip()

        # Teleport command functionality
        if message_clean == "!here":
            bot.chat(f"/tp {BOT_NAME} {username}")
            return

        # Check for video tutorial link matching parameters
        yt_match = re.search(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+', message)
        if yt_match:
            yt_url = yt_match.group(0)
            bot.chat("YouTube blueprint received! Requesting asset parsing parameters via AI context window...")
            
            # Switch into creative mode to drop blocks seamlessly
            bot.chat(f"/gamemode creative {BOT_NAME}")
            time.sleep(1)
            
            ask_ai_to_build(bot, yt_url)

    @On(bot, 'end')
    def handle_disconnect(*args):
        print("Network packet stream terminated. Attempting reconnect routing sequence...")
        time.sleep(30)
        create_bot()

def ask_ai_to_build(bot, url):
    prompt = f"""
    The user wants to replicate a structure from this specific Minecraft video: {url}.
    Generate a sequence of exactly 3 to 5 highly clean standard Minecraft /fill or /setblock commands 
    using relative coordinates (~) to build a matching shelter, statue, or layout design concept.
    Output ONLY the raw slash commands separated by newlines, nothing else. No text description or code blocks.
    """
    
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        commands = response.text.strip().split("\n")
        bot.chat("Blueprint decoded! Running coordinate filling operations...")
        
        for cmd in commands:
            if cmd.startswith("/"):
                bot.chat(cmd)
                time.sleep(1.5) # Protects against network packet flooding kicks
                
        bot.chat("AI schematic construction sequence completed.")
    except Exception as e:
        bot.chat("Error parsing design metrics. Checking authentication handshake or key format variables...")
        print(f"Exception Log Details: {e}")

create_bot()
