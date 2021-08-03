from datetime import datetime

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def index(request):
    date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    message = 'Server live current time is: '

    return Response(data=message + date, status=status.HTTP_200_OK)
