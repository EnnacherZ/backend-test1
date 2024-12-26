import asyncio
import json
from channels.generic.http import AsyncHttpConsumer
from django.utils.encoding import smart_str
from django.http import HttpResponse
from django.db import models
from .models import Shoe
from .serializers import ShoeSerializer
from channels.db import database_sync_to_async

class SSEConsumer(AsyncHttpConsumer):

    async def handle(self, body):
        # Crée une réponse HTTP avec les bons en-têtes pour SSE
        response = HttpResponse(content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        response['Connection'] = 'keep-alive'
        
        # Autoriser CORS (si nécessaire)
        origin = self.scope.get('headers', {}).get('origin')
        ALLOWED_ORIGINS = ['192.168.1.9:3000']  # Changez selon vos besoins
        if origin in ALLOWED_ORIGINS:
            response['Access-Control-Allow-Origin'] = origin

        # Envoi des en-têtes
        await self.send_headers(response)

        # Boucle pour envoyer des événements SSE toutes les 2 secondes
        while True:
            # Récupérer les chaussures depuis la base de données
            shoes = await database_sync_to_async(Shoe.objects.all)()
            serializer = ShoeSerializer(shoes, many=True)
            data = json.dumps({'list_shoes': serializer.data})

            # Convertir les données en format SSE
            message = f"data: {smart_str(data)}\n\n"
            
            # Envoyer les données
            await self.send_body(message.encode('utf-8'))
            
            # Attendre 2 secondes avant d'envoyer le prochain message
            await asyncio.sleep(2)

    async def send_headers(self, response):
        """Envoie les en-têtes HTTP nécessaires pour les SSE"""
        await self.send({
            "type": "http.response.headers",
            "headers": [
                [b"Content-Type", b"text/event-stream"],
                [b"Cache-Control", b"no-cache"],
                [b"Connection", b"keep-alive"],
            ],
        })
    
    async def send_body(self, body):
        """Envoie les données SSE au client"""
        await self.send({
            "type": "http.response.body",
            "body": body,
            "more_body": True,
        })
