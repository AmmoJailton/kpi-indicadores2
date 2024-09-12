class StoreInfo():

  def __init__(self, df_lojas, id_loja):
    mask = df_lojas['loja_id'] == id_loja
    
    nome_loja:str = df_lojas[mask]['nome_completo'].values[0]
    marca_loja:str = df_lojas[mask]['marca'].values[0]
    tipo:str = df_lojas[mask]['tipo'].values[0]
    regional:str = df_lojas[mask]['regional'].values[0]
    
    self.email:str = df_lojas[mask]['email'].values[0]
    self.nome_loja = nome_loja.title()
    self.marca_loja = marca_loja.title()
    self.tipo = tipo.title()
    self.regional = regional.title()
    self.email_regional = self._get_regional_email(regional_name=self.regional)
    self.loja_id = id_loja
  
  def _get_regional_email(self, regional_name:str):
    emails_regionais = {
      'luciano': 'luciano.millamonte@coteminas.com.br',
      'clarissa': 'clarissa.ferreira@ammovarejo.com.br',
      'claudio': 'claudio.oliveira@ammovarejo.com.br',
      'ivan': 'ivan.teixeira@ammovarejo.com.br',
      'zeuxis': 'zeuxis.guimaraes@coteminas.com.br',
      'rodrigo': 'rodrigo.graci@coteminas.com.br',
      'sandra': 'sandra.pereira@ammovarejo.com.br',
    }
    
    # if regional_name.lower() in names_regionais:
    #   return names_regionais[regional_name.lower()]
    # else:
    #   return 'joao.garcia@ammovarejo.com.br'
    return 'joao.garcia@ammovarejo.com.br'
    