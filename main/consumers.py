import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from .models import *
from .serializers import *


class BookSocket(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'book'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.ReciveData(data)
        # await self.send(text_data=json.dumps(send_data))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'book',
                'message': data
            }
        )

    # Receive message from room group
    async def book(self, event):
        data = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))

    async def ReciveData(self, data):
        if data['type'] == "book0":
            data['data'] = await self.book0()
        elif data['type'] == "book1":
            data['data'] = await self.book1()
        elif data['type'] == "busy1":
            data['data'] = await self.busy1(data['id'])
        elif data['type'] == "busy0":
            data['data'] = await self.busy0(data['id'])

        return data

    @database_sync_to_async
    def book0(self):
        books = Books.objects.filter(status=False)
        dt = []
        for r in books:
            t = {
                'id': r.id,
                'author': r.author.name,
                'book': r.name,
            }
            dt.append(t)
        data = {
            'type': 'book0',
            'books': dt
        }
        return data

    @database_sync_to_async
    def book1(self):
        books = Books.objects.filter(status=1)
        dt = []
        for r in books:
            t = {
                'id': r.id,
                'name': r.name,
                'author': r.author.name,
            }
            dt.append(t)
        data = {
            'type': 'book1',
            'books': dt
        }
        return data

    @database_sync_to_async
    def busy1(self, id):
        book = Books.objects.get(id=id)
        book.status = 1
        book.save()

        books0 = Books.objects.filter(status=0)
        dt0 = []
        for r in books0:
            t = {
                'id': r.id,
                'name': r.name,
                'author': r.author.name,
            }
            dt0.append(t)

        books1 = Books.objects.filter(status=1)
        dt1 = []
        for r in books1:
            t = {
                'id': r.id,
                'name': r.name,
                'author': r.author.name,
            }
            dt1.append(t)
        data = {
            'type': 'book0and1',
            'books0': dt0,
            'books1': dt1
        }
        return data

    @database_sync_to_async
    def busy0(self, id):
        book = Books.objects.get(id=id)
        book.status = 0
        book.save()

        books0 = Books.objects.filter(status=0)
        dt0 = []
        for r in books0:
            t = {
                'id': r.id,
                'name': r.name,
                'author': r.author.name,
            }
            dt0.append(t)

        books1 = Books.objects.filter(status=1)
        dt1 = []
        for r in books1:
            t = {
                'id': r.id,
                'name': r.name,
                'author': r.author.name,
            }
            dt1.append(t)
        data = {
            'type': 'book0and1',
            'books0': dt0,
            'books1': dt1
        }
        return data


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        print(self.room_name)
        print(self.room_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.RecieveData(data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': send_data['data']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))

    async def RecieveData(self, data):
        if data['type'] == "chat1":
            data['data'] = await self.chat1(data)

        return data

    @database_sync_to_async
    def chat1(self, data):
        data = {
            'type': 'chat1',
            'message': data['message']
        }
        return data

#class ChatConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     self.room_name = self.scope['url_route']['kwargs']['room_name']
    #     self.room_group_name = 'chat_%s' % self.room_name
    #     print(self.room_name)
    #     print(self.room_group_name)
    #     # Join room group
    #     await self.channel_layer.group_add(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #
    #     await self.accept()
    #
    # async def disconnect(self, close_code):
    #     # Leave room group
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #
    # # Receive message from WebSocket
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #     print(message)
    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.channel_layer.group_send,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )
    #
    # # Receive message from room group
    # async def chat_message(self, event):
    #     message = event['message']
    #     print(message, 'chat_message')
    #
    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
#        }))