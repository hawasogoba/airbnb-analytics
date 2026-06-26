SELECT
    host_id,
    COUNT(*) AS nb_listings
FROM {{ ref('silver_listings') }}
GROUP BY host_id
ORDER BY nb_listings DESC