

import json
from uuid import uuid4, UUID
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine, text, select, DateTime, create_engine, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

from sqlalchemy.ext.mutable import MutableDict



class Base(DeclarativeBase):
    pass

engine = create_engine("sqlite:///learning.db")


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)


class Chats(Base):
    __tablename__ = "chats"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    modified_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    
class Messages(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    content: Mapped[dict] = mapped_column(
    MutableDict.as_mutable(JSON),
    nullable=False
)
    def setRole(self, role):
        self.content["role"] = role

    def setContent(self, content):
        self.content["content"] = content
    
# required!
Base.metadata.create_all(engine)

        # for i, user in enumerate(users):

print("Starting sim.... \n\n")

login = True
test = False
chatting = False

while login:
    with Session(engine) as session:
        query = select(User)
        users = session.scalars(query).all()

        usernames = []
        i = 0
        print("Available Users: .... \n\n\n")
    
        for user in users:
            i = i + 1
            print(f"User: {user.name}; id: {user.id}")
            usernames.append(user.name)
        
        if i == 0:
            print("No users\n\n")

        user = input("select or input a user: \n\n")
        if user in usernames:
            print("Logged in as: " + user)
            query = select(User).where(User.name == user)
            userid = session.scalars(query).all()[0].id
            print(userid)
            test = True
            login = False
        else:
            answer = input("No user by that name, would you like to create a new user? y/n: ")
            if answer == "y":
                new_user = User(name=user)
                session.add(new_user)
                session.commit()


while test:
    print("\n\n\n\n")
    print("---------------------------------------------------------------------------------------------")  
    print("\n\nAvailable chats\n\n")
    print("---------------------------------------------------------------------------------------------")

    with Session(engine) as session:
    
   

        chatQuery = select(Chats).where(Chats.user == userid).order_by(Chats.created_at.asc())
        results = session.scalars(chatQuery).all()

        chatCount = 0
        chat_ids = []
        for chat in results:
            chatCount = chatCount + 1
            chat_ids.append(chat.id)
            print(f"{chatCount}:   {chat.name}                {chat.created_at} | {chat.id}")
        print("---------------------------------------------------------------------------------------------")

        if chatCount == 0:
            print("No chats")
            answer = input("Would you like to create one y/n: ")
            if answer == "y":
                userChoice = input("Type in name of chat: ")
                new_chat = Chats(name=userChoice, user=userid)
                session.add(new_chat)
                session.commit()
            else:
                break

        chatSelection = input("Please select a chat you would like to enter or type \"new\" to get a new chat: ")
        
        if chatSelection == "new":
            userChoice = input("Type in name of chat: ")
            new_chat = Chats(name=userChoice, user=userid)
            session.add(new_chat)
            session.commit()
            print("\n\n\n\n")
            print("---------------------------------------------------------------------------------------------")  
            print("\n\nAvailable chats\n\n")
            print("---------------------------------------------------------------------------------------------")

            chatQuery = select(Chats).where(Chats.user == userid).order_by(Chats.created_at.asc())
            results = session.scalars(chatQuery).all()

            chatCount = 0
            
            for chat in results:
                chatCount = chatCount + 1
                chat_ids.append(chat.id)
                print(f"{chatCount}:   {chat.name}                {chat.created_at} | {chat.id}")
            print("---------------------------------------------------------------------------------------------")

        else:
            # try: 
            chatSelection = int(chatSelection)
            print(chatSelection)
            if (chatSelection <= chatCount) and chatSelection != 0:
                user_choice_chat_id = chat_ids[chatSelection-1]
                chatting = True
                break

            # except Exception as e:
            #     print("invalid!")
            #     break

while chatting:
    with Session(engine) as session:
        query = select(Chats).where(Chats.id == user_choice_chat_id)
        chat_name = session.scalars(query).all()
        print("\n\n\n\n")
        print("---------------------------------------------------------------------------------------------")  
        print(f"\n\nAvailable Messages for chat: {chat_name[0].name}\n\n")
        print("---------------------------------------------------------------------------------------------")


        chatQuery = select(Messages).where(Messages.chat_id == user_choice_chat_id).order_by(Messages.created_at.asc())
        result = session.scalars(chatQuery).all()

        message_count = 0
        print("Type message: ...  type /bye to exit, /clear to clear")

        for message in result:
            message_count += 1
            print(f"{message.content["role"]}:  {message.content["content"]}")

        if message_count == 0:
            print("No messages .....")

        while True:
            newMessage = input("")


            match newMessage:
                case "/bye":
                    chatting = False
                    break

                case "/clear":
                    chatQuery = select(Messages).where(Messages.chat_id == user_choice_chat_id).order_by(Messages.created_at.asc())
                    result = session.scalars(chatQuery).all()
                    for message in result:
                        session.delete(message)
                        session.commit()
                    print("messages deleted..... \n\n\n")
                        

                case _:
                    session.add(Messages(chat_id=user_choice_chat_id, content=
                                            {"role": "user", "content": newMessage}
                                        ))
                    session.commit()
                    print(f"user:  {newMessage}")
                

                

               
                
           



#Passwords!
# from pwdlib import PasswordHash  password_hash = PasswordHash.recommended()  hashed = password_hash.hash("my_password")



# password_hash.verify("my_password", hashed)