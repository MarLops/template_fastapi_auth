import logging
import datetime
from fastapi import Request
from starlette.middleware.base import StreamingResponse
from .interface import MiddlewareBase
from starlette.datastructures import Headers, MutableHeaders


logger = logging.getLogger("middware")
logger.setLevel(logging.INFO)
handler = logging.FileHandler('middware.log')      
logger.addHandler(handler)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))


class MiddwareSimple(MiddlewareBase):
    async def middleware_before(self,request: Request):
        {% if cookiecutter.add_midware_time_in_logger == 'True'%}
        await self.check_time("Start Request")
        {% endif %}
        {% if cookiecutter.add_midware_header_in_looger == 'True'%}
        await self.check_header(request)
        {% endif %}
        return request
    
    async def middleware_after(self,response: StreamingResponse):
        {% if cookiecutter.add_midware_time_in_logger == 'True'%}
        await self.check_time("Finish Request")
        {% endif %}
        return response
    
    {% if cookiecutter.add_midware_time_in_logger == 'True'%}
    async def check_header(self,request: Request):
        header =  MutableHeaders(scope=request.scope)
        logger.info(f'Check Header - {str(header.items)}')
    {% endif %}   

    {% if cookiecutter.add_midware_time_in_logger == 'True'%}
    async def check_time(self, message):
        logger.info(f'{message} - {datetime.datetime.now()}')
    {% endif %}
    
        