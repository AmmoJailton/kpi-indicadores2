import datetime
from typing import Any, Dict, List
from commom.kpi_data.kpi_data_manager import KpiDataManager
from commom.data_classes.report_content_data_class import DailyReportBody, DebugBody
from commom.data_classes.store_info_data_class import StoreInfo
from commom.report_generator import ReportGenerator
from innovation_messenger import IEmailProperties, Messenger

class DailyReportService():
    kpi_data_manager: KpiDataManager
    reportGenerator: ReportGenerator
    messenger: Messenger
    
    def __init__(self, messenger: Messenger) -> None:
        self.kpi_data_manager = KpiDataManager()
        self.reportGenerator = ReportGenerator()
        self.messenger = messenger
        pass

    def send_kpi_daily_mail(self, body: DailyReportBody) -> Dict[str, Any]:
        ids_loja = body.ids_loja

        yesterday_date = datetime.datetime.today() - datetime.timedelta(days=1)
        yesterday_date_str = yesterday_date.strftime("%d.%m.%Y").replace("/", "_")

        if body.debug_mode:
            self.kpi_data_manager = self.kpi_data_manager.fetch_and_build_datasets(
                source="local", file_path="./notebooks/kpi_data_manager.pkl"
            )
        elif self.kpi_data_manager.should_fetch_datasets:
            self.kpi_data_manager.fetch_and_build_datasets(source="bigquery")

        for id in ids_loja:
            store = StoreInfo(df_lojas=self.kpi_data_manager.df_lojas, id_loja=id)

            formated_content = self.reportGenerator.format_report_content(
                report_type="kpi",
                df_kpis_loja=self.kpi_data_manager.df_kpis_loja,
                df_kpis_vendedor=self.kpi_data_manager.df_kpis_vendedor,
                df_nome_vendedor=self.kpi_data_manager.df_nome_vendedor,
                yesterday_date=yesterday_date_str,
                store=store,
            )

            file_name = ""

            if formated_content.document_file_name != "":
                file_name = self.reportGenerator.generate_report(report_type="kpi", obj_report_content=formated_content)

            # if len(body.custom_recipients) > 0:
            #     emails_recipients_list = body.custom_recipients
            # else:
            #     emails_recipients_list = self.reportGenerator.get_recipients_for_report(
            #         report_type="kpi",
            #         store=store,
            #     )
            emails_recipients_list = ['joao.garcia@ammovarejo.com.br']
            if len(emails_recipients_list) >= 1:
                email_body = self.reportGenerator.create_kpi_email_body(
                    store=store, file_name=file_name, report_date=yesterday_date_str
                )

                email_subject = self.reportGenerator.create_kpi_email_subject(
                    store=store, report_date_string=yesterday_date_str
                )

                email_properties = IEmailProperties(
                    subject=email_subject,
                    recipient=emails_recipients_list,
                    file_name=file_name,
                    body=email_body,
                )

                self.messenger.send_message(
                    channel="email",
                    email_properties=email_properties,
                )

            self.reportGenerator.delete_report_file(file_name=file_name)

        return {
            "statusCode": 201,
            "recipients": emails_recipients_list,
        }

    def send_kpi_daily_mail_all(self, body: DebugBody) -> Dict[str, Any]:
        self.kpi_data_manager.fetch_and_build_datasets(source="bigquery")

        mask_ativa = self.kpi_data_manager.df_lojas["ativa"]

        id_lojas: List[str] = list(self.kpi_data_manager.df_lojas[mask_ativa]["loja_group_code"].unique())

        daily_report_body = DailyReportBody(ids_loja=id_lojas, debug_mode=body.debug_mode)

        return self.send_kpi_daily_mail(body=daily_report_body)
