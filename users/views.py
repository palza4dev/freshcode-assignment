import json
import re
import bcrypt
import jwt

from django.http                import JsonResponse
from django.views               import View
from json.decoder               import JSONDecodeError
from django.conf                import settings

from users.models           import User

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'USER_DOSE_NOT_EXIST'}, status = 404)

            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)
            
            token = jwt.encode({'id' : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)

            return JsonResponse({'token':token}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)