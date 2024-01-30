from django.contrib.auth.models import User, AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from knox.models import AuthToken as Token
from urllib.parse import parse_qs
from channels.db import database_sync_to_async

class TokenAuthentication :

    model = None

    def get_model(self) :
        if self.model is not None :
            return self.model
        return Token
    
    def authenticate(self,token) :
        model = self.get_model()

        try :
            key = token[:8]
            token = model.objects.select_related("user").get(token_key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed(_("Invalid token."))
        
        if not token.user.is_active :
            raise AuthenticationFailed(_("Use is Inactive"))
        
        return token.user
    
@database_sync_to_async
def get_user(scope) :   
    if "token" not in scope :
        raise ValueError("Cannot find token in scope")
    
    token = scope["token"]
    user = None

    try :
        auth = TokenAuthentication()
        user = auth.authenticate(token)
    except AuthenticationFailed :
        pass
    return user or AnonymousUser




class TokenAuthMiddleware:
    """
    Custom middleware that takes a token from the query string and authenticates via Django Rest Framework authtoken.
    """
 
    def __init__(self, app):
        # Store the ASGI application we were passed
        self.app = app
 
    async def __call__(self, scope, receive, send):
        # Look up user from query string (you should also do things like
        # checking if it is a valid user ID, or if scope["user"] is already
        # populated).
        query_params = parse_qs(scope["query_string"].decode())
        token = query_params["token"][0]
        scope["token"] = token
        scope["user"] = await get_user(scope)
        return await self.app(scope, receive, send)   

        

      

      



