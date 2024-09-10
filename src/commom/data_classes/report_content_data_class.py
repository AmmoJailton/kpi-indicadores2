from dataclasses import dataclass, field
from typing import Optional
import pandas as pd

@dataclass
class IPageContent:
  title: str
  content: pd.DataFrame

@dataclass
class IReportContentPage:
  page: str
  content: list[IPageContent]
  
@dataclass
class IReportContent:
  document_file_name: str
  document_content: list[IReportContentPage]