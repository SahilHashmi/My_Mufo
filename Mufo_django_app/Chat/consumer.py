# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat , Room , Visitor
# from User.models import User
# from bots import BotHandler
# from datetime import datetime

# from asgiref.sync import sync_to_async
# import json, html, pytz
    
# class ChatConsumer(AsyncWebsocketConsumer):
    
#     async def connect(self):
#         self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
#         self.group_room_code = f'chat_{self.room_code}'

#         self.sender_token = self.scope.get("query_string").decode('utf-8')
#         if '=' in self.sender_token:
#             self.sender_token = self.sender_token.split('=')[1]
#         else:
#             self.sender_token = None

#         self.room_model = await self.get_room_model()
#         self.bots = await self.active_bots()
#         self.bothandler = BotHandler(self.bots, self.group_room_code)

#         self.user = await self.get_user_from_token(self.sender_token)

#         if not self.user:
#             self.sender = "admin"
#         else:
#             self.sender = str(self.user)

#         await self.channel_layer.group_add(self.group_room_code, self.channel_name)

#         await self.channel_layer.group_send(
#             self.group_room_code,
#             {
#                 "type": "chat_message",
#                 "message": "Joined the room!",
#                 "sender": self.sender
#             }
#         )

#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_send(
#             self.group_room_code,
#             {
#                 "type": "chat.message",
#                 "message": "Leave the room",
#                 "sender": self.sender
#             }
#         )
#         await self.channel_layer.group_discard(self.group_room_code, self.channel_name)

#     async def receive(self, text_data=None, bytes_data=None):
#         json_data = json.loads(text_data)
#         message = json_data.get('message')

#         saved = await self.save_message(message)
#         if saved:
#             date_created = str(saved.created)
#         else:
#             date_created = str(datetime.now(tz=pytz.UTC))

#         await self.channel_layer.group_send(
#             self.group_room_code,
#             {
#                 "type": "chat.message",
#                 "message": message,
#                 "sender": self.sender,
#                 "date": date_created
#             }
#         )

#         bot = await self.bothandler.get_response(message)

#         if bot:
#             bot_object, response = bot
#             user = await self.get_bot_user(bot_object)
#             if response:
#                 saved = await self.save_message(response, user=user)
#             await self.channel_layer.group_send(
#                 self.group_room_code,
#                 {
#                     "type": "bot.response",
#                     "message": str(response),
#                     "sender": str(user),
#                     "date": str(saved.created)
#                 }
#             )

#     async def bot_response(self, text_data):
#         message = text_data.get("message")
#         sender = text_data.get("sender")
#         date = text_data.get('date')
#         await self.send(text_data=json.dumps({"message": message, "sender": sender, "date": date}))

#     async def chat_message(self, text_data):
#         is_blocked = await self.get_blocked()
#         if is_blocked:
#             return 0

#         message = html.escape(text_data.get("message"))
#         sender = text_data.get('sender')
#         date = text_data.get('date')

#         await self.send(text_data=json.dumps({"message": message, "sender": sender, 'date': date}))

#     @database_sync_to_async
#     def save_message(self, text: str, user=None):
#         if not user:
#             user = self.user
#         if user:
#             chat = Chat.objects.create(
#                 from_user=user,
#                 text=text
#             )

#             self.room_model.chat_set.add(chat)

#             return chat

#     @database_sync_to_async
#     def get_room_model(self):
#         return Room.objects.get(room_code=self.room_code)

#     @database_sync_to_async
#     def get_user_from_token(self, token):
#         try:
#             if not token:
#                 return None
#             return User.objects.get(token=token)
#         except User.DoesNotExist:
#             return None

#     @database_sync_to_async
#     def get_blocked(self):
#         if self.user and self.room_model:
#             query = self.room_model.blocked_users.filter(token=self.user.token)
#             return any(query)

#     @database_sync_to_async
#     def active_bots(self):
#         bots = [x for x in self.room_model.active_bots.all()]
#         return bots

#     @sync_to_async
#     def bot_handler(self):
#         return BotHandler(self.bots, self.group_room_code)

#     @database_sync_to_async
#     def get_bot_user(self, bot):
#         return bot.user


# class NotifConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add('notif_chat', self.channel_name)
    
#         await self.accept()
    
#     async def receive(self, text_data=None, bytes_data=None):
#         data_json = json.loads(text_data)
        
#         ip_addr = data_json.get('ip_address')
#         user_agent = data_json.get('user_agent')

#         if all([ip_addr, user_agent]):

#             await self.save_visitor(ip_addr=ip_addr, user_agent=user_agent)
        
#         total_visitor = await self.total_visitor()

#         await self.channel_layer.group_send(
#             'notif_chat',
#             {
#                 'type':'send.notif',
#                 'total_visitor':total_visitor
#             }
#         )
    
#     async def send_notif(self, text_data):

#         await self.send(text_data=json.dumps(text_data))
    
#     @database_sync_to_async
#     def total_visitor(self):
#         return Visitor.objects.all().count()
    
#     @database_sync_to_async
#     def save_visitor(self, ip_addr, user_agent):
#         if Visitor.objects.filter(ip_addr=ip_addr).first():
#             return None
#         v = Visitor(ip_addr=ip_addr, user_agent=user_agent)
#         v.save()
#         return v

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class TestConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = 'test_consumer'
#         self.room_group_name = 'test_consumer_group'
#         await self.channel_layer.group_add(
#             self.room_name, self.room_group_name
#         )
#         await self.accept()
#         await self.send(text_data=json.dumps({'status': 'connected'}))

#     async def receive(self, text_data=None, bytes_data=None):
#         print('received called')
#         await self.send(text_data=json.dumps({'status': 'connectedcascs'}))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_name, self.room_group_name
#         )

# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Chat , Room , Visitor
# from User.models import User
# from bots import BotHandler
# from datetime import datetime

# from asgiref.sync import sync_to_async
# import json, html, pytz
    
# class ChatConsumer(AsyncWebsocketConsumer):
    
#     async def connect(self):
#         self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
#         self.group_room_code = f'chat_{self.room_code}'

#         self.sender_token = self.scope.get("query_string").decode('utf-8')
#         if '=' in self.sender_token:
#             self.sender_token = self.sender_token.split('=')[1]
#         else:
#             self.sender_token = None

#         self.room_model = await self.get_room_model()
#         self.bots = await self.active_bots()
#         self.bothandler = BotHandler(self.bots, self.group_room_code)

#         self.user = await self.get_user_from_token(self.sender_token)

#         if not self.user:
#             self.sender = "admin"
#             self.sender_profile_picture = ""
#         else:
#             self.sender = str(self.user)
#             self.sender_profile_picture = str(self.user.profile_picture)

#         await self.channel_layer.group_add(self.group_room_code, self.channel_name)

#         await self.channel_layer.group_send(
#             self.group_room_code,
#             {
#                 "type": "chat_message",
#                 "message": "Joined the room!",
#                 "sender": self.sender,
#                 "sender_profile_picture": self.sender_profile_picture
#             }
#         )

#         await self.accept()

#     async def disconnect(self, code):
#         await self.channel_layer.group_send(
#             self.group_room_code,
#             {
#                 "type": "chat.message",
#                 "message": "Leave the room",
#                 "sender": self.sender,
#                 "sender_profile_picture": self.sender_profile_picture
#             }
#         )
#         await self.channel_layer.group_discard(self.group_room_code, self.channel_name)


#     async def receive(self, text_data=None, bytes_data=None):
#         json_data = json.loads(text_data)

#         message = json_data.get('message')

#         saved = await self.save_message(message)
#         if saved:
#             date_created = str(saved.created)
#         else:
#             date_created = str(datetime.now(tz=pytz.UTC))

#         sender_profile_picture = ""

#         if self.user:
#             sender_profile_picture = str(self.user.profile_picture)

#         await self.channel_layer.group_send(
#             self.group_room_code,
#             {
#                 "type": "chat.message",
#                 "message": message,
#                 "sender": self.sender,
#                 "date": date_created,
#                 "sender_profile_picture": sender_profile_picture     
#             }
#         )

    
#         bot = await self.bothandler.get_response(message)

#         if bot:
#             bot_object, response = bot
#             user = await self.get_bot_user(bot_object)
#             if response:
#                 saved = await self.save_message(response, user=user)
                
#             await self.channel_layer.group_send(
#                 self.group_room_code,
#                 {
#                     "type": "bot.response",
#                     "message": str(response),
#                     "sender": str(user),
#                     "date": str(saved.created),
#                 }
#             )

#     async def bot_response(self, text_data):
#         message = text_data.get("message")
#         sender = text_data.get("sender")
#         date = text_data.get('date')
#         await self.send(text_data=json.dumps({"message": message, "sender": sender, "date": date}))

#     async def chat_message(self, text_data):
#         is_blocked = await self.get_blocked()
#         if is_blocked:
#             return 0

#         message = html.escape(text_data.get("message"))
#         sender = text_data.get('sender')
#         date = text_data.get('date')
#         sender_profile_picture = text_data.get('sender_profile_picture')
#         await self.send(text_data=json.dumps({"message": message, "sender": sender,"profile_picture": sender_profile_picture,'date': date}))

#     @database_sync_to_async
#     def save_message(self, text: str, user=None):
#         if not user:
#             user = self.user
#         if user:
#             chat = Chat.objects.create(
#                 from_user=user,
#                 text=text
#             )

#             self.room_model.chat_set.add(chat)

#             return chat

#     @database_sync_to_async
#     def get_room_model(self):
#         return Room.objects.get(room_code=self.room_code)

#     @database_sync_to_async
#     def get_user_from_token(self, token):
#         try:
#             if not token:
#                 return None
#             return User.objects.get(token=token)
#         except User.DoesNotExist:
#             return None

#     @database_sync_to_async
#     def get_blocked(self):
#         if self.user and self.room_model:
#             query = self.room_model.blocked_users.filter(token=self.user.token)
#             return any(query)

#     @database_sync_to_async
#     def active_bots(self):
#         bots = [x for x in self.room_model.active_bots.all()]
#         return bots

#     @sync_to_async
#     def bot_handler(self):
#         return BotHandler(self.bots, self.group_room_code)

#     @database_sync_to_async
#     def get_bot_user(self, bot):
#         return bot.user


# class NotifConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add('notif_chat', self.channel_name)
    
#         await self.accept()
    
#     async def receive(self, text_data=None, bytes_data=None):
#         data_json = json.loads(text_data)
        
#         ip_addr = data_json.get('ip_address')
#         user_agent = data_json.get('user_agent')

#         if all([ip_addr, user_agent]):

#             await self.save_visitor(ip_addr=ip_addr, user_agent=user_agent)
        
#         total_visitor = await self.total_visitor()

#         await self.channel_layer.group_send(
#             'notif_chat',
#             {
#                 'type':'send.notif',
#                 'total_visitor':total_visitor
#             }
#         )
    
#     async def send_notif(self, text_data):

#         await self.send(text_data=json.dumps(text_data))
    
#     @database_sync_to_async
#     def total_visitor(self):
#         return Visitor.objects.all().count()
    
#     @database_sync_to_async
#     def save_visitor(self, ip_addr, user_agent):
#         if Visitor.objects.filter(ip_addr=ip_addr).first():
#             return None
#         v = Visitor(ip_addr=ip_addr, user_agent=user_agent)
#         v.save()
#         return v

# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class TestConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = 'test_consumer'
#         self.room_group_name = 'test_consumer_group'
#         await self.channel_layer.group_add(
#             self.room_name, self.room_group_name
#         )
#         await self.accept()
#         await self.send(text_data=json.dumps({'status': 'connected'}))

#     async def receive(self, text_data=None, bytes_data=None):
#         print('received called')
#         await self.send(text_data=json.dumps({'status': 'connectedcascs'}))

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_name, self.room_group_name
#         )

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat , Room , Visitor
from User.models import User
from bots import BotHandler
from datetime import datetime

from asgiref.sync import sync_to_async
import json, html, pytz

class ChatConsumer(AsyncWebsocketConsumer):
    joined_room = {}    
    async def connect(self):
        self.room_code = self.scope["url_route"]["kwargs"]["room_code"]
        self.group_room_code = f'chat_{self.room_code}'

        self.sender_token = self.scope.get("query_string").decode('utf-8')
        if '=' in self.sender_token:
            self.sender_token = self.sender_token.split('=')[1]
        else:
            self.sender_token = None

        self.room_model = await self.get_room_model()
        self.bots = await self.active_bots()
        self.bothandler = BotHandler(self.bots, self.group_room_code)

        self.user = await self.get_user_from_token(self.sender_token)
        if not self.user:
            self.sender = "admin"
            self.sender_profile_picture = ""
        else:
            self.sender = str(self.user)
            self.sender_profile_picture = str(self.user.profile_picture)
       
        await self.channel_layer.group_add(self.group_room_code, self.channel_name)

        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat_message",
                "message": "Joined the room!",
                "sender": self.sender,
                "sender_profile_picture": self.sender_profile_picture
            }
        )
 
        if self.sender_profile_picture:
            ChatConsumer.joined_room[self.sender] = self.sender_profile_picture

        await self.accept()

    async def disconnect(self, code):
        if self.sender in self.joined_room:
            del ChatConsumer.joined_room[self.sender]
        
        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat.message",
                "message": "Leave the room",
                "sender": self.sender,
                "sender_profile_picture": self.sender_profile_picture,
            }
        )
        await self.channel_layer.group_discard(self.group_room_code, self.channel_name)



    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)

        message = json_data.get('message')

        saved = await self.save_message(message)
        if saved:
            date_created = str(saved.created)
        else:
            date_created = str(datetime.now(tz=pytz.UTC))

        sender_profile_picture = str(self.user.profile_picture) if self.user else ""

        await self.channel_layer.group_send(
            self.group_room_code,
            {
                "type": "chat.message",
                "message": message,
                "sender": self.sender,
                "date": date_created,
                "sender_profile_picture": sender_profile_picture
                    
            }
        )

    
        bot = await self.bothandler.get_response(message)

        if bot:
            bot_object, response = bot
            user = await self.get_bot_user(bot_object)
            if response:
                saved = await self.save_message(response, user=user)
                
            await self.channel_layer.group_send(
                self.group_room_code,
                {
                    "type": "bot.response",
                    "message": str(response),
                    "sender": str(user),
                    "date": str(saved.created),
                }
            )

    async def bot_response(self, text_data):
        message = text_data.get("message")
        sender = text_data.get("sender")
        date = text_data.get('date')
        await self.send(text_data=json.dumps({"message": message, "sender": sender, "date": date}))

    async def chat_message(self, text_data):
        is_blocked = await self.get_blocked()
        if is_blocked:
            return 0

        message = html.escape(text_data.get("message"))
        sender = text_data.get('sender')
        date = text_data.get('date')
        sender_profile_picture = text_data.get('sender_profile_picture')
        joined_room_profile_pictures = list(ChatConsumer.joined_room.values())
        await self.send(text_data=json.dumps({"message": message, "sender": sender,"profile_picture": sender_profile_picture,'date': date,"filtered_joined_room":joined_room_profile_pictures}))

    @database_sync_to_async
    def save_message(self, text: str, user=None):
        if not user:
            user = self.user
        if user:
            chat = Chat.objects.create(
                from_user=user,
                text=text
            )

            self.room_model.chat_set.add(chat)

            return chat

    @database_sync_to_async
    def get_room_model(self):
        return Room.objects.get(room_code=self.room_code)

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            if not token:
                return None
            return User.objects.get(token=token)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_blocked(self):
        if self.user and self.room_model:
            query = self.room_model.blocked_users.filter(token=self.user.token)
            return any(query)

    @database_sync_to_async
    def active_bots(self):
        bots = [x for x in self.room_model.active_bots.all()]
        return bots

    @sync_to_async
    def bot_handler(self):
        return BotHandler(self.bots, self.group_room_code)

    @database_sync_to_async
    def get_bot_user(self, bot):
        return bot.user

class NotifConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('notif_chat', self.channel_name)
    
        await self.accept()
    
    async def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        
        ip_addr = data_json.get('ip_address')
        user_agent = data_json.get('user_agent')

        if all([ip_addr, user_agent]):

            await self.save_visitor(ip_addr=ip_addr, user_agent=user_agent)
        
        total_visitor = await self.total_visitor()

        await self.channel_layer.group_send(
            'notif_chat',
            {
                'type':'send.notif',
                'total_visitor':total_visitor
            }
        )
    
    async def send_notif(self, text_data):

        await self.send(text_data=json.dumps(text_data))
    
    @database_sync_to_async
    def total_visitor(self):
        return Visitor.objects.all().count()
    
    @database_sync_to_async
    def save_visitor(self, ip_addr, user_agent):
        if Visitor.objects.filter(ip_addr=ip_addr).first():
            return None
        v = Visitor(ip_addr=ip_addr, user_agent=user_agent)
        v.save()
        return v

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'test_consumer'
        self.room_group_name = 'test_consumer_group'
        await self.channel_layer.group_add(
            self.room_name, self.room_group_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'status': 'connected'}))

    async def receive(self, text_data=None, bytes_data=None):
        print('received called')
        await self.send(text_data=json.dumps({'status': 'connectedcascs'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name, self.room_group_name
        )
