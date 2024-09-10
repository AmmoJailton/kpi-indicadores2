import datetime
from typing import List
from innovation_messenger.data_classes.report_content_data_class import IPageContent, IReportContent, IReportContentPage
import pandas as pd
from unidecode import unidecode

class KpiDataFormater:
    def __init__(self) -> None:
        pass

    @classmethod
    def format_all_tables(
            self,
            id_loja:str,
            df_kpis_loja:pd.DataFrame,
            df_kpis_vendedor:pd.DataFrame,
            df_nome_vendedor:pd.DataFrame
            ):

        df_store_formated = self._format_store_kpis(
            df_kpis_loja=df_kpis_loja,
            id_loja=id_loja
            )

        if df_store_formated.size==0:
            return pd.DataFrame(),pd.DataFrame(),pd.DataFrame()

        df_vendedor_formated_month = self._format_vendedor_kpis_mes(
            df_kpis_vendedor=df_kpis_vendedor,
            df_nome_vendedor=df_nome_vendedor,
            id_loja=id_loja
            )

        df_vendedor_formated_day = self._format_vendedor_kpis_dia(
            df_kpis_vendedor=df_kpis_vendedor,
            df_nome_vendedor=df_nome_vendedor,
            id_loja=id_loja
            )

        return df_store_formated,df_vendedor_formated_month,df_vendedor_formated_day

    @staticmethod
    def _format_store_kpis(
            df_kpis_loja:pd.DataFrame,
            id_loja:str) -> pd.DataFrame: 
        
        mask = df_kpis_loja['distributorId'] == id_loja

        df_store = df_kpis_loja[mask].fillna(0).copy()
        df_store_current_month = df_store.loc[df_store.groupby(["type"])["month"].idxmax()].drop_duplicates()

        rename_dict ={
            'net_value':'Venda Loja (PDV)',
            'meta':'Meta Loja (PDV)',
            'meta_percentual':'Meta % (PDV)',
            'mkp':'Markup',
            'tkts_per_day':'Tickets/Dia',
            'PA':'Peças por Atendimento',
            'tkt_medio':'Ticket Médio',
            # 'n_parcelas':'Parcela Média',
            'discount_percentual': 'Desconto Médio %',
            'type':'Período'
        }

        format_money = 'R$ {:,.0f}'
        format_percentage = '{:,.0f}%'

        format_dict ={
            'Venda Loja (PDV)': format_money,
            'Meta Loja (PDV)': format_money,
            'Meta % (PDV)':format_percentage,
            'Markup':'{:,.2f}',
            'Tickets/Dia':'{:,.1f}',
            'Peças por Atendimento':'{:,.1f}',
            'Ticket Médio':format_money,
            # 'Parcela Média':'{:,.1f}',
            'Desconto Médio %': format_percentage,
        }

        df_store_formated = df_store_current_month[rename_dict.keys()].round(2).rename(columns=rename_dict)

        for key,format in format_dict.items():
            df_store_formated[key] = df_store_formated[key].map(format.format)

            if format==format_money:
                df_store_formated[key] = df_store_formated[key].str.replace(',', '.')

        try:
            df_store_formated = df_store_formated.set_index('Período').reset_index().T[[1,2,0]]
        except KeyError:
            df_store_formated = pd.DataFrame()
        return df_store_formated

    @staticmethod
    def _format_vendedor_kpis_mes(
            df_kpis_vendedor:pd.DataFrame,
            df_nome_vendedor:pd.DataFrame,
            id_loja:str) -> pd.DataFrame: 
        
        mask = df_kpis_vendedor['distributorId'] == id_loja
        df_vendedor = df_kpis_vendedor[mask].reset_index(drop=True)
        df_vendedor['month'] = df_vendedor['month'].fillna(0)

        mask_ano_dia = df_vendedor['type'].isin(['Mês'])
        mask_mes = df_vendedor['month'] == df_vendedor['month'].max()
        mask = mask_ano_dia & mask_mes
        df_vendedor_mes:pd.DataFrame = df_vendedor[mask].reset_index(drop=True)
        df_vendedor_mes['normalized_net_value'] = df_vendedor_mes['net_value']*100/df_vendedor_mes['net_value'].max().round(2)
        df_vendedor_mes['net_value_share'] = df_vendedor_mes['net_value']*100/df_vendedor_mes['net_value'].max().round(2)
        df_vendedor_mes = df_nome_vendedor.merge(df_vendedor_mes, on='cpf_vendedor_inteiro').drop(columns='cpf_vendedor_inteiro')

        rename_dict ={
            'vendedor': 'Vendedor',
            'days_of_work': 'Dias Trabalhados',
            'net_value':'Acumulado no Mês',
            'normalized_net_value':'Homogeneidade',
            'meta':'Meta do Mês',
            'meta_percentual':'Meta %',
            'mkp':'Markup',
            'tkts_per_day':'Tickets/Dia',
            'PA':'Peças por Atendimento',
            'tkt_medio':'Ticket Médio',
            # 'n_parcelas':'Parcela Média',
            'discount_percentual': 'Desconto Médio %',
            # 'type':'Período'
        }

        format_money = 'R$ {:,.0f}'
        format_percentage = '{:,.0f}%'

        format_dict ={
            'Acumulado no Mês': format_money,
            'Homogeneidade': format_percentage,
            'Meta do Mês':format_money,
            'Meta %':format_percentage,
            'Markup':'{:,.2f}',
            'Tickets/Dia':'{:,.1f}',
            'Peças por Atendimento':'{:,.1f}',
            'Ticket Médio':format_money,
            # 'Parcela Média':'{:,.1f}',
            'Desconto Médio %': format_percentage,
        }


        df_vendedor_mes_formatado = (df_vendedor_mes[rename_dict.keys()].sort_values('normalized_net_value', ascending=False).round(2).rename(columns=rename_dict))
    
        for key,format in format_dict.items():
            df_vendedor_mes_formatado[key] = df_vendedor_mes_formatado[key].map(format.format)
            if format==format_money:
                df_vendedor_mes_formatado[key] = df_vendedor_mes_formatado[key].str.replace(',', '.')
    
        df_vendedor_mes_formatado = df_vendedor_mes_formatado.reset_index(drop=True).T.reset_index().T

        return df_vendedor_mes_formatado.set_index(0)

    @staticmethod
    def _format_vendedor_kpis_dia(
            df_kpis_vendedor:pd.DataFrame,
            df_nome_vendedor:pd.DataFrame,
            id_loja:str) -> pd.DataFrame:

        mask = df_kpis_vendedor['distributorId'] == id_loja
        df_vendedor = df_kpis_vendedor[mask].reset_index(drop=True)
        df_vendedor['month'] = df_vendedor['month'].fillna(0)

        mask_dia = df_vendedor['type'].isin(['Dia'])
        df_vendedor_dia = df_vendedor[mask_dia].reset_index(drop=True)
        df_vendedor_dia['normalized_net_value'] = df_vendedor_dia['net_value']*100/df_vendedor_dia['net_value'].max().round(2)
        df_vendedor_dia['net_value_share'] = df_vendedor_dia['net_value']*100/df_vendedor_dia['net_value'].max().round(2)
        df_vendedor_dia = df_nome_vendedor.merge(df_vendedor_dia, on='cpf_vendedor_inteiro').drop(columns='cpf_vendedor_inteiro')

        rename_dict ={
            'vendedor': 'Vendedor',
            'net_value':'Acumulado no Dia',
            'normalized_net_value':'Homogeneidade',
            'meta':'Meta do Dia',
            'meta_percentual':'Meta %',
            'mkp':'Markup',
            'tkts_per_day':'Tickets',
            'PA':'Peças por Atendimento',
            'tkt_medio':'Ticket Médio',
            # 'n_parcelas':'Parcela Média',
            'discount_percentual': 'Desconto Médio %'

        }

        format_money = 'R$ {:,.0f}'
        format_percentage = '{:,.0f}%'

        format_dict ={
            'Acumulado no Dia': format_money,
            'Homogeneidade': format_percentage,
            'Meta do Dia':format_money,
            'Meta %':format_percentage,
            'Markup':'{:,.2f}',
            'Tickets':'{:,.0f}',
            'Peças por Atendimento':'{:,.1f}',
            'Ticket Médio':format_money,
            # 'Parcela Média':'{:,.1f}',
            'Desconto Médio %': format_percentage,
        }


        df_vendedor_dia_formatado = df_vendedor_dia[rename_dict.keys()].sort_values('normalized_net_value', ascending=False).rename(columns=rename_dict)

        for key,format in format_dict.items():
            df_vendedor_dia_formatado[key] = df_vendedor_dia_formatado[key].map(format.format)
            if format==format_money:
                df_vendedor_dia_formatado[key] = df_vendedor_dia_formatado[key].str.replace(',', '.')

        df_vendedor_dia_formatado = df_vendedor_dia_formatado.reset_index(drop=True).T.reset_index().T
        return df_vendedor_dia_formatado.set_index(0)