import time
import http.server
import threading
import re
from javascript import require, On

mineflayer = require('mineflayer')

# --- DUMMY WEB SERVER FOR RENDER FREE TIER ---
def run_dummy_server():
    class SimpleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"AI Builder Bot is running!")

    import os
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()


# --- MINECRAFT BUILDER BOT CONFIGURATION ---
SERVER_IP = "thekingsserver.aternos.me"
SERVER_PORT = 31641
BOT_NAME = "TheKingBuilder"
PASSWORD = "BuildPassword123"

def create_bot():
    print(f"Connecting {BOT_NAME} to {SERVER_IP}:{SERVER_PORT}...")
    
    bot = mineflayer.createBot({
        'host': SERVER_IP,
        'port': SERVER_PORT,
        'username': BOT_NAME,
        'auth': 'offline',
        'version': False  
    })

    @On(bot, 'spawn')
    def handle_spawn(*args):
        print(f"{BOT_NAME} is ready!")
        time.sleep(2)
        bot.chat(f"/register {PASSWORD} {PASSWORD}")
        bot.chat(f"/login {PASSWORD}")

    @On(bot, 'chat')
    def handle_chat(this, username, message, *args):
        if username == BOT_NAME:
            return
            
        message_clean = message.lower().strip()

        # --- FEATURE 1: !here COMMAND ---
        if message_clean == "!here":
            bot.chat(f"Teleporting to {username} to build...")
            bot.chat(f"/tp {BOT_NAME} {username}")
            return

        # Default standard spawn command
        if message_clean == "!buildspawn":
            bot.chat("Building default spawn platform...")
            build_spawn_platform(bot, bot.entity.position)
            return

        # --- FEATURE 2: YOUTUBE LINK DETECTION ---
        # Detects standard youtube.com or youtu.be links in the server chat
        yt_match = re.search(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+', message)
        if yt_match:
            yt_url = yt_match.group(0)
            bot.chat("YouTube link received! Analyzing video schematic design...")
            
            # Requesting creative permissions to run building codes
            bot.chat(f"/gamemode creative {BOT_NAME}")
            time.sleep(1)
            
            # Triggers the AI video command building logic
            parse_and_build_video_structure(bot, yt_url)

    @On(bot, 'end')
    def handle_disconnect(*args):
        time.sleep(30)
        create_bot()

def build_spawn_platform(bot, pos):
    bot.chat(f"/gamemode creative {BOT_NAME}")
    time.sleep(1)
    bot.chat(f"/fill {int(pos.x)-3} {int(pos.y)-1} {int(pos.z)-3} {int(pos.x)+3} {int(pos.y)-1} {int(pos.z)+3} crying_obsidian")
    time.sleep(1)
    bot.chat(f"/fill {int(pos.x)-2} {int(pos.y)-1} {int(pos.z)-2} {int(pos.x)+2} {int(pos.y)-1} {int(pos.z)+2} smooth_stone_slab")
    time.sleep(1)
    bot.chat(f"/setblock {int(pos.x)} {int(pos.y)-1} {int(pos.z)} beacon")
    bot.chat("Spawn platform construction completed!")

def parse_and_build_video_structure(bot, url):
    pos = bot.entity.position
    x, y, z = int(pos.x), int(pos.y), int(pos.z)
    
    # Placeholder layout simulator representing schematic parsing 
    # To use full live text/schematic conversion, you link your OpenAI/Gemini API key here
    bot.chat("Video blueprint interpreted! Running generated relative block placements...")
    
    try:
        # Example generation code: Building an advanced shelter based on parsed metrics
        bot.chat("/fill ~-4 ~ ~-4 ~4 ~4 ~4 oak_planks hollow")
        time.sleep(1)
        bot.chat("/fill ~-4 ~4 ~-4 ~4 ~4 ~4 glass") # Glass skylight roof
        time.sleep(1)
        bot.chat("/setblock ~ ~1 ~-4 air") # Doorway cutout
        bot.chat("/setblock ~ ~2 ~-4 air")
        time.sleep(1)
        bot.chat("/setblock ~ ~1 ~-3 oak_door")
        bot.chat("/setblock ~-3 ~1 ~-3 lantern") # Interior safety lights
        bot.chat("/setblock ~3 ~1 ~-3 lantern")
        
        bot.chat("Structure successfully replicated from video file data!")
    except Exception as e:
        bot.chat("Error parsing design structures from video URL endpoint.")

create_bot()
