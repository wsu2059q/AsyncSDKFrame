import asyncio
import aiohttp
from typing import Optional

class Main:
    def __init__(self, sdk, logger):
        self.sdk = sdk
        self.logger = logger
        self.ai_prefix = sdk.env.get("AI_PREFIX", "/ai")
        self.has_handle = False

        if hasattr(sdk, "NormalHandler"):
            sdk.NormalHandler.AddHandle(self.handle_normal_message)
            self.logger.info("成功注册NormalHandler消息处理")
            self.has_handle = True
        if hasattr(sdk, "OneBotMessageHandler"):
            sdk.OneBotMessageHandler.AddHandle(self.handle_onebot_message)
            self.logger.info("成功注册OneBotMessageHandler消息处理")
            self.has_handle = True
        if hasattr(sdk, "ServNormal"):
            sdk.ServNormal.AddHandle(self.handle_normal_message)
            self.logger.info("成功注册ServNormal消息处理 - 并不推荐您使用同步服务器模块添加AI请求处理器，因为它会阻塞您的主程序")
            self.has_handle = True
            # self.logger.info("此模块仅支持异步消息处理器，请使用其它模块代替")

        if self.has_handle == False:
            self.logger.warning("未找到任何可用的消息处理器")

    def handle_sync_message(self, data):
        message = data.get("event", {}).get("message", {}).get("content", {}).get("text", "")

        if not message.startswith(self.ai_prefix):
            return
        
        actual_message = message[len(self.ai_prefix):].strip()

        try:
            response = self.sdk.util.ExecAsync(
                self.get_ai_response, 
                data["event"]["chat"]["chatId"], 
                actual_message
            )
            self.send_sync_response(data, response, source="yunhu")
        except Exception as e:
            self.logger.error(f"同步消息处理失败: {str(e)}")
    async def handle_normal_message(self, data):
        message = data.get("event", {}).get("message", {}).get("content", {}).get("text", "")

        if not message.startswith(self.ai_prefix):
            return
        
        actual_message = message[len(self.ai_prefix):].strip()
        response = await self.get_ai_response(data["event"]["chat"]["chatId"], actual_message)
        await self.send_response(data, response, source="yunhu")

    async def handle_onebot_message(self, data):
        raw_message = data.get("raw_message", "")
        if not raw_message.startswith(self.ai_prefix):
            return
        
        actual_message = raw_message[len(self.ai_prefix):].strip()
        chatId = data.get("user_id")
        response = await self.get_ai_response(chatId, actual_message)
        await self.send_response(data, response, source="onebot")

    async def get_ai_response(self, chatId, message: str) -> str:
        url = self.sdk.env.get("AI_API_URL", "https://api.openai.com/")
        token = self.sdk.env.get("AI_API_KEY", None)
        model = self.sdk.env.get("AI_MODEL", None)
        has_store_model = False

        self.logger.info(f"[AI] 准备调用AI接口: {url} 模型: {model} 会话id: {chatId}")
        if url is None or token is None or model is None:
            msg = "AI接口地址，令牌或模型未设置，请检查配置文件"
            self.logger.error(msg)
            return msg

        messages = []
        if hasattr(self.sdk, "AIChatMessageStore"):
            messages = await self.sdk.AIChatMessageStore.get_message_history(chatId)
            has_store_model = True
        else:
            self.logger.warning("未找到AI消息存储模块，将不保存历史对话")
        
        messages.append({"role": "user", "content": message})
        payload = {
            "model": model,
            "stream": False,
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "messages": messages
        }
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        result = await response.json()
                        ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", "未能获取回复")
                        
                        if has_store_model:
                            await self.sdk.AIChatMessageStore.add_message(chatId, "user", message)
                            await self.sdk.AIChatMessageStore.add_message(chatId, "assistant", ai_response)
                        
                        return ai_response
                    else:
                        self.logger.error(f"AI接口调用失败，状态码: {response.status}, 响应: {await response.text()}")
                        return "AI接口调用失败，请稍后再试"
        except Exception as e:
            self.logger.error(f"AI接口调用异常: {str(e)}")
            return "AI接口调用异常，请检查日志"

    async def send_response(self, original_data, response, source: str):
        if source == "yunhu":
            if hasattr(self.sdk, "MessageSender"):
                send = self.sdk.MessageSender
                self.logger.info(f"[NormalHandler] 准备发送回复: {response}")
                recv_id = original_data.get("event", {}).get("chat", {}).get("chatId")
                recv_type = original_data.get("event", {}).get("chat", {}).get("chatType")
                recv_type = 'user' if recv_type == 'bot' else 'group'
                if recv_id and recv_type:
                    result = await send.Text(
                        recvId=recv_id,
                        recvType=recv_type,
                        content=response,
                    )
            else:
                self.logger.error("云湖消息发送模块（MessageSender）未找到，请确保该模块为正常状态")
        elif source == "onebot":
            if hasattr(self.sdk, "OneBotAdapter"):
                self.logger.info(f"[OneBotMessageHandler] 准备发送回复: {response}")
                message_type = original_data.get("message_type", "private")
                user_id = original_data.get("user_id")
                group_id = original_data.get("group_id")
                
                if message_type == "private":
                    await self.sdk.OneBotAdapter.send_message(user_id, response, "private")
                elif message_type == "group":
                    await self.sdk.OneBotAdapter.send_message(group_id, response, "group")
            else:
                self.logger.error("OneBot适配器模块未找到，请确保该模块为正常状态")
        else:
            self.logger.error(f"未知的消息来源: {source}")

    def send_sync_response(self, original_data, response, source: str):
        if source == "yunhu":
            if hasattr(self.sdk, "SendMessage"):
                send = self.sdk.SendMessage
                self.logger.info(f"[NormalHandler] 准备发送回复: {response}")
                recv_id = original_data.get("event", {}).get("chat", {}).get("chatId")
                recv_type = original_data.get("event", {}).get("chat", {}).get("chatType")
                recv_type = 'user' if recv_type == 'bot' else 'group'
                if recv_id and recv_type:
                    result = send.Text(
                        recvId=recv_id,
                        recvType=recv_type,
                        content=response,
                    )