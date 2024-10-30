from dataclasses import dataclass
import dataclasses
from typing import List, Literal, Optional, Union
import datetime
import pandas as pd
from pydantic import BaseModel

class ILoginArtexParams(BaseModel):
    code_or_email: str
    password: Optional[str] = None