
from commom.base_classes.base_generator import BaseGenerator
from commom.data.data_formater import KpiDataFormater
from commom.data_classes.report_content_data_class import IPageContent, IReportContent, IReportContentPage
from commom.data_classes.store_info_data_class import StoreInfo
from commom.pdf_creator import PDFGenerator
import pandas as pd
import datetime
from typing import Callable, List, Dict, Optional

import unidecode

class ReportGenerator(BaseGenerator):
    def __init__(self):
        pass

    @classmethod
    def generate_report(cls, report_type: str, **kwargs) -> any:
        report_types: Dict[str, Callable] = {
            'kpi': PDFGenerator.from_dataframe
        }
        
        return report_types[report_type](**kwargs)
    
    @classmethod
    def format_report_content(cls, report_type: str , **kwargs) -> IReportContent:
        report_types: Dict[str, Callable] = {
            'kpi': cls._format_kpi_data_to_report_content,
        }

        return report_types[report_type](**kwargs)
        
    @classmethod
    def get_recipients_for_report(cls, report_type: str, **kwargs) -> List[str]:
        report_types: Dict[str, Callable] = {
            'kpi': cls._get_email_sender_list,
        }
        
        return report_types[report_type](**kwargs)

    @classmethod
    def _format_kpi_data_to_report_content(
        cls,
        df_kpis_loja: pd.DataFrame,
        df_kpis_vendedor: pd.DataFrame, 
        df_nome_vendedor: pd.DataFrame,
        store: StoreInfo,
        yesterday_date: str,
        **kwargs
    ) -> IReportContent:
        
        df_store_formated,df_vendedor_formated_month,df_vendedor_formated_day = KpiDataFormater.format_all_tables(
            id_loja=store.loja_id,
            df_kpis_loja= df_kpis_loja,
            df_kpis_vendedor= df_kpis_vendedor,
            df_nome_vendedor= df_nome_vendedor
        )
        
        if df_store_formated.size > 0:
            filename:str = 'relatorio_' + store.marca_loja.replace(' ', '_') + '-' + store.nome_loja.replace(' ', '_') + '_' + yesterday_date
            filename = unidecode.unidecode(filename)

            formated_content = IReportContent(
                document_file_name=f'{filename}.pdf',
                document_content=[
                    IReportContentPage(
                        page='1',
                        content=[
                            IPageContent(
                                title=f'KPIs Loja {store.marca_loja} - {store.nome_loja} - {yesterday_date}',
                                content=df_store_formated
                            )
                        ]
                    ),
                    IReportContentPage(
                        page='2',
                        content=[
                            IPageContent(
                                title='KPI Vendedor Mês',
                                content=df_vendedor_formated_month
                            ),
                            IPageContent(
                                title=f'KPIs Vendedor Dia {yesterday_date}',
                                content=df_vendedor_formated_day
                            )
                        ]
                    )
                ]
            )
            
            return formated_content
        else:
            formated_content: IReportContent = {
                'document_file_name': f'vazio.pdf',
                'document_content': [
                    # IReportContentPage
                    {
                        'page': '1',
                        'content': [
                            # IPageContent
                            {
                                'title': 'vazio',
                                'content': ''
                            }
                        ]
                    },
                ]
            }
            
            
            return formated_content

    @classmethod
    def _get_email_sender_list(
        cls, 
        store: StoreInfo,
        test_email: Optional[str] = None,
        **kwargs
    ) -> List[str]:
        # ------
        # Voltar as linhas comentadas abaixo
        # ------
        
        # if test_email:
        #     return [test_email]
        
        # email_vinicius = 'vinicius.voltolini@ammovarejo.com.br'
        # return [store.email, store.email_regional, email_vinicius]
        
        # ------
        # Voltar as linhas comentadas acima e apagar o ultimo return
        # ------
        return ['joao.garcia@ammovarejo.com.br'] # test only
 
    @staticmethod
    def create_kpi_email_body(email_reg: str) -> str:
        return f"""
        Relatório em anexo. Versão em teste de validação. 

        Favor conferir os valores e dar feedback para: {email_reg}

        Observações:

        - A referência de data é sempre o faturamento e não a criação do pedido.

        - Atualmente o valor de Venda Loja (PDV) ainda não considera a venda cupom, mas passará a considerar no futuro.

        - A Meta Loja (PDV) não contempla a meta do multicanal.
        """
    
    @staticmethod
    def create_kpi_email_subject(store: StoreInfo, report_date_string: str) -> str:
        return f'[TESTE] Report Diário Loja: {store.marca_loja} {store.nome_loja} - {report_date_string}'
    
