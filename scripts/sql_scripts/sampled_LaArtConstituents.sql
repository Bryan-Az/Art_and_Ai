SELECT *
FROM constituents
EXCEPT
SELECT constituentid,
       ulanid,
       preferreddisplayname,
       forwarddisplayname,
       lastname,
       displaydate,
       artistofngaobject,
       beginyear,
       endyear,
       visualbrowsertimespan,
       nationality,
       visualbrowsernationality,
       constituenttype
FROM (SELECT *
      FROM constituents
      WHERE constituents.artistofngaobject = 1) a
INNER JOIN la_geographicStatistics
        ON a.nationality = la_geographicStatistics."Demonym"