SELECT *
FROM objects_constituents
INNER JOIN (
    SELECT *
    FROM (SELECT *
          FROM constituents
          WHERE constituents.artistofngaobject = 1) a
    INNER JOIN la_geographicStatistics
    ON a.nationality = la_geographicStatistics."Demonym") x
ON objects_constituents.constituentid = x.constituentid