SELECT
    r.*,
    CASE WHEN f.full_moon_date IS NOT NULL THEN true ELSE false END AS is_full_moon_night
FROM {{ source('bronze', 'bronze_reviews') }} r
LEFT JOIN {{ source('bronze', 'bronze_full_moon') }} f
    ON CAST(r.date AS DATE) = f.full_moon_date