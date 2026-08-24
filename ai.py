import time
from datetime import datetime
import asyncio
from ollama import AsyncClient, chat, ChatResponse
from pydantic_ai import Agent
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic import BaseModel
from typing import Literal

COLORS = {
    "reset": "\033[0m",
    "warning": "\033[38;2;233;174;126m",
    "error": "\033[38;2;248;113;113m",
    "success": "\033[38;2;74;222;128m",
    "info": "\033[38;2;96;165;250m",
    "orange": "\033[38;2;249;115;22m",

}


class Assistant:

    class ToolCall(BaseModel):
        tool: Literal["weather", "calculator", "search"]
        argument: str

    def __init__(self, reasoning_model, main_model, router_model):
        self.reasoning_model = reasoning_model
        self.main_model = main_model
        self.router_model = router_model
        start = datetime.now()
        print(f"{COLORS['info']}=== Loading models! ==={COLORS['reset']}")
        

        response: ChatResponse = chat(
        
            model=self.router_model,
            messages=[
                {"role": "user", "content": "Hi"}
            ],
            keep_alive=-1,
        )

        if response["message"]["content"] is not None:
            
            print(f"{COLORS['success']}=== Models Loaded ==={COLORS['reset']}")
            end = datetime.now()
        print(f"{COLORS['info']}Total time: {(end-start).total_seconds()} seconds!{COLORS['reset']}")

        
    
    async def chat(self, message):

        chatMessages = {'role': 'user', 'content': message}
        async for part in await AsyncClient().chat(
            model=self.router_model, 
            messages=[chatMessages], 
            stream=True ):

            chunk = part['message']['content']
            if chunk:
                yield chunk

    

    async def route(self, message):
        model = OllamaModel(
            self.router_model,
            provider=OllamaProvider(
            base_url="http://localhost:11434/v1"
    ))

        agent = Agent(
            model,
            instructions="""
            You are a tool router.

            Choose exactly one tool:
            - weather: use for weather questions
            - calculator: use for mathematical calculations
            - search: use when the user wants to search for information

            Put the user's relevant request into argument like {"tool": "weather", "argument": "Tokyo"}, respond only with json.
            """,
            # output_type=Assistant.ToolCall
        )
        
        result = await agent.run(message)
        print(result.output)
    

       
        # print(f"user: {response['messages'][0]['content']}")
        # time.sleep(1)
        # for i in range(5):

        #     print(f"AI:  {response['messages'][1]["content"]}")
        #     time.sleep(1)


