import asyncio
from ErisPulse import sdk, logger

async def main():
    sdk.init()
    env    = sdk.env
    
    if hasattr(sdk, "Server"):
        sdk.Server.Start()
    if hasattr(sdk, "NormalHandler") and hasattr(sdk, "AsyncServer"):
        sdk.AsyncServer.AddTrigger(sdk.NormalHandler)
        sdk.NormalHandler.AddHandle(handle_message)
        await sdk.AsyncServer.Run()

if __name__ == "__main__":
    asyncio.run(main())