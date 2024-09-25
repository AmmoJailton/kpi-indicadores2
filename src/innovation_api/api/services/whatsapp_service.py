import os
from typing import Any, Dict, List, Optional
import requests as req
import json

from commom.data_classes.whatsapp_message_data_class import IWhatsappMessage

class WhatsappService():
    def __init__(self) -> None:
        pass
    
    def send_whatsapp_message(self, phone: str, message: IWhatsappMessage):
        token = self._get_token()
        botmaker_url = self._get_url()
        channel_id = self._get_channel_id()
        
        if token is None:
            return {
                'ERROR': 'INVALID ACCESS TOKEN',
                'Status': 'Message not sent'
            }
        elif botmaker_url is None:
            return {
                'ERROR': 'INVALID URL',
                'Status': 'Message not sent'
            }
        elif channel_id is None:
            return {
                'ERROR': 'INVALID CHANNEL',
                'Status': 'Message not sent'
            }

        headers = self._format_headers(token)
        data = self._format_message(channel_id=channel_id,phone= phone, message= message)
        
        response = self._send_message(url = botmaker_url, data = data, headers=headers)
        return response.json()

    @staticmethod
    def _send_message(url: str, data:Dict[str, str], headers:Dict[str, str]) -> req.Response:
        response = req.post(url, data=json.dumps(data), headers=headers)
        return response
  
    @staticmethod
    def _format_message(channel_id:str, phone:str, message:IWhatsappMessage) -> Dict[str, str]:
        message_dict = message.model_dump()

        return {
            'chat': { 
                'channelId': channel_id, 
                'contactId':  phone 
            },
            'messages': [
                message_dict
            ]
            
        }
    
    @staticmethod
    def _format_headers(token:str) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'access-token': token,
        }
        
    @staticmethod
    def _get_token() -> Optional[str]:
        token = os.getenv('BOTMAKER_ACCESS_TOKEN')
        return token

    @staticmethod
    def _get_url() -> Optional[str]:
        url = os.getenv('BOTMAKER_URL')
        return url
    
    @staticmethod
    def _get_channel_id() -> str:
        channel_id = os.getenv('BOTMAKER_CHANNEL_ID')
        return channel_id