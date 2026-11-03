import time
import http.server
import threading
from javascript import require, On

mineflayer = require('mineflayer')

# --- DUMMY WEB SERVER FOR RENDER FREE TIER ---
def run_dummy_server():
    class SimpleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"New Builder Bot is active!")

    import os
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()


# --- MINECRAFT BUILDER BOT CONFIGURATION ---
SERVER_IP = "thekingsserver.aternos.me"
SERVER_PORT = 31641
BOT_NAME = "TheKingBuilder"       # A unique name for your new builder bot
PASSWORD = "BuildPassword123"      # Separate password for AuthMe

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
        print(f"{BOT_NAME} has joined the game!")
        time.sleep(2)
        bot.chat(f"/register {PASSWORD} {PASSWORD}")
        bot.chat(f"/login {PASSWORD}")

    @On(bot, 'chat')
    def handle_chat(this, username, message, *args):
        if username == BOT_NAME:
            return
            
        # Command to trigger the spawn building process
        if message.lower() == "!buildspawn":
            bot.chat("Understood! Activating build layout parameters now...")
            build_spawn_platform(bot)

    @On(bot, 'end')
    def handle_disconnect(*args):
        time.sleep(30)
        create_bot()

def build_spawn_platform(bot):
    pos = bot.entity.position
    
    # Automatically requests creative privileges to utilize high-level tools
    bot.chat(f"/gamemode creative {BOT_NAME}")
    time.sleep(1)
    
    # Renders a sleek 7x7 dark obsidian platform with a glowing center
    bot.chat(f"/fill {int(pos.x)-3} {int(pos.y)-1} {int(pos.z)-3} {int(pos.x)+3} {int(pos.y)-1} {int(pos.z)+3} crying_obsidian")
    time.sleep(1)
    bot.chat(f"/fill {int(pos.x)-2} {int(pos.y)-1} {int(pos.z)-2} {int(pos.x)+2} {int(pos.y)-1} {int(pos.z)+2} smooth_stone_slab")
    time.sleep(1)
    bot.chat(f"/setblock {int(pos.x)} {int(pos.y)-1} {int(pos.z)} beacon")
    
    # Places protective corner barrier pillars
    bot.chat(f"/fill {int(pos.x)-3} {int(pos.y)} {int(pos.z)-3} {int(pos.x)-3} {int(pos.y)+2} {int(pos.z)-3} chiseled_stone_bricks")
    bot.chat(f"/fill {int(pos.x)+3} {int(pos.y)} {int(pos.z)-3} {int(pos.x)+3} {int(pos.y)+2} {int(pos.z)-3} chiseled_stone_bricks")
    bot.chat(f"/fill {int(pos.x)-3} {int(pos.y)} {int(pos.z)+3} {int(pos.x)-3} {int(pos.y)+2} {int(pos.z)+3} chiseled_stone_bricks")
    bot.chat(f"/fill {int(pos.x)+3} {int(pos.y)} {int(pos.z)+3} {int(pos.x)+3} {int(pos.y)+2} {int(pos.z)+3} chiseled_stone_bricks")
    
    # Finalize spawn location anchoring
    bot.chat(f"/setworldspawn {int(pos.x)} {int(pos.y)} {int(pos.z)}")
    bot.chat("Spawn platform construction completed successfully!")

create_bot()
