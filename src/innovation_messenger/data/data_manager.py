import pandas as pd
import datetime
from typing import Tuple, Dict, Callable
import numpy as np

from innovation_messenger.database.data_read import DataRead
from innovation_messenger.database.queries.query_lojas import QUERY_LOJAS
from innovation_messenger.database.queries.query_metas import QUERY_METAS
from innovation_messenger.database.queries.query_parcelas import QUERY_PARCELAS
from innovation_messenger.database.queries.query_vendas import QUERY_VENDAS
from innovation_messenger.database.queries.query_vendedores import QUERY_VENDEDORES

class KpiDataManager:
    df_kpis_loja: pd.DataFrame
    
    def __init__(
            self, 
            delta_days:int =1
            ) -> None:
        self._sources : Dict[str, Callable] = {
            'local': DataRead.from_local_pickle,
            'bigquery': DataRead.from_bigquery
        }
        self.delta_days = delta_days
        self.yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=self.delta_days))
        self.yesterday_date_str = self.yesterday_date.strftime("%Y-%m-%d")

    @property
    def all_dataframes(self) -> Dict[str, pd.DataFrame]:
        return {
            'df_metas':self.df_metas,
            'df_lojas':self.df_lojas,
            'df_vendedores':self.df_vendedores,
            'df_vendas':self.df_vendas,
            'df_parcelas':self.df_parcelas,
            'df_vendas_pdv':self.df_vendas_pdv,
            'df_parcelas_with_displaycode':self.df_parcelas_with_displaycode,
            'df_nome_vendedor':self.df_nome_vendedor
        }

    def fetch_and_build_datasets(self, source: str) -> bool:
        self._fetch_data_from_bigquery()
        self._build_df_vendas_pdv()
        self._build_df_parcelas_with_displaycode()
        
        self.df_nome_vendedor = self.df_vendas_pdv.groupby(['vendedor','cpf_vendedor_inteiro'])['is_frete'].max().reset_index().drop(columns='is_frete')
        
        kpis_loja_dict = {}
        
        for kpi_period in ['Dia','Mês','Ano']:
            kpis_loja_dict[f'kpis_loja_{kpi_period.lower()}'] = self._build_kpis_dataframe(
                kpi_type='loja',
                kpi_period=kpi_period
         )
            
        self.df_kpis_loja = pd.concat(list(kpis_loja_dict.values()))

        kpis_vendedor_dict = {}
        for kpi_period in ['Dia','Mês','Ano']:
            kpis_vendedor_dict[f'kpis_vendedor_{kpi_period.lower()}'] = self._build_kpis_dataframe(
                kpi_type='vendedor',
                kpi_period=kpi_period
            )

        df_kpis_vendedor = pd.concat(list(kpis_vendedor_dict.values()))
        df_kpis_vendedor = df_kpis_vendedor.dropna(subset='cpf_vendedor_inteiro')
        mask = df_kpis_vendedor['cpf_vendedor_inteiro'] != 'Devolução'
        self.df_kpis_vendedor = df_kpis_vendedor[mask]
    
        return True

    def _fetch_data_from_bigquery(self) -> None:
        self.df_lojas = DataRead.from_bigquery(QUERY_LOJAS)
        self.df_vendedores = DataRead.from_bigquery(QUERY_VENDEDORES)
        self.df_vendas = DataRead.from_bigquery(QUERY_VENDAS)
        self.df_parcelas = DataRead.from_bigquery(QUERY_PARCELAS)
        self.df_metas = DataRead.from_bigquery(QUERY_METAS).rename(columns = {
        'cpf_vendedor':'cpf_vendedor_inteiro',
        'loja':'distributorId'
        })

    def _build_df_vendas_pdv(self) -> None:
        df_vendas_temp = self.df_vendas.copy()
        
        PDV_TYPE_LIST = (['STORE', 'PI - 360', 'PI', 'EP', 'Troca', 'Devolução'])
        df_vendas_temp['is_frete'] = df_vendas_temp['tipo_transacao'] == 'frete'
        df_vendas_temp = df_vendas_temp.sort_values(['displaycode','is_frete']).reset_index(drop=True)
        df_vendas_temp['tipo_transacao'] = df_vendas_temp['tipo_transacao'].replace('frete', None)
        df_vendas_temp['tipo_transacao'] = df_vendas_temp['tipo_transacao'].fillna(df_vendas_temp['tipo_transacao'].shift(1))
        df_vendas_temp['venda_cupom'] = ~ df_vendas_temp['cupom_vendedor'].isnull()
        
        
        mask_pdv = df_vendas_temp['tipo_transacao'].isin(PDV_TYPE_LIST)
        
        df_vendas_pdv = df_vendas_temp[mask_pdv]
        df_vendas_pdv.loc[:,'tipo_transacao'] = df_vendas_pdv['tipo_transacao'].replace('PI - 360', 'STORE')
        df_vendas_pdv.loc[:,'tipo_transacao'] = df_vendas_pdv['tipo_transacao'].replace('PI', 'STORE')
        df_vendas_pdv.loc[:,'tipo_transacao'] = df_vendas_pdv['tipo_transacao'].replace('EP', 'STORE')

        self.df_vendas_pdv = df_vendas_pdv.reset_index(drop=True)
        
        return None

    def _build_df_parcelas_with_displaycode(self):
        df_vendedor_displaycode = self.df_vendas_pdv.groupby(['displaycode','cpf_vendedor_inteiro','distributorId'])['year'].count().reset_index().drop(columns='year')
        
        df_parcelas_with_displaycode = self.df_parcelas.merge(df_vendedor_displaycode, how='left', on='displaycode')
        self.df_parcelas_with_displaycode = df_parcelas_with_displaycode
        return None

    def _build_kpis_dataframe(
            self,
            kpi_period:str,
            kpi_type:str,
            **kwargs
            ) -> pd.DataFrame:


        mask_tickets, mask_vendas, mask_parcelas, mask_meta = self._build_masks(
            kpi_period=kpi_period,
            kpi_type=kpi_type,
            )


        df_kpis = self._merge_dataframes(
                kpi_period=kpi_period,
                kpi_type=kpi_type,
                mask_vendas=mask_vendas,
                mask_tickets=mask_tickets,
                mask_parcelas=mask_parcelas,
                mask_meta=mask_meta)

        if kpi_type == 'loja':
            if kpi_period == 'Ano':
                df_kpis['tkts_per_day'] = df_kpis['tkts']/self.yesterday_date.timetuple().tm_yday
            if kpi_period == 'Mês':
                df_kpis['tkts_per_day'] = df_kpis['tkts']/self.yesterday_date.day
            if kpi_period == 'Dia':
                df_kpis['tkts_per_day'] = df_kpis['tkts']

        elif kpi_type == 'vendedor':
            if kpi_period == 'Mês':
                df_kpis['tkts_per_day'] = df_kpis['tkts']/df_kpis['days_of_work'].round(2)
            else:
                df_kpis['tkts_per_day'] = df_kpis['tkts']
        
        df_kpis['type'] = kpi_period

        df_kpis['mkp'] = (df_kpis['net_value']/df_kpis['store_cost']).round(2)
        df_kpis['tkt_medio'] = df_kpis['net_value']/df_kpis['tkts'].round(2)
        df_kpis['meta_percentual'] = (df_kpis['net_value']/df_kpis['meta']*100).round(2)
        df_kpis['PA'] = df_kpis['amount']/df_kpis['tkts'].round(2)
        df_kpis['discount_percentual'] = ((df_kpis['discount_value']/df_kpis['net_value'])*100).round(2)

        return df_kpis
    
    def _build_masks(
            self,
            kpi_period:str,
            kpi_type:str,
            ) -> Tuple[pd.Series,pd.Series,pd.Series,pd.Series]:

        mask_tickets = self.df_vendas_pdv['tipo_transacao'].isin(['STORE', 'CUPOM']) & self.df_vendas_pdv['is_frete']==False

        mask_vendas = pd.Series(np.ones(self.df_vendas_pdv.shape[0]).astype(bool))

        mask_parcelas = pd.Series(np.ones(self.df_parcelas_with_displaycode.shape[0]).astype(bool))

        if kpi_type == 'loja':
            mask_meta = self.df_metas['tipo_meta'] == 'Meta Loja PDV'
        elif 'vendedor':
            mask_meta = self.df_metas['tipo_meta'] == 'Meta Vendedor PDV'

        if kpi_period == 'Dia':
            mask_yesterday_vendas = self.df_vendas_pdv['invoice_date'].astype(str) == self.yesterday_date_str
            mask_vendas = mask_yesterday_vendas
            mask_tickets = mask_tickets & mask_yesterday_vendas

            mask_metas_yesterday = self.df_metas['date'].astype(str) == self.yesterday_date_str
            mask_meta = mask_meta & mask_metas_yesterday

            mask_parcelas = self.df_parcelas_with_displaycode['data_emissao_NF'].astype(str) == self.yesterday_date_str
        return mask_tickets, mask_vendas, mask_parcelas, mask_meta

    def _merge_dataframes(
            self,
            kpi_period:str,
            kpi_type:str,
            mask_vendas:pd.Series,
            mask_tickets:pd.Series,
            mask_parcelas:pd.Series,
            mask_meta:pd.Series) -> pd.DataFrame:
        
        AGG_DICT = {
            'discount_value': 'sum',
            'net_value': 'sum',
            'store_cost': 'sum'
        }


        GROUP_BY_COLUMNS_DICT = {
            'Ano': ['distributorId', 'year'],
            'Mês': ['distributorId', 'year', 'month'],
            'Dia': ['distributorId', 'year', 'month']
        }
        
        group_by_columns = GROUP_BY_COLUMNS_DICT[kpi_period]
        if kpi_type == 'vendedor':
            group_by_columns = ['cpf_vendedor_inteiro'] + group_by_columns

        df_kpis = self.df_vendas_pdv[mask_vendas].groupby(group_by_columns).agg(AGG_DICT).reset_index()

        df_kpis = df_kpis.merge(
            self.df_parcelas_with_displaycode[mask_parcelas].groupby(group_by_columns)['n_parcelas'].mean().reset_index(),
            on=group_by_columns, how='left'
        )
        
        df_kpis = df_kpis.merge(
            self.df_vendas_pdv[mask_tickets].groupby(group_by_columns)['parent_orderId'].nunique().reset_index(
            ).rename(columns={"parent_orderId": "tkts"}), how='left'
        )
        
        df_kpis = df_kpis.merge(
            self.df_vendas_pdv[mask_tickets].groupby(group_by_columns)['amount'].sum().reset_index(), how='left'
        )
        
        df_kpis = df_kpis.merge(
            self.df_metas[mask_meta].groupby(group_by_columns)['meta'].sum().reset_index(), how='left'
        )

        if kpi_type == 'vendedor':
            df_kpis = df_kpis.merge(
                self.df_vendas_pdv.groupby(group_by_columns)['invoice_date'].nunique().reset_index(
                ).rename(columns={'invoice_date':'days_of_work'}), how='left'
            )
        
        if kpi_type == 'day':
            yesterday_date = (datetime.datetime.today() - datetime.timedelta(days=1))
            df_kpis['day'] = yesterday_date.day

        return df_kpis

    def fetch_local_datasets(self, file_path: str) -> pd.DataFrame:
        return DataRead.from_local_pickle(file_path)