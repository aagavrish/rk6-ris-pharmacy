SELECT
    med_code,
    med_name,
    med_group,
    med_company,
    med_country,
    amount,
    cost
FROM
    medicines
    JOIN medicines_available ON(med_id = med_code)
WHERE
    med_country LIKE '%$med_country%'