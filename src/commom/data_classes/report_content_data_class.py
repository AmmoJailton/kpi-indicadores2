from dataclasses import dataclass
from typing import List, Union

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


class DailyReportBody(BaseModel):
    ids_loja: List[str]
