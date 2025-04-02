import asyncio
from typing import List, Dict

class Main:
    def __init__(self, sdk, logger):
        self.sdk = sdk
        self.logger = logger
        self.message_store = {}  # {chatId: [messages]}

    async def get_message_history(self, chatId) -> List[Dict]:
        return self.message_store.get(chatId, [])

    async def add_message(self, chatId, role: str, content: str):
        if chatId not in self.message_store:
            self.message_store[chatId] = []
        
        self.message_store[chatId].append({
            "role": role,
            "content": content
        })
        self.logger.info(f"已存储新消息到聊天 {chatId}")

    async def clear_history(self, chatId):
        if chatId in self.message_store:
            del self.message_store[chatId]
            self.logger.info(f"已清除聊天 {chatId} 的历史消息")
