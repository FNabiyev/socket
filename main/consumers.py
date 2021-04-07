import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import *
from .serializers import *


class BookSocket(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'book'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.ReciveData(data)
        await self.send(text_data=json.dumps(send_data))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'add_b',
                'message': data
            }
        )

    async def add_b(self, event):
        data = event['message']
        await self.send(text_data=json.dumps(data))

    async def ReciveData(self, data):
        if data['type'] == "status1":
            data['data'] = await self.status1()
        elif data['type'] == "add_book":
            data['data'] = await self.add_book(data['data'])
        elif data['type'] == "buyurtma":
            data['data'] = await self.buyurtma(data)
        elif data['type'] == "status0":
            print("status111")
            data['data'] = await self.status0()

        return data

    @database_sync_to_async
    def add_book(self, data):
        b = Books.objects.create(name=data['book'], author_id=data['author'])
        data = {
            'type': 'add_book',
            'id': b.id,
            'book': data['book'],
            'author': Authors.objects.get(id=data['author']).name,
        }

        return data

    @database_sync_to_async
    def status1(self):
        books = Books.objects.filter(status=True).order_by('-id')
        dt = []
        for b in books:
            t = {
                'id': b.id,
                'book': b.name,
                'author': b.author.name,
            }
            dt.append(t)
        data = {
            'type': 'status1',
            'books': dt
        }
        return data

    @database_sync_to_async
    def buyurtma(self, data):
        b = Bookings.objects.create(book_id=data['id'], user_id=data['user'])
        dt = {
            'type':'buyurtma',
            'message':'{} nomli kitob {} tomonidan band qilindi!'.format(b.book.name, b.user.username)
        }

        return dt

    @database_sync_to_async
    def status0(self):
        print('asdsa')
        books = Books.objects.filter(status=False).order_by('-id')
        dt = []
        for b in books:
            t = {
                'id': b.id,
                'book': b.name,
                'author': b.author.name,
            }
            dt.append(t)
        data = {
            'type': 'status0',
            'books': dt
        }
        return data

class ChattingSocket(AsyncWebsocketConsumer):

    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chatting'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.ReciveData(data)
        await self.send(text_data=json.dumps(send_data))

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat',
                'message': data
            }
        )
    async def chat(self, event):
        data = event['message']
        await self.send(text_data=json.dumps(data))

    async def ReciveData(self, data):
        if data['type'] == "add_chat":
            data['data'] = await self.add_chat(data)

    @database_sync_to_async
    def add_chat(self, data):
        b = Chattings.objects.create(user_id=data['user'], message=data['msg'])
        dt = {
            'type': 'add_chat',
            'user': b.user.username,
            'msg': b.message
        }

        return dt

class BookingSocket(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'booking'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # await self.send(text_data=json.dumps(data))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'sendAll',
                'message': data
            }
        )

    async def sendAll(self, event):
        data = event['message']
        await self.send(text_data=json.dumps(data))


class ChatingSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        send_data = await self.ReciveData(data)
        # print(send_data)
        # await self.send(text_data=json.dumps(data))

    async def ReciveData(self, data):
        if data['type'] == "chatting":
            data['data'] = await self.chatting()

    @database_sync_to_async
    def chatting(self, data):
        Chattings.objects.create(author_id=data['author'], user_id=data['user'], text=data['message'])

        return {}
