from google.cloud import bigquery

client = bigquery.Client()

dataset_id = 'caseq1.tab'
tabela = 'local'

query = f"""
SELECT column_name
FROM `{dataset_id}.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = '{tabela}'
"""

query = client.query(query)
colunas = query.result()

colunas_em_comum = [row.column_name for row in colunas]

base_query = """
SELECT local.id,{comparacoes}
  FROM caseq1.tab.local AS local
  JOIN caseq1.tab.gcp AS gcp
    ON local.id = gcp.id
 WHERE {condicoes};
"""

comparacoes = []
condicoes   = []

for col in colunas_em_comum:
    comparacoes.append(f"""
       CASE
         WHEN local.{col} IS DISTINCT FROM gcp.{col} THEN 
           'Local: ' || CAST(local.{col} AS STRING) || ', GCP: ' || CAST(gcp.{col} AS STRING)
         ELSE NULL
       END AS {col}""")
    condicoes.append(f"local.{col} != gcp.{col}")

string_comparacoes = ', '.join(comparacoes)
string_condicoes = '\n    OR '.join(condicoes)

sql_query = base_query.format(comparacoes=string_comparacoes, condicoes=string_condicoes)

print(sql_query)
