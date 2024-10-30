from typing import Any, List
from commom.data_classes.login_data_class import ILoginArtexParams
from innovation_api.api.services.login_artex_service import LoginArtexService
from innovation_api.typing import IEndpoint, IEndpointConfig
from innovation_api import __version__

class LoginArtexController(IEndpoint):
    service : LoginArtexService
    
    @property
    def endpoints(self) -> List[IEndpointConfig]: 
        return [IEndpointConfig(route="/login-artex", class_method=self.login, rest_method="POST", tags=["LOGIN ARTEX"])]

    def __init__(self) -> None:
        self.service = LoginArtexService()
        pass

    def login(self, body: ILoginArtexParams) -> Any:
        if body.code_or_email == '':
            return {
                "result": "Error",
                "message": "code_or_email is required",
            }

        response = self.service.login(code_or_email=body.code_or_email)
        
        if response:
            return {
                "result": "Success",
                "message": response
            }
        else:
            return {
                "result": "Invalid code_or_email",
                "message": response
            }
            
        
