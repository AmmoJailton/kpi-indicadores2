from typing import List

from artex_login_codes import ARTEX_LOGIN_CODES


class LoginArtexService:
    codes: List[str] = []
    
    def __init__(self):
        self.codes = ARTEX_LOGIN_CODES
        pass
    
    def login(self, code_or_email: str) -> bool:
        code_or_email = code_or_email.lower()
        code_or_email = code_or_email.replace(" ", "")
        
        codes = []
        for code in self.codes:
            codes.append(code.lower()) 
            
        return code_or_email in codes
    