from dataclasses import dataclass
from typing import Dict


@dataclass
class StoreInfo:
    def __init__(self, df_lojas, id_loja):
        mask = df_lojas["loja_id"] == id_loja

        if len(df_lojas[mask]["nome_completo"].values) == 0:
            nome_loja = ""
        else:
            nome_loja: str = df_lojas[mask]["nome_completo"].values[0].title()

        if len(df_lojas[mask]["marca"].values) == 0:
            marca_loja = ""
        else:
            marca_loja: str = df_lojas[mask]["marca"].values[0].title()

        if len(df_lojas[mask]["tipo"].values) == 0:
            tipo: str = ""
        else:
            tipo: str = df_lojas[mask]["tipo"].values[0].title()

        if len(df_lojas[mask]["regional"].values) == 0:
            regional = ""
        else:
            regional: str = df_lojas[mask]["regional"].values[0].title()

        if len(df_lojas[mask]["email"].values) == 0:
            self.email = ""
        else:
            self.email = df_lojas[mask]["email"].values[0]

        self.nome_loja = nome_loja
        self.marca_loja = marca_loja
        self.tipo = tipo
        self.regional = regional
        self.email_regional = self._get_regional_email(regional_name=self.regional)
        self.loja_id = id_loja

    def _get_regional_email(self, regional_name: str):
        emails_regionais = self.emails_regionais()

        if regional_name.lower() in emails_regionais:
            return emails_regionais[regional_name.lower()]
        else:
            return ""

    def emails_regionais(self) -> Dict[str, str]:
        return {
            "luciano": "luciano.millamonte@coteminas.com.br",
            "clarissa": "clarissa.ferreira@ammovarejo.com.br",
            "claudio": "claudio.oliveira@ammovarejo.com.br",
            "ivan": "ivan.teixeira@ammovarejo.com.br",
            "zeuxis": "zeuxis.guimaraes@coteminas.com.br",
            "rodrigo": "rodrigo.graci@coteminas.com.br",
            "sandra": "sandra.pereira@ammovarejo.com.br",
            "henrique": "henrique.silva@ammovarejo.com.br",
            "mateus": "mateus.barboza@ammovarejo.com.br",
        }
