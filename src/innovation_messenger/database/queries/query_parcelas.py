QUERY_PARCELAS = '''
SELECT 
  EXTRACT(YEAR FROM data_emissao_NF) AS year,
  EXTRACT(MONTH FROM data_emissao_NF) AS month,
  data_emissao_NF,
  displaycode,
  AVG(qtd_parcelado) AS n_parcelas,
  FROM `projetoomni.isa_workspace.fat_pagamento`
WHERE EXTRACT(YEAR FROM data_emissao_NF) = 2024
GROUP BY 1,2,3,4
'''