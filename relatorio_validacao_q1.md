
# Considerações sobre a Questão 1

## Automatização do Arquivo .sql
Com o intuito de automatizar o processo, no primeiro arquivo `.sql` foi desenvolvida uma query que verifica as divergências em todas as colunas entre as duas bases. No entanto, como foi utilizado o BigQuery do Google Cloud, não foi possível realizar essa validação de forma dinâmica, sendo necessário criar uma condição para cada coluna.

Para otimizar o processo, no segundo arquivo `.py` foi desenvolvido um script que gera o SQL de forma dinâmica. Nesse caso, não é necessário informar o nome das colunas manualmente, pois o script executa uma query que retorna todas as colunas da tabela local, permitindo a criação automatizada do SQL.

---

## Problemas Identificados

### 1. Registros Duplicados

- **Total de registros duplicados**: 3.000 duplicados.

Exemplo de um registro duplicado encontrado durante a validação de migração de dados na **base GCP**:

| ID      | CODE_GENDER | FLAG_OWN_CAR | FLAG_OWN_REALTY | CNT_CHILDREN | AMT_INCOME_TOTAL | NAME_INCOME_TYPE | NAME_EDUCATION_TYPE | NAME_FAMILY_STATUS | NAME_HOUSING_TYPE | DAYS_BIRTH | DAYS_EMPLOYED | FLAG_MOBIL | FLAG_WORK_PHONE | FLAG_PHONE | FLAG_EMAIL | OCCUPATION_TYPE   | CNT_FAM_MEMBERS |
|---------|-------------|--------------|-----------------|--------------|------------------|------------------|---------------------|--------------------|-------------------|------------|---------------|------------|----------------|------------|------------|-------------------|-----------------|
| 5008804 | Male        | Y            | Y               | 0            | 42750000.0        | Working           | Higher education    | Civil marriage     | Rented apartment  | 12005      | -4542         | 1          | 0              | 0          | 0          | Without Occupation | 2.0             |
| 5008804 | Male        | Y            | Y               | 0            | 42750000.0        | Working           | Higher education    | Civil marriage     | Rented apartment  | 12005      | -4542         | 1          | 0              | 0          | 0          | Without Occupation | 2.0             |

Para conferência dos demais registros duplicados favor acessar o arquivo: 
`duplicados_gcp.csv`

---

### 2. Registros Ausentes

#### Registros ausentes na base GCP (presentes na Local):
- **Total**: 4.051 registros ausentes na GCP.
- **Percentual**: 0.92 %.
Os registros ausentes na base GCP foram exportados para `registros_presentes_somente_na_local.csv`.

#### Registros ausentes na base Local (presentes na GCP):
- **Total**: Não existem registros ausentes na base local.

---

### 3. Diferenças em Campos Específicos

A tabela abaixo apresenta os campos que possuem diferenças entre a base Local e a base GCP, juntamente com a quantidade de diferenças e o percentual dessas diferenças:

| Campo            | Quantidade de Diferenças | Percentual de Diferenças (%) |
|------------------|--------------------------|------------------------------|
| CODE_GENDER      | 437459                   | 100%                         |
| AMT_INCOME_TOTAL | 437459                   | 100%                         |
| DAYS_BIRTH       | 437459                   | 100%                         |
| FLAG_WORK_PHONE  | 311438                   | 71.19%                       |
| OCCUPATION_TYPE  | 133118                   | 30.43%                       |

---

## Diferença no Campo CODE_GENDER

O campo `CODE_GENDER` representa a mesma informação em ambas as bases (Local e GCP), porém é representado de formas diferentes:

- **Base GCP**: O valor é representado como `Male`.
- **Base Local**: O valor é representado como `M`.

Mesmo que os dados subjacentes sejam os mesmos, essa diferença na representação pode gerar inconsistências. As diferenças foram exportadas para `registros_com_diferencas.csv`.

---

### 4. Incompatibilidades de Formato

O campo `FLAG_WORK_PHONE` apresentou incompatibilidade de formato do dado entre a base Local e a base GCP:

| Coluna           | Tipo Base Local | Tipo Base GCP  |
|------------------|-----------------|----------------|
| FLAG_WORK_PHONE  | int64           | float64        |

---

## Anexos
- `registros_presentes_somente_na_local.csv`: Registros ausentes na base GCP.
- `registros_presentes_somente_na_gcp.csv`: Registros ausentes na base Local.
- `registros_com_diferencas.csv`: Registros com diferenças em campos específicos.
- `duplicados_gcp.csv`: Registros duplicados na base GCP.
- `duplicados_local.csv`: Registros duplicados na base Local.
