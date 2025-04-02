import json
import asyncio
from ErisPulse import sdk, logger
async def echo_message():
    sdk.init()
    logger.info("test")
    async def handle_message(data):
        recv_id = data.get("event", {}).get("chat", {}).get("chatId")
        recv_type = data.get("event", {}).get("chat", {}).get("chatType")
        recv_type = 'user' if recv_type == 'bot' else 'group'
        content = data.get("event", {}).get("message", {}).get("content", {}).get("text")
        if recv_id and recv_type and content:
            send = sdk.MessageSender
            result = await send.Text(
                recvId=recv_id,
                recvType=recv_type,
                content=content,
            )

    async def handle_cmd(data):
        recv_id = data.get("event", {}).get("sender", {}).get("senderId")
        recv_type = data.get("event", {}).get("chat", {}).get("chatType")
        recv_type = 'user' if recv_type == 'bot' else 'group'
        if recv_id and recv_type:
            send = sdk.MessageSender
            result = await send.Text(
                recvId=recv_id,
                recvType=recv_type,
                content="Command received!",
            )
            logger.info(result)
    
    async def handle_leave_group(data):
        recv_id = data.get("event", {}).get("chatId")
        recv_type = data.get("event", {}).get("chatType")
        recv_type = 'user' if recv_type == 'bot' else 'group'
        user_nickname = data.get("event", {}).get("nickname")

        if recv_id and recv_type and user_nickname:
            send = sdk.MessageSender
            result = await send.Text(
                recvId=recv_id,
                recvType=recv_type,
                content=f"{user_nickname} has left the group!",
            )
            logger.info(result)
    async def handle_join_group(data):
        recv_id = data.get("event", {}).get("chatId")
        recv_type = data.get("event", {}).get("chatType")
        recv_type = 'user' if recv_type == 'bot' else 'group'
        user_nickname = data.get("event", {}).get("nickname")
        
        if recv_id and recv_type and user_nickname:
            send = sdk.MessageSender
            result = await send.Text(
                recvId=recv_id,
                recvType=recv_type,
                content=f"{user_nickname} has joined the group!",
            )

    if hasattr(sdk, "NormalHandler"):
        sdk.NormalHandler.AddHandle(handle_message)
    if hasattr(sdk, "CommandHandler"):
        sdk.CommandHandler.AddHandle(handle_cmd)
    if hasattr(sdk, "LeaveGroupHandler"):
        sdk.LeaveGroupHandler.AddHandle(handle_leave_group)
    if hasattr(sdk, "JoinGroupHandler"):
        sdk.JoinGroupHandler.AddHandle(handle_join_group)
    # if hasattr(sdk, "AsyncServer"):
        # sdk.AsyncServer.AddTrigger(sdk.NormalHandler)
        # sdk.AsyncServer.AddTrigger(sdk.CommandHandler)
        # sdk.AsyncServer.AddTrigger(sdk.LeaveGroupHandler)
        # sdk.AsyncServer.AddTrigger(sdk.JoinGroupHandler)
    #     try:
    #         await sdk.AsyncServer.Run()
    #     except RuntimeError as e:
    #         pass
    async def run_servers():
        tasks = []
        # if hasattr(sdk, "AsyncServer"):
        #     tasks.append(sdk.AsyncServer.Run())
        #     sdk.AsyncServer.AddTrigger(sdk.NormalHandler)
        #     sdk.AsyncServer.AddTrigger(sdk.CommandHandler)
        #     sdk.AsyncServer.AddTrigger(sdk.LeaveGroupHandler)
        #     sdk.AsyncServer.AddTrigger(sdk.JoinGroupHandler)
        if hasattr(sdk, "Server"):
            tasks.append(sdk.Server.Start())
        if hasattr(sdk, "OneBotAdapter"):
            tasks.append(sdk.OneBotAdapter.Run())
            sdk.OneBotAdapter.AddTrigger(sdk.OneBotMessageHandler)
            sdk.OneBotAdapter.AddTrigger(sdk.OneBotNoticeHandler)
            sdk.OneBotAdapter.AddTrigger(sdk.OneBotRequestHandler)
            message_data = {
                "action": "send_private_msg",
                "params": {
                    "user_id": 2694611137,
                    "message": "这是一条测试私信消息"
                }
            }
            await sdk.OneBotAdapter.send(json.dumps(message_data))
        await asyncio.gather(*tasks)

    await run_servers()

if __name__ == "__main__":
    asyncio.run(echo_message())
