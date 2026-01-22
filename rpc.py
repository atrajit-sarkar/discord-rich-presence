from pypresence import Presence
import time
import sys

CLIENT_ID = "PASTE_YOUR_APPLICATION_ID_HERE"

def main():
    while True:
        try:
            rpc = Presence(CLIENT_ID)
            rpc.connect()

            start_time = int(time.time())

            rpc.update(
                details="Expedition 33",
                state="Exploring • Deep Focus",
                start=start_time,
                large_image="clair-obscure",
                large_text="Clair Obscur",
                buttons=[
                    {"label": "Join", "url": "https://discord.com"},
                    {"label": "Website", "url": "https://github.com"}
                ]
            )

            print("Rich Presence running...")
            while True:
                time.sleep(15)

        except Exception as e:
            print("Disconnected. Reconnecting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    main()
