QUERY_METAS = """
SELECT
  EXTRACT(YEAR FROM dia) AS year,
  EXTRACT(MONTH FROM dia) AS month,
  dia AS date,
  loja,
  cpf_vendedor,
  tipo_meta,
  META as meta

FROM `projetoomni.isa_workspace.fat_metas`

WHERE EXTRACT(YEAR FROM dia) = 2024 AND
tipo_meta IN ('Meta Loja PDV', 'Meta Vendedor PDV') AND
dia <= CURRENT_DATE()  - 1
"""
