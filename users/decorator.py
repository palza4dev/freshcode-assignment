import jwt
import json

from django.http      import JsonResponse
from django.shortcuts import redirect
from django.conf      import settings
from users.models     import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):       
        if "Authorization" not in request.headers : 
            return JsonResponse ({"message" : "UNAUTHORIZED"}, status=401)

        encode_token = request.headers["Authorization"]

        try:
            data = jwt.decode(encode_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user = User.objects.get(id = data["id"])    
            request.user = user

        except jwt.exceptions.DecodeError :
            return JsonResponse({"massage":"JWT_MALFORMED"}, status=401)

        except User.DoesNotExist :
            return JsonResponse({"message":"UNKNOWN_USER"}, status=401)

        user = request.session.get('user')
        
        if user is None or not user:
            return  redirect('/login')

        return func(self, request, *args, **kwargs)

    return wrapper

def admin_decorator(func):
    def wrapper(self, request, *args, **kwargs):       
        if "Authorization" not in request.headers : 
            return JsonResponse ({"message" : "UNAUTHORIZED"}, status=401)

        encode_token = request.headers["Authorization"]

        try:
            data = jwt.decode(encode_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user = User.objects.get(id = data["id"])    
            request.user = user

        except jwt.exceptions.DecodeError :
            return JsonResponse({"massage":"JWT_MALFORMED"}, status=401)

        except User.DoesNotExist :
            return JsonResponse({"message":"UNKNOWN_USER"}, status=401)

        user = request.session.get('user')
        
        if user is None or not user:
            return  redirect('/login')

        user = User.objects.get(email=user)
        if user.role != 'admin':
            return redirect('/')

        return func(self, request, *args, **kwargs)


    return wrapper