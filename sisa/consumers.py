import json
from channels.generic.websocket import AsyncWebsocketConsumer

class PrintConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print_job = text_data_json.get('print_job', '')

        # Aquí puedes enviar el trabajo de impresión al cliente
        await self.send(text_data=json.dumps({
            'print_job': print_job
        }))
