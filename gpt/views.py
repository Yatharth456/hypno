import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from config import Config
from rest_framework.permissions import IsAuthenticated



class OpenAIChatView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        # Get the model and message from the request data
        message = request.data.get('message')
        if not message:
            return Response({'message': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Make the request to the OpenAI API
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {Config.GPT_API_KEY}',
        }
        data = {
            'model': "gpt-3.5-turbo",
            'messages': [{'role': 'user', 'content': message}]
        }
        response = requests.post(Config.GPT_CHAT_URL, headers=headers, json=data)

        # Return the response from the OpenAI API to the client
        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to retrieve response from OpenAI API.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
