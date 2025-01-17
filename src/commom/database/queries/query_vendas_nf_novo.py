QUERY_VENDAS_NF_NOVO = """
SELECT * FROM `projetoomni.ammo_dw.fato_vendas` 
WHERE EXTRACT(YEAR FROM createdAt) >= 2024
"""
