SELECT
    role
FROM
    users
WHERE
    username = '$login'
    AND password = '$password'