SELECT
    med_ID,
    med_group,
    amount,
    cost,
    update_date
FROM
    medicines_available
    JOIN medicines ON(med_id = med_code)
WHERE
    med_group LIKE '%$med_group%'