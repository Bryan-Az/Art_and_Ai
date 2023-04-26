SELECT objectid,
b.constituentid,
displayorder,
roletype,
role,
prefix,
suffix,
displaydate as displaydate_linkMade,
beginyear as beginyear_linkMade,
endyear as endyear_linkMade,
b.country as country_linkMade,
zipcode,
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
constituenttype,
Demonym,
pct_country_NGA,
countryCode,
Continent,
`Country Name`
FROM objects_constituents as b
INNER JOIN (
    SELECT *
    FROM (SELECT *
          FROM constituents
          WHERE constituents.artistofngaobject = 1) a
    INNER JOIN la_geographicStatistics
    ON a.nationality = la_geographicStatistics.Demonym) x
ON b.constituentid = x.constituentid