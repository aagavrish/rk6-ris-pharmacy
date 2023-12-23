SELECT
    med_ID,
    med_name,
    med_company,
    amount,
    cost
FROM
    medicines_available
    JOIN medicines ON(med_ID = med_code)
WHERE
    amount > 0
ORDER BY
    amount DESC