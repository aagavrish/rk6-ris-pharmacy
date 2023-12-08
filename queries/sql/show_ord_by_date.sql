SELECT
    conclusion_date,
    sup_name,
    med_code,
    med_name,
    amount,
    price
FROM
    orders
    JOIN order_list USING (or_ID)
    JOIN suppliers ON (sup_id = sup_code)
    JOIN medicines ON (med_id = med_code)
WHERE
    conclusion_date = '$conclusion_date'