from django.contrib.auth.models import User, AnonymousUser
from channels.middleware import BaseMiddleware
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from urllib.parse import parse_qs
from channels.db import database_sync_to_async


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self,scope,receive,send) :
        query_string = scope.get("query_string").decode()
        token = query_string.split("toke=")[1] if "token=" in query_string else None

        if token :
            # I will authenticate the user using knox TokenAuthentication
            user = await self.authenticate_user(token)

            if user :
                # if authentication is successful, add the user to the scope

                scope["user"] = user

        return await super().__call__(scope, receive, send)
    
    @database_sync_to_async

    def authenticate_user(self,token) :
        try :
            user, _ = TokenAuthentication().authenticate_credentials(token)
        
        except AuthenticationFailed :
            return None
        
        return user or AnonymousUser     

        

      

      



