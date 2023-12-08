SELECT
    sup_code,
    sup_name,
    city,
    contract_date
FROM
    suppliers
WHERE
    termination_date IS NULL
    AND city LIKE '%$city%'