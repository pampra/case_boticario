WITH dias_atraso AS (
  SELECT id_revendedor,
         dt_vencimento,
         dt_pagamento,
         CASE
            WHEN dt_pagamento IS NULL AND dt_vencimento < CAST('2023-01-16' AS DATE) THEN DATE_DIFF(CAST('2023-01-16' AS DATE), dt_vencimento, DAY)
            WHEN dt_pagamento > dt_vencimento THEN DATE_DIFF(dt_pagamento, dt_vencimento, DAY)
            ELSE 0
         END AS qtd_dias
    FROM caseq2.tab.tb_titulo
),
dias_atraso_1m AS (
  SELECT MAX(dias_atraso.qtd_dias) AS max_dias_atraso_1m,
         id_revendedor
    FROM dias_atraso
   WHERE dt_vencimento BETWEEN DATE_SUB(CAST('2023-01-16' AS DATE), INTERVAL 30 DAY) AND CAST('2023-01-16' AS DATE)
     AND (dt_pagamento <= CAST('2023-01-16' AS DATE)
      OR dt_pagamento IS NULL)
GROUP BY id_revendedor
),
dias_atraso_3m AS (
  SELECT MAX(dias_atraso.qtd_dias) AS max_dias_atraso_3m,
         id_revendedor
    FROM dias_atraso
   WHERE dt_vencimento BETWEEN DATE_SUB(CAST('2023-01-16' AS DATE), INTERVAL 90 DAY) AND CAST('2023-01-16' AS DATE)
     AND (dt_pagamento <= CAST('2023-01-16' AS DATE)
      OR dt_pagamento IS NULL)
GROUP BY id_revendedor
),
faturado_3m AS (
  SELECT FORMAT('%.2f', SUM(CAST(REPLACE(CAST(vlr_pedido AS STRING), ',', '.') AS FLOAT64) / 100)) AS total_faturado_3m,
         id_revendedor
    FROM caseq2.tab.tb_titulo
   WHERE dt_pagamento IS NOT NULL
     AND dt_vencimento BETWEEN DATE_SUB(CAST('2023-01-16' AS DATE), INTERVAL 90 DAY) AND CAST('2023-01-16' AS DATE)
     AND dt_pagamento <= CAST('2023-01-16' AS DATE)
GROUP BY id_revendedor
),
qtd_boletos AS (
  SELECT COUNT(*) AS total_boletos_3m,
         id_revendedor
    FROM caseq2.tab.tb_titulo
   WHERE forma_pagamento = 'Boleto a Prazo'
     AND dt_vencimento BETWEEN DATE_SUB(CAST('2023-01-16' AS DATE), INTERVAL 90 DAY) AND CAST('2023-01-16' AS DATE)
GROUP BY id_revendedor
)

SELECT tb_revendedor.id_revendedor,
       tb_revendedor.nm_revendedor,
       dias_atraso_1m.max_dias_atraso_1m,
       dias_atraso_3m.max_dias_atraso_3m,
       faturado_3m.total_faturado_3m,
       qtd_boletos.total_boletos_3m
  FROM caseq2.tab.tb_revendedor
  JOIN dias_atraso_1m
    ON dias_atraso_1m.id_revendedor = tb_revendedor.id_revendedor
  JOIN dias_atraso_3m
    ON dias_atraso_3m.id_revendedor = tb_revendedor.id_revendedor
  JOIN faturado_3m
    ON faturado_3m.id_revendedor = tb_revendedor.id_revendedor
  JOIN qtd_boletos
    ON qtd_boletos.id_revendedor = tb_revendedor.id_revendedor