from fastapi import Request
from starlette.middleware.base import StreamingResponse
from .middware import MiddwareSimple
from .interface import MiddlewareBase


class Middware_Personalite(MiddwareSimple):
    def __init__(self):
        ...

    async def middleware_before(self,request: Request):
        return request
    
    async def middleware_after(self,response: StreamingResponse):
        return response



def create_middware(config):
    return MiddwareSimple()