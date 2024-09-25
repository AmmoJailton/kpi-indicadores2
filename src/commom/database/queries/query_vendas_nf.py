QUERY_VENDAS_NF = """
SELECT
  distributorId,
  EXTRACT(YEAR
  FROM
    createdAt) AS year,
  EXTRACT(MONTH
  FROM
    createdAt) AS month,
  fiscalsParentOrder AS parent_orderId,
  fat_vendas_nf.displayCode AS displaycode,
  createdAt AS invoice_date,
  omniChannelType AS tipo_transacao,
  employeeCpf AS cpf_vendedor_inteiro,
  SUM(amount) AS amount,
  SUM(paidFreight) AS paidFreight,
  SUM(customerShippingCost) AS customerShippingCost,
  SUM(grossValue) AS grossValue,
  SUM(discount) AS discount_value,
  SUM(cost) AS store_cost,
  SUM(netValue) AS net_value
FROM
  `projetoomni.innovation_dataset.vendas_lojas_temp` fat_vendas_nf
LEFT JOIN
  `ammo_dw.dim_display_code` dim_display_code
ON
  fat_vendas_nf.displayCode = dim_display_code.displayCode
WHERE
  EXTRACT(YEAR
  FROM
    createdAt) = 2024
GROUP BY
  1, 2, 3, 4, 5, 6, 7, 8
"""
