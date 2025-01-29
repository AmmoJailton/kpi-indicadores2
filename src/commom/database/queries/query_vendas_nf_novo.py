QUERY_VENDAS_NF_NOVO = """
SELECT * FROM `projetoomni.ammo_dw.fato_vendas`
WHERE type IN ('Propria', 'Oulet')
AND EXTRACT( YEAR from createdAt ) >= 2024
"""
