import json, bcrypt, jwt

from django.http        import JsonResponse
from django.views       import View
from json.decoder       import JSONDecodeError

from freshcode.settings import SECRET_KEY, ALGORITHM
from users.models       import User

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'INVALID_EMAIL'}, status = 401)

            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_PASSWORD'}, status = 401)

            access_token = jwt.encode({'id' : user.id}, SECRET_KEY, algorithm = ALGORITHM)

            return JsonResponse({'access_token':access_token}, status = 200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status = 400)

        except JSONDecodeError:
            return JsonResponse({'message' : 'JSON_DECODE_ERROR'}, status = 400)