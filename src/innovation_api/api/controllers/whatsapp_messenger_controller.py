from typing import Any, Dict, List

from fastapi import HTTPException
from commom.data_classes.whatsapp_message_data_class import IWhatsappBody
from innovation_api.api.services.whatsapp_service import WhatsappService
from innovation_api.typing import IEndpoint, IEndpointConfig


class WhatsappController(IEndpoint):
    TAGS = ["WHATSAPP"]
    whatsapp_service : WhatsappService
    
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [
            IEndpointConfig(
                route="/send-message", class_method=self.send_message, rest_method="POST", tags=self.TAGS
            ),
        ]

    def __init__(self) -> None:
        self.whatsapp_service = WhatsappService()
        pass

    def send_message(self, body: IWhatsappBody):
        return {
            'status': 'em fase de testes'
        }
        if body.phone == '':
            raise HTTPException(status_code=400, detail='Invalid phone number')
        elif len(body.phone) < 13:
            raise HTTPException(status_code=400, detail='Invalid phone number')
        
        message = body.message.model_dump()
        empty_message = True
        
        for k in message.values():
            if k is not None:
                empty_message = False
        
        if empty_message:
            raise HTTPException(status_code=400, detail='Invalid message')
        
        
        return self.whatsapp_service.send_whatsapp_message(phone=body.phone, message=body.message)
    