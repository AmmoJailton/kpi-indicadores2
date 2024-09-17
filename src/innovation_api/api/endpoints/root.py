import datetime
import os
from typing import List

from commom.data.data_manager import KpiDataManager
from commom.data_classes.report_content_data_class import DailyReportBody, DebugBody
from commom.data_classes.store_info_data_class import StoreInfo
from commom.report_generator import ReportGenerator
from innovation_api import __version__
from innovation_api.typing import IEndpoint, IEndpointConfig
from innovation_messenger import IEmailProperties, Messenger


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
    TAGS = ["KPI report"]

    @property
    def endpoints(self) -> List[IEndpointConfig]:
        return [
            IEndpointConfig(
                route="/dailyreport", class_method=self.send_kpi_daily_mail, rest_method="POST", tags=self.TAGS
            ),
            IEndpointConfig(
                route="/dailyreport-all",
                class_method=self.send_kpi_daily_mail_all,
                rest_method="POST",
                tags=self.TAGS,
            ),
        ]

    def __init__(self) -> None:
        self.kpi_data_manager = KpiDataManager()
        pass

    def send_kpi_daily_mail(self, body: DailyReportBody):
        if body.debug_mode:
            self.kpi_data_manager = self.kpi_data_manager.fetch_and_build_datasets(
                source="local", file_path="./notebooks/kpi_data_manager.pkl"
            )
        elif self.kpi_data_manager.should_fetch_datasets:
            self.kpi_data_manager.fetch_and_build_datasets(source="bigquery")

        ids_loja = body.ids_loja

        reportGenerator = ReportGenerator()

        yesterday_date = datetime.datetime.today() - datetime.timedelta(days=1)
        yesterday_date_str = yesterday_date.strftime("%d.%m.%Y").replace("/", "_")

        for id in ids_loja:
            store = StoreInfo(df_lojas=self.kpi_data_manager.df_lojas, id_loja=id)

            formated_content = reportGenerator.format_report_content(
                report_type="kpi",
                df_kpis_loja=self.kpi_data_manager.df_kpis_loja,
                df_kpis_vendedor=self.kpi_data_manager.df_kpis_vendedor,
                df_nome_vendedor=self.kpi_data_manager.df_nome_vendedor,
                yesterday_date=yesterday_date_str,
                store=store,
            )

            file_name = reportGenerator.generate_report(report_type="kpi", obj_report_content=formated_content)

            if len(body.custom_recipients) > 0:
                emails_recipients_list = body.custom_recipients
            else:
                emails_recipients_list = reportGenerator.get_recipients_for_report(
                    report_type="kpi",
                    store=store,
                )

            if len(emails_recipients_list) >= 1:
                email_properties = IEmailProperties(
                    subject=reportGenerator.create_kpi_email_subject(
                        store=store, report_date_string=yesterday_date_str
                    ),
                    recipient=emails_recipients_list,
                    file_name=file_name,
                    body=reportGenerator.create_kpi_email_body(store.email_regional),
                )

                Messenger.send_message(
                    channel="email",
                    email_properties=email_properties,
                )

            reportGenerator.delete_report_file(file_name=file_name)

        return {
            "statusCode": 201,
            "recipients": emails_recipients_list,
        }

    def send_kpi_daily_mail_all(self, body: DebugBody):
        self.kpi_data_manager.fetch_and_build_datasets(source="local", file_path="./notebooks/kpi_data_manager2.pkl")
        # self.kpi_data_manager.fetch_and_build_datasets()

        mask_ativa = self.kpi_data_manager.df_lojas["ativa"]

        id_lojas: List[str] = list(self.kpi_data_manager.df_lojas[mask_ativa]["loja_group_code"].unique())

        body = DailyReportBody(ids_loja=id_lojas, debug_mode=body.debug_mode)

        self.send_kpi_daily_mail(body=body)
