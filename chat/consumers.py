import json
from django.contrib import messages
from .models import ChatRoom, Message
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       self.room_name = self.scope['url_route']['kwargs']['room_name']
       self.room_group_name = 'chat_%s' % self.room_name

       #join room group
       await self.channel_layer.group_add(
           self.room_group_name,
           self.channel_name
       )
       await self.accept()

    async def disconnect(self, close_code):
        #leave room grooup
       self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    def custom_for(self):
        msgSeen = Message.objects.filter(seen=False).exclude(user=self.scope['user'])
        print("ovo je msgSeen ", msgSeen)
        for i in msgSeen:
            i.seen = True
            i.save()

    #recive message form websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)  
        message = text_data_json['message']
        message_seen = text_data_json['message_seen']
        print("ovo je message_seen ", message_seen)
        #passin user iz self.scope
        self.user_id = self.scope['user'].id
        room = await database_sync_to_async(ChatRoom.objects.get)(name=self.room_name)
        #create new message object
        if message:
            chat = Message(
                content=message,
                user=self.scope['user'],
                room=room
            )
            if message_seen == True:
                await database_sync_to_async(self.custom_for)()
                

            await database_sync_to_async(chat.save)()
            #send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type':'chat_message',
                    'message': message,
                    'message_id':chat.id, #ovo je izvuceni message id 
                    'message_seen':chat.seen,
                    'user_id': self.user_id
                }
            )
    #receive message from room group
    async def chat_message(self, event):
        print("ovo je event: ", event)
        message = event['message']
        message_seen = event['message_seen']
        user_id = event['user_id']
        message_id = event['message_id']
        

        #send message to websocket
        await self.send(text_data=json.dumps({
            'message': message,
            'message_seen':message_seen,
            'user_id': user_id,
            'message_id': message_id
        }))