from pypresence import Presence
import time
import sys
from datetime import datetime, timedelta
import subprocess
import platform

# ═══════════════════════════════════════════════════════════════
#                    DISCORD RPC CONFIGURATION
# ═══════════════════════════════════════════════════════════════

CLIENT_ID = "1463554682172739677"

# ╔═══════════════════════════════════════════════════════════════╗
# ║                   CUSTOMIZATION OPTIONS                        ║
# ╚═══════════════════════════════════════════════════════════════╝

# ─────────────────── TIMER SETTINGS ─────────────────────
USE_CUSTOM_START_TIME = True  # Set to False to use current time
CUSTOM_START_TIME = "2000-09-13 13:30:00"  # Format: "YYYY-MM-DD HH:MM:SS"
USE_END_TIME = False  # Show countdown instead of elapsed time
CUSTOM_END_TIME = "2026-01-29 18:00:00"  # Format: "YYYY-MM-DD HH:MM:SS"

# ─────────────────── MULTIPLAYER SETTINGS ─────────────────────
ENABLE_MULTIPLAYER = True  # Show party/multiplayer info
CURRENT_PARTY_SIZE = 1  # Number of players currently joined
MAX_PARTY_SIZE = 100000  # Maximum number of players allowed
PARTY_ID = "game-session-001"  # Unique party identifier

# ─────────────────── TEXT DISPLAY ─────────────────────
MAIN_TEXT = "🎮 Expedition 33"  # Main status text (details)
SUB_TEXT = "🏆 Better than anyone loves"  # Sub status text (state)
USE_EMOJI = True  # Include emoji in text

# ─────────────────── IMAGES & ICONS ─────────────────────
# Large image (main icon)
LARGE_IMAGE_KEY = "mayel"  # Image key from Discord Developer Portal (MUST match uploaded asset)
LARGE_IMAGE_TEXT = "✨ Clair Obscur: Expedition 33"  # Hover text

# Small image (overlay icon)
USE_SMALL_IMAGE = False  # Set to True to show status icon overlay
SMALL_IMAGE_KEY = "status"  # Small icon key (e.g., for status) - MUST match uploaded asset
SMALL_IMAGE_TEXT = "🔥 On Fire!"  # Hover text for small image

# ─────────────────── BUTTONS ─────────────────────
# ⚠️ IMPORTANT: Buttons only show for OTHER users viewing your profile!
# You won't see buttons on your own profile - this is normal Discord behavior
ENABLE_BUTTONS = True
BUTTON_1_LABEL = "Join Game"  # Keep under 32 characters, avoid excessive emojis
BUTTON_1_URL = "https://discord.gg/csd"
BUTTON_2_LABEL = "Website"  # Keep under 32 characters
BUTTON_2_URL = "https://github.com/atrajit-sarkar"

# ─────────────────── ADVANCED LAYOUT OPTIONS ─────────────────────
# Custom layout templates (change anytime for different looks)
LAYOUT_TEMPLATES = {
    "gaming": {
        "details": "🎮 In Match • Battle Royale",
        "state": "💪 Going for Victory",
        "large_text": "⚔️ Epic Battle Mode",
        "small_text": "🔥 Hot Streak!"
    },
    "competitive": {
        "details": "🏆 Ranked Match • Diamond III",
        "state": "📈 Climbing the Ladder",
        "large_text": "🎯 Competitive Mode",
        "small_text": "⚡ High Performance"
    },
    "chill": {
        "details": "🌙 Chill Gaming Session",
        "state": "🎵 Vibing & Gaming",
        "large_text": "✨ Relaxed Mode",
        "small_text": "☕ Taking it Easy"
    },
    "streaming": {
        "details": "📺 Live on Stream",
        "state": "💬 Chatting with Viewers",
        "large_text": "🎥 Streaming Now",
        "small_text": "🔴 LIVE"
    },
    "custom": {
        "details": MAIN_TEXT,
        "state": SUB_TEXT,
        "large_text": LARGE_IMAGE_TEXT,
        "small_text": SMALL_IMAGE_TEXT if USE_SMALL_IMAGE else None
    }
}

# Select your preferred layout: "gaming", "competitive", "chill", "streaming", "custom"
CURRENT_LAYOUT = "custom"

# ─────────────────── DYNAMIC UPDATES ─────────────────────
AUTO_UPDATE_PARTY = False  # Automatically update party size over time (demo mode)
UPDATE_INTERVAL = 15  # Seconds between updates (if dynamic updates enabled)

# ─────────────────── DISCORD DETECTION ─────────────────────
AUTO_DETECT_DISCORD = True  # Check if Discord is running before starting
EXIT_IF_NOT_RUNNING = False  # Exit if Discord is not detected (otherwise wait)
WAIT_TIME_IF_NOT_RUNNING = 1800  # Seconds to wait before checking again

# ═══════════════════════════════════════════════════════════════
#                          FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def is_discord_running():
    """Check if Discord client is running on the system."""
    try:
        system = platform.system()
        
        if system == "Windows":
            # Check for Discord processes on Windows
            cmd = 'tasklist /FI "IMAGENAME eq Discord.exe" /FO CSV /NH'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            # Check if Discord.exe is in the output
            if "Discord.exe" in result.stdout:
                return True
            
            # Also check for DiscordCanary, DiscordPTB, etc.
            for variant in ["DiscordCanary.exe", "DiscordPTB.exe", "DiscordDevelopment.exe"]:
                cmd = f'tasklist /FI "IMAGENAME eq {variant}" /FO CSV /NH'
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if variant in result.stdout:
                    return True
            
            return False
            
        elif system == "Linux":
            # Check for Discord processes on Linux
            result = subprocess.run(["pgrep", "-f", "discord"], capture_output=True)
            return result.returncode == 0
            
        elif system == "Darwin":  # macOS
            # Check for Discord processes on macOS
            result = subprocess.run(["pgrep", "-f", "Discord"], capture_output=True)
            return result.returncode == 0
            
        else:
            print(f"⚠️ Unsupported platform: {system}")
            return True  # Assume Discord is running on unknown platforms
            
    except Exception as e:
        print(f"⚠️ Error detecting Discord: {e}")
        return True  # Assume Discord is running if detection fails

def get_timestamp(time_str):
    """Convert string timestamp to Unix epoch time."""
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    except:
        print(f"⚠️ Invalid timestamp format: {time_str}")
        return int(time.time())

def get_layout_config():
    """Get the selected layout configuration."""
    return LAYOUT_TEMPLATES.get(CURRENT_LAYOUT, LAYOUT_TEMPLATES["custom"])

def build_rpc_config():
    """Build the Rich Presence configuration with all customizations."""
    layout = get_layout_config()
    config = {}
    
    # Set main text
    config["details"] = layout["details"]
    config["state"] = layout["state"]
    
    # Set timestamps
    if USE_CUSTOM_START_TIME:
        config["start"] = get_timestamp(CUSTOM_START_TIME)
    else:
        config["start"] = int(time.time())
    
    if USE_END_TIME:
        config["end"] = get_timestamp(CUSTOM_END_TIME)
    
    # Set images
    config["large_image"] = LARGE_IMAGE_KEY
    config["large_text"] = layout["large_text"]
    
    if USE_SMALL_IMAGE:
        config["small_image"] = SMALL_IMAGE_KEY
        config["small_text"] = layout["small_text"]
    
    # Set party/multiplayer info
    if ENABLE_MULTIPLAYER:
        config["party_id"] = PARTY_ID
        config["party_size"] = [CURRENT_PARTY_SIZE, MAX_PARTY_SIZE]
    
    # Set buttons
    if ENABLE_BUTTONS:
        config["buttons"] = [
            {"label": BUTTON_1_LABEL, "url": BUTTON_1_URL},
            {"label": BUTTON_2_LABEL, "url": BUTTON_2_URL}
        ]
    
    return config

def print_banner():
    """Print a beautiful startup banner."""
    print("\n" + "═" * 70)
    print("║" + " " * 68 + "║")
    print("║" + "✨ DISCORD RICH PRESENCE - ADVANCED EDITION ✨".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("═" * 70)

def print_config_summary():
    """Print current configuration summary."""
    print("\n📋 CURRENT CONFIGURATION:")
    print("─" * 70)
    
    layout = get_layout_config()
    print(f"🎨 Layout Style: {CURRENT_LAYOUT.upper()}")
    print(f"📝 Main Text: {layout['details']}")
    print(f"📝 Sub Text: {layout['state']}")
    
    if USE_CUSTOM_START_TIME:
        print(f"⏰ Start Time: {CUSTOM_START_TIME} (Custom)")
    else:
        print(f"⏰ Start Time: Now")
    
    if USE_END_TIME:
        print(f"⏱️ End Time: {CUSTOM_END_TIME} (Countdown)")
    
    if ENABLE_MULTIPLAYER:
        print(f"👥 Multiplayer: {CURRENT_PARTY_SIZE}/{MAX_PARTY_SIZE} players")
    else:
        print(f"👤 Single Player Mode")
    
    print(f"🖼️ Large Image: {LARGE_IMAGE_KEY}")
    if USE_SMALL_IMAGE:
        print(f"🔹 Small Image: {SMALL_IMAGE_KEY}")
    
    if ENABLE_BUTTONS:
        print(f"🔘 Button 1: {BUTTON_1_LABEL}")
        print(f"🔘 Button 2: {BUTTON_2_LABEL}")
    
    print("─" * 70)
    print("✅ Rich Presence is now ACTIVE!\n")

def main():
    """Main function to run the Rich Presence."""
    print_banner()
    
    # Check if Discord is running before attempting to connect
    if AUTO_DETECT_DISCORD:
        print("\n🔍 Checking if Discord is running...")
        
        if not is_discord_running():
            print("❌ Discord client is NOT running!")
            print("\n💡 Please start Discord and try again.\n")
            
            if EXIT_IF_NOT_RUNNING:
                print("⏹️  Exiting...\n")
                sys.exit(1)
            else:
                print(f"⏳ Waiting {WAIT_TIME_IF_NOT_RUNNING} seconds before retrying...\n")
                time.sleep(WAIT_TIME_IF_NOT_RUNNING)
                return main()  # Retry
        else:
            print("✅ Discord is running! Proceeding...\n")
    
    while True:
        try:
            rpc = Presence(CLIENT_ID)
            rpc.connect()
            print("🔗 Connected to Discord!")
            
            # Build and apply configuration
            config = build_rpc_config()
            rpc.update(**config)
            
            print_config_summary()
            
            # Main loop
            counter = 0
            while True:
                time.sleep(UPDATE_INTERVAL)
                counter += 1
                
                # Optional: Demo dynamic party updates
                if AUTO_UPDATE_PARTY and counter % 4 == 0:
                    # Simulate players joining/leaving
                    import random
                    new_size = random.randint(1, MAX_PARTY_SIZE)
                    config["party_size"] = [new_size, MAX_PARTY_SIZE]
                    rpc.update(**config)
                    print(f"👥 Party updated: {new_size}/{MAX_PARTY_SIZE} players")

        except KeyboardInterrupt:
            print("\n\n⏹️  Shutting down Rich Presence...")
            print("👋 Goodbye!\n")
            sys.exit(0)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Reconnecting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()