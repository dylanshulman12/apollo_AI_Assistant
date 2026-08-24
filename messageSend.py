import asyncio


# Example code! Too lazy to implement but i will try with asyncio later
# async def main():
#     client = BeeperClient(
#         access_token=TOKEN,
#     )

#     # Find your chats
#     chats = await client.chats.list()

#     for chat in chats:
#         print(chat.id, chat.title)

#     # Pick a chat
#     chat_id = chats[0].id

#     # Send a message
#     result = await client.messages.send(
#         chat_id=chat_id,
#         text="Hello from Python!"
#     )

#     print("Sent:", result)

#     # Listen for new messages
#     async for event in client.events():
#         if event.type == "message.upserted":
#             message = event.data
#             print(
#                 f"NEW MESSAGE: {message.sender_name}: "
#                 f"{message.text}"
#             )

# if __name__ == "__main__":
#     asyncio.run(main())