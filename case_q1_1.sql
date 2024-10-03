SELECT *
  FROM caseq1.tab.local
 WHERE NOT EXISTS (
    SELECT TRUE
      FROM caseq1.tab.gcp
     WHERE gcp.id = local.id
 );

SELECT *
  FROM caseq1.tab.gcp
 WHERE NOT EXISTS (
    SELECT TRUE
      FROM caseq1.tab.local
     WHERE local.id = gcp.id
 );
 
 SELECT local.id,
       CASE
         WHEN local.ID IS DISTINCT FROM gcp.ID THEN 
           'Local: ' || CAST(local.ID AS STRING) || ', GCP: ' || CAST(gcp.ID AS STRING)
         ELSE NULL
       END AS ID, 
       CASE
         WHEN local.CODE_GENDER IS DISTINCT FROM gcp.CODE_GENDER THEN 
           'Local: ' || CAST(local.CODE_GENDER AS STRING) || ', GCP: ' || CAST(gcp.CODE_GENDER AS STRING)
         ELSE NULL
       END AS CODE_GENDER, 
       CASE
         WHEN local.FLAG_OWN_CAR IS DISTINCT FROM gcp.FLAG_OWN_CAR THEN 
           'Local: ' || CAST(local.FLAG_OWN_CAR AS STRING) || ', GCP: ' || CAST(gcp.FLAG_OWN_CAR AS STRING)
         ELSE NULL
       END AS FLAG_OWN_CAR, 
       CASE
         WHEN local.FLAG_OWN_REALTY IS DISTINCT FROM gcp.FLAG_OWN_REALTY THEN 
           'Local: ' || CAST(local.FLAG_OWN_REALTY AS STRING) || ', GCP: ' || CAST(gcp.FLAG_OWN_REALTY AS STRING)
         ELSE NULL
       END AS FLAG_OWN_REALTY, 
       CASE
         WHEN local.CNT_CHILDREN IS DISTINCT FROM gcp.CNT_CHILDREN THEN 
           'Local: ' || CAST(local.CNT_CHILDREN AS STRING) || ', GCP: ' || CAST(gcp.CNT_CHILDREN AS STRING)
         ELSE NULL
       END AS CNT_CHILDREN, 
       CASE
         WHEN local.AMT_INCOME_TOTAL IS DISTINCT FROM gcp.AMT_INCOME_TOTAL THEN 
           'Local: ' || CAST(local.AMT_INCOME_TOTAL AS STRING) || ', GCP: ' || CAST(gcp.AMT_INCOME_TOTAL AS STRING)
         ELSE NULL
       END AS AMT_INCOME_TOTAL, 
       CASE
         WHEN local.NAME_INCOME_TYPE IS DISTINCT FROM gcp.NAME_INCOME_TYPE THEN 
           'Local: ' || CAST(local.NAME_INCOME_TYPE AS STRING) || ', GCP: ' || CAST(gcp.NAME_INCOME_TYPE AS STRING)
         ELSE NULL
       END AS NAME_INCOME_TYPE, 
       CASE
         WHEN local.NAME_EDUCATION_TYPE IS DISTINCT FROM gcp.NAME_EDUCATION_TYPE THEN 
           'Local: ' || CAST(local.NAME_EDUCATION_TYPE AS STRING) || ', GCP: ' || CAST(gcp.NAME_EDUCATION_TYPE AS STRING)
         ELSE NULL
       END AS NAME_EDUCATION_TYPE, 
       CASE
         WHEN local.NAME_FAMILY_STATUS IS DISTINCT FROM gcp.NAME_FAMILY_STATUS THEN 
           'Local: ' || CAST(local.NAME_FAMILY_STATUS AS STRING) || ', GCP: ' || CAST(gcp.NAME_FAMILY_STATUS AS STRING)
         ELSE NULL
       END AS NAME_FAMILY_STATUS, 
       CASE
         WHEN local.NAME_HOUSING_TYPE IS DISTINCT FROM gcp.NAME_HOUSING_TYPE THEN 
           'Local: ' || CAST(local.NAME_HOUSING_TYPE AS STRING) || ', GCP: ' || CAST(gcp.NAME_HOUSING_TYPE AS STRING)
         ELSE NULL
       END AS NAME_HOUSING_TYPE, 
       CASE
         WHEN local.DAYS_BIRTH IS DISTINCT FROM gcp.DAYS_BIRTH THEN 
           'Local: ' || CAST(local.DAYS_BIRTH AS STRING) || ', GCP: ' || CAST(gcp.DAYS_BIRTH AS STRING)
         ELSE NULL
       END AS DAYS_BIRTH, 
       CASE
         WHEN local.DAYS_EMPLOYED IS DISTINCT FROM gcp.DAYS_EMPLOYED THEN 
           'Local: ' || CAST(local.DAYS_EMPLOYED AS STRING) || ', GCP: ' || CAST(gcp.DAYS_EMPLOYED AS STRING)
         ELSE NULL
       END AS DAYS_EMPLOYED, 
       CASE
         WHEN local.FLAG_MOBIL IS DISTINCT FROM gcp.FLAG_MOBIL THEN 
           'Local: ' || CAST(local.FLAG_MOBIL AS STRING) || ', GCP: ' || CAST(gcp.FLAG_MOBIL AS STRING)
         ELSE NULL
       END AS FLAG_MOBIL, 
       CASE
         WHEN local.FLAG_WORK_PHONE IS DISTINCT FROM gcp.FLAG_WORK_PHONE THEN 
           'Local: ' || CAST(local.FLAG_WORK_PHONE AS STRING) || ', GCP: ' || CAST(gcp.FLAG_WORK_PHONE AS STRING)
         ELSE NULL
       END AS FLAG_WORK_PHONE, 
       CASE
         WHEN local.FLAG_PHONE IS DISTINCT FROM gcp.FLAG_PHONE THEN 
           'Local: ' || CAST(local.FLAG_PHONE AS STRING) || ', GCP: ' || CAST(gcp.FLAG_PHONE AS STRING)
         ELSE NULL
       END AS FLAG_PHONE, 
       CASE
         WHEN local.FLAG_EMAIL IS DISTINCT FROM gcp.FLAG_EMAIL THEN 
           'Local: ' || CAST(local.FLAG_EMAIL AS STRING) || ', GCP: ' || CAST(gcp.FLAG_EMAIL AS STRING)
         ELSE NULL
       END AS FLAG_EMAIL, 
       CASE
         WHEN local.OCCUPATION_TYPE IS DISTINCT FROM gcp.OCCUPATION_TYPE THEN 
           'Local: ' || CAST(local.OCCUPATION_TYPE AS STRING) || ', GCP: ' || CAST(gcp.OCCUPATION_TYPE AS STRING)
         ELSE NULL
       END AS OCCUPATION_TYPE, 
       CASE
         WHEN local.CNT_FAM_MEMBERS IS DISTINCT FROM gcp.CNT_FAM_MEMBERS THEN 
           'Local: ' || CAST(local.CNT_FAM_MEMBERS AS STRING) || ', GCP: ' || CAST(gcp.CNT_FAM_MEMBERS AS STRING)
         ELSE NULL
       END AS CNT_FAM_MEMBERS
  FROM caseq1.tab.local AS local
  JOIN caseq1.tab.gcp AS gcp
    ON local.id = gcp.id
 WHERE local.ID != gcp.ID
    OR local.CODE_GENDER != gcp.CODE_GENDER
    OR local.FLAG_OWN_CAR != gcp.FLAG_OWN_CAR
    OR local.FLAG_OWN_REALTY != gcp.FLAG_OWN_REALTY
    OR local.CNT_CHILDREN != gcp.CNT_CHILDREN
    OR local.AMT_INCOME_TOTAL != gcp.AMT_INCOME_TOTAL
    OR local.NAME_INCOME_TYPE != gcp.NAME_INCOME_TYPE
    OR local.NAME_EDUCATION_TYPE != gcp.NAME_EDUCATION_TYPE
    OR local.NAME_FAMILY_STATUS != gcp.NAME_FAMILY_STATUS
    OR local.NAME_HOUSING_TYPE != gcp.NAME_HOUSING_TYPE
    OR local.DAYS_BIRTH != gcp.DAYS_BIRTH
    OR local.DAYS_EMPLOYED != gcp.DAYS_EMPLOYED
    OR local.FLAG_MOBIL != gcp.FLAG_MOBIL
    OR local.FLAG_WORK_PHONE != gcp.FLAG_WORK_PHONE
    OR local.FLAG_PHONE != gcp.FLAG_PHONE
    OR local.FLAG_EMAIL != gcp.FLAG_EMAIL
    OR local.OCCUPATION_TYPE != gcp.OCCUPATION_TYPE
    OR local.CNT_FAM_MEMBERS != gcp.CNT_FAM_MEMBERS;
