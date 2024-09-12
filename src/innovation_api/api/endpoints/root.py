import datetime
import os
from typing import List

from commom.data.data_manager import KpiDataManager
from commom.data_classes.report_content_data_class import DailyReportBody
from commom.data_classes.store_info_data_class import StoreInfo
from commom.report_generator import ReportGenerator
from innovation_api import __version__
from innovation_api.typing import IEndpoint, IEndpointConfig
from innovation_messenger import IEmailSender, Messenger


class RootEndpoint(IEndpoint):
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [IEndpointConfig(route="/", class_method=self.get_info, rest_method="GET", tags=["Get Info"])]

    def __init__(self) -> None:
        pass

    def get_info(self):
        now = datetime.datetime.now()
        return {
            "statusCode": 201,
            "version": __version__,
            "env": os.getenv("ENV"),
            "Status": f"A requisição foi feita em: {now}",
        }


class TestEndpoint(IEndpoint):
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [IEndpointConfig(route="/test", class_method=self.get_info, rest_method="GET", tags=["Get Info"])]

    def __init__(self) -> None:
        pass

    def get_info(self):
        return {"statusCode": 201, "version": __version__, "env": os.getenv("ENV"), "test": "endpoint de teste"}


class DailyReportEndpoint(IEndpoint):
    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [
            IEndpointConfig(
                route="/dailyreport", class_method=self.enviar_email_kpi_diario, rest_method="POST", tags=["KPI report"]
            )
        ]

    def __init__(self) -> None:
        pass

    def enviar_email_kpi_diario(self, body: DailyReportBody):
        kpi_data_manager = KpiDataManager()

        # if kpi_data_manager.should_fetch_datasets:
        #     kpi_data_manager.fetch_and_build_datasets()

        dataframes = kpi_data_manager.fetch_local_datasets("./notebooks/kpi_data_manager.pkl")  # mock

        ids_loja = body.ids_loja

        reportGenerator = ReportGenerator()

        yesterday_date = datetime.datetime.today() - datetime.timedelta(days=1)
        yesterday_date_str = yesterday_date.strftime("%d.%m.%Y").replace("/", "_")

        for id in ids_loja:
            store = StoreInfo(df_lojas=dataframes.df_lojas, id_loja=id)

            # formated_content = reportGenerator.format_report_content(
            #     report_type='kpi',
            #     df_kpis_loja = kpi_data_manager.df_kpis_loja,
            #     df_kpis_vendedor = kpi_data_manager.df_kpis_vendedor,
            #     df_nome_vendedor = kpi_data_manager.df_nome_vendedor,
            #     yesterday_date= yesterday_date_str,
            #     store = store
            # )

            formated_content = reportGenerator.format_report_content(
                report_type="kpi",
                df_kpis_loja=dataframes.df_kpis_loja,
                df_kpis_vendedor=dataframes.df_kpis_vendedor,
                df_nome_vendedor=dataframes.df_nome_vendedor,
                yesterday_date=yesterday_date_str,
                store=store,
            )

            file_name = reportGenerator.generate_report(report_type="kpi", obj_report_content=formated_content)

            emails_recipients_list = reportGenerator.get_recipients_for_report(
                report_type="kpi",
                store=store,
            )

            for email_recipient in emails_recipients_list:
                email_sender = IEmailSender(
                    subject=reportGenerator.create_kpi_email_subject(
                        store=store, report_date_string=yesterday_date_str
                    ),
                    recipient=email_recipient,
                    file_name=file_name,
                    body=reportGenerator.create_kpi_email_body(store.email_regional),
                )

                Messenger.send_report(
                    report_channel="email",
                    email_sender=email_sender,
                )

        return {
            "statusCode": 201,
        }
