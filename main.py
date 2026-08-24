from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio


COLORS = {
    "reset": "\033[0m",
    "warning": "\033[38;2;233;174;126m",
    "error": "\033[38;2;248;113;113m",
    "success": "\033[38;2;74;222;128m",
    "info": "\033[38;2;96;165;250m",
    "orange": "\033[38;2;249;115;22m",

}

import time
from configuration import Config
# from messageSend import Messenger
from ai import Assistant
import asyncio




app = FastAPI()
assistant = Assistant("qwen30B", "qwen_main", "reaperdoesntrun/Qwen3-0.6B-Distilled:latest")

@app.get("/")
async def get():

    p1 = Assistant("qwen30B", "qwen_main", "reaperdoesntrun/Qwen3-0.6B-Distilled:latest")
    await p1.route("What's the weather in Tokyo?")    
    with open("templates/index.html") as f:
        return HTMLResponse(f.read())


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    print("Client connected!")
    

    while True:

        message = await websocket.receive_text()
        print("Client:", message)
            
        
        async for chunk in assistant.chat(message):
            await websocket.send_text(chunk)
            print(chunk)




