from dataclasses import dataclass
from typing import List, Optional, Union

import pandas as pd
from pydantic import BaseModel


@dataclass
class IPageContent:
    title: str
    content: Union[pd.DataFrame, str]


@dataclass
class IReportContentPage:
    page: str
    content: list[IPageContent]


@dataclass
class IReportContent:
    document_file_name: str
    document_content: list[IReportContentPage]


class DebugBody(BaseModel):
    debug_mode: Optional[bool] = True


class DailyReportBody(DebugBody):
    ids_loja: List[str]
    custom_recipients: Optional[List[str]] = []
