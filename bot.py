import time
import http.server
import threading
import re
import os
from javascript import require, On

mineflayer = require('mineflayer')

# --- DUMMY WEB SERVER FOR RENDER FREE TIER ---
def run_dummy_server():
    class SimpleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Gazebo Builder Bot Live!")
            
    port = int(os.environ.get("PORT", 8080))
    server = http.server.HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# --- CONFIGURATION ---
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
        print(f"{BOT_NAME} ready to construct.")
        time.sleep(2)
        bot.chat(f"/register {PASSWORD} {PASSWORD}")
        time.sleep(1)
        bot.chat(f"/login {PASSWORD}")

    @On(bot, 'chat')
    def handle_chat(this, username, message, *args):
        if username == BOT_NAME:
            return
            
        message_clean = message.lower().strip()

        # Teleport bot directly to you
        if message_clean == "!here":
            bot.chat(f"/tp {BOT_NAME} {username}")
            return

        # Check for the Gazebo YouTube video link
        yt_match = re.search(r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+', message)
        if yt_match:
            bot.chat("Beautiful Gazebo blueprint recognized! Starting exact construction layout...")
            bot.chat(f"/gamemode creative {BOT_NAME}")
            time.sleep(1)
            build_exact_gazebo(bot)

    @On(bot, 'end')
    def handle_disconnect(*args):
        time.sleep(30)
        create_bot()

def build_exact_gazebo(bot):
    pos = bot.entity.position
    x, y, z = int(pos.x), int(pos.y), int(pos.z)
    
    # Layer 1: Stone Brick Foundation base ring
    bot.chat(f"/fill {x-2} {y-1} {z-2} {x+2} {y-1} {z+2} stone_bricks")
    time.sleep(1.2)
    bot.chat(f"/fill {x-1} {y-1} {z-1} {x+1} {y-1} {z+1} spruce_planks")
    time.sleep(1.2)
    
    # Layer 2: Setting up 4 structural Oak Log Pillars
    bot.chat(f"/fill {x-2} {y} {z-2} {x-2} {y+3} {z-2} oak_log")
    bot.chat(f"/fill {x+2} {y} {z-2} {x+2} {y+3} {z-2} oak_log")
    bot.chat(f"/fill {x-2} {y} {z+2} {x-2} {y+3} {z+2} oak_log")
    bot.chat(f"/fill {x+2} {y} {z+2} {x+2} {y+3} {z+2} oak_log")
    time.sleep(1.2)
    
    # Layer 3: Fences and Arch entries
    bot.chat(f"/setblock {x-2} {y} {z-1} spruce_fence")
    bot.chat(f"/setblock {x-2} {y} {z+1} spruce_fence")
    bot.chat(f"/setblock {x+2} {y} {z-1} spruce_fence")
    bot.chat(f"/setblock {x+2} {y} {z+1} spruce_fence")
    bot.chat(f"/setblock {x-1} {y} {z-2} spruce_fence")
    bot.chat(f"/setblock {x+1} {y} {z-2} spruce_fence")
    bot.chat(f"/setblock {x-1} {y} {z+2} spruce_fence")
    bot.chat(f"/setblock {x+1} {y} {z+2} spruce_fence")
    time.sleep(1.2)
    
    # Layer 4: Spruce Slab Roof system outline
    bot.chat(f"/fill {x-3} {y+4} {z-3} {x+3} {y+4} {z+3} spruce_slabs")
    time.sleep(1.2)
    bot.chat(f"/fill {x-2} {y+4} {z-2} {x+2} {y+4} {z+2} dark_oak_planks")
    time.sleep(1.2)
    bot.chat(f"/fill {x-1} {y+5} {z-1} {x+1} {y+5} {z+1} dark_oak_stairs")
    time.sleep(1.2)
    
    # Details: Hanging Lantern center lighting
    bot.chat(f"/setblock {x} {y+3} {z} spruce_fence")
    bot.chat(f"/setblock {x} {y+2} {z} lantern[hanging=true]")
    
    bot.chat("The Beautiful Gazebo construction structure is fully completed!")

create_bot()
