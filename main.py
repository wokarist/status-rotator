import json
import time
import random
import asyncio
import aiohttp
import os
from datetime import datetime
from colorama import Fore, Style, init

#######################################
#####         Coded by Wok        #####
#######################################

class DiscordStatusRotator:
    def __init__(self):
        init()
        self.config = self.load_config()
        self.messages = self.load_messages()
        self.headers = {
            'Authorization': self.config['token'],
            'Content-Type': 'application/json'
        }
        self.api_url = 'https://discord.com/api/v9/users/@me/settings'

    def load_config(self):
        if not os.path.exists('config.json'):
            default_config = {
                "token": "YOUR_TOKEN_HERE",
                "emojis": ["", "", ""],
                "change_time": 10, 
                "random_order": True,
                "include_emoji": True 
            }
            with open('config.json', 'w') as f:
                json.dump(default_config, f, indent=4)
            print("created ''config.json''")
            exit(1)
        
        with open('config.json', 'r') as f:
            return json.load(f)

    def load_messages(self):
        if not os.path.exists('text.txt'):
            example_messages = [
                "test1",
                "test2",
                "test3",
                "test4",
                "test5"
            ]
            with open('text.txt', 'w') as f:
                f.write('\n'.join(example_messages))
            print("created ''text.txt''")
            exit(1)
        
        with open('text.txt', 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines() if line.strip()]

    async def update_status(self, message, emoji=None):
        status_data = {
            "custom_status": {
                "text": message
            }
        }
        
        if emoji and self.config['include_emoji']:
            status_data["custom_status"]["emoji_name"] = emoji
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(self.api_url, headers=self.headers, json=status_data) as response:
                    current_time = datetime.now().strftime("%H:%M:%S")
                    token_preview = self.config['token'][:12]
                    
                    if response.status == 200:
                        status_text = f"{emoji + ' ' if emoji else ''}{message}"
                        print(f"[{Fore.GREEN}{current_time}{Style.RESET_ALL}] Status changed to: {Fore.LIGHTBLUE_EX}{status_text}{Style.RESET_ALL} | {Fore.GREEN}{token_preview}..{Style.RESET_ALL}")
                    else:
                        response_text = await response.text()
                        print(f"[{Fore.GREEN}{current_time}{Style.RESET_ALL}] failed to update status {response.status} - {response_text}")
        except Exception as e:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{Fore.GREEN}{current_time}{Style.RESET_ALL}] error updating status {e}")

    async def run(self):
        if not self.messages:
            print("no messages found in text.txt")
            return
        
        try:
            while True:
                messages_to_use = self.messages.copy()
                
                if self.config['random_order']:
                    random.shuffle(messages_to_use)
                
                for message in messages_to_use:
                    emoji = random.choice(self.config['emojis']) if self.config['include_emoji'] else None
                    await self.update_status(message, emoji)
                    await asyncio.sleep(self.config['change_time'])
        except KeyboardInterrupt:
            print("\nstatus rotator stopped")
        except Exception as e:
            print(f"an error occurred: {e}")

if __name__ == "__main__":
    print("Coded By Wokarist")
    rotator = DiscordStatusRotator()
    
    if rotator.config['token'] == "YOUR_TOKEN_HERE":
        print("please edit config.json and add your token")
        exit(1)
    
    asyncio.run(rotator.run())
