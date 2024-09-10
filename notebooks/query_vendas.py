QUERY_VENDAS = '''
SELECT
  EXTRACT(YEAR FROM invoice_date) AS year,
  EXTRACT(MONTH FROM invoice_date) AS month,
  parent_orderId,
  displaycode,
  invoice_date,
  distributorId,
  groupCode,
  distributorId_ajustado,
  tipo_transacao,
  vendedor,
  cupom_vendedor,
  cpf_vendedor_inteiro,  
  SUM(priceFrom) AS priceFrom,
  SUM(priceTo) AS priceTo, 
  SUM(sellin_value) AS sellin_value, 
  SUM(accounting_cost_value) AS accounting_cost_value, 
  SUM(store_cost) AS store_cost, 
  SUM(custo_cd) AS custo_cd, 
  SUM(amount) AS amount, 
  SUM(full_value) AS full_value, 
  SUM(gross_value) AS gross_value, 
  SUM(discount_value) AS discount_value, 
  SUM(net_value) AS net_value
  
FROM `projetoomni.isa_workspace.query_referencia_vendas`
WHERE EXTRACT(YEAR FROM invoice_date) = 2024

GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12
'''