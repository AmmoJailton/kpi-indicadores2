from fastapi import FastAPI, Body, HTTPException
from innovation_api.api.services.daily_report_service import DailyReportService
from innovation_messenger import Messenger  # Adicione este import
from commom.data_classes.report_content_data_class import DailyReportBody

messenger = Messenger()  # Instancie o Messenger
daily_report_service = DailyReportService(messenger=messenger)  # Passe o messenger
from innovation_api import __version__

fast_api = FastAPI()

@fast_api.get("/", tags=["Get Info"])
def get_info():
    return {
        "status": "ok",
        "version": "0.1.0"
    }

@fast_api.post("/login-artex", tags=["LOGIN ARTEX"])
def login_artex(code_or_email: str = Body(..., embed=True)):
    if not code_or_email:
        return {
            "result": "Error",
            "message": "code_or_email is required"
        }
    # Simulação de autenticação
    if code_or_email == "admin@example.com":
        return {
            "result": "Success",
            "message": "Usuário autenticado"
        }
    else:
        return {
            "result": "Invalid code_or_email",
            "message": None
        }

@fast_api.post("/dailyreport", tags=["KPI report"])
def send_kpi_daily_mail(
    ids_loja: list[str] = Body(..., embed=True),
    debug_mode: bool = Body(False, embed=True),
    custom_recipients: list[str] = Body(default=[], embed=True)
):
    if not ids_loja or len(ids_loja) < 1:
        raise HTTPException(status_code=400, detail="Invalid ids_loja")
    body = DailyReportBody(
        ids_loja=ids_loja,
        debug_mode=debug_mode,
        custom_recipients=custom_recipients
    )
    return daily_report_service.send_kpi_daily_mail(body=body)


@fast_api.post("/dailyreport-all", tags=["KPI report"])
def send_kpi_daily_mail_all(debug_info: dict = Body(...)):
    return daily_report_service.send_kpi_daily_mail_all(body=Body)

