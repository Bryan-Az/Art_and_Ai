SELECT *
FROM objects_constituents
INNER JOIN (
    SELECT *
    FROM (SELECT *
          FROM constituents
          WHERE constituents.artistofngaobject = 1) a
    INNER JOIN latin_in_nga
    ON a.nationality = latin_in_nga."Demonym") x
ON objects_constituents.constituentid = x.constituentid