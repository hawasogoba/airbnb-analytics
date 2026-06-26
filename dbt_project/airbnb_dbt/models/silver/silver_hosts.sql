SELECT *
FROM {{ source('bronze', 'bronze_hosts') }}
WHERE id IS NOT NULL