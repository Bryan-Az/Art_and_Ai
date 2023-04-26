/* The output of this query is the first file containing relevent information about the artwork (physical and digital),
    and the artist. (object constituents (link rels b/w art and artists) + constituents (artist info) + L.A. geo details (stats))
    
    P.S.
    Some columns were not selected to avoid memory usage.
    
    constituents table may filter relationships more using constituentType column (the same artwork will be matched to groups of people if the 'individual' constituentType is not selected - leading to many row data for a single url/artwork).
    
    object_constituents table may filter relationships more than 'artistofNGAobject' column does in constituents using the roleType col. roleType filters based on types of artist (painter, publisher, author, etc.)
    
    Reduction possible by including an extra where key in the object_constituents select using these columns.
    
*/
SELECT objectid,
b.constituentid,
roletype,
role,
displaydate as displaydate_artMade,
beginyear as beginyear_artMade,
endyear as endyear_artMade,
b.country as country_artMade,
zipcode as zipcode_artMade,
ulanid,
forwarddisplayname,
artistofngaobject,
beginyear,
endyear, 
nationality,
constituenttype,
Demonym as demonym,
pct_country_NGA,
countryCode as artists_countryCode,
Continent as artists_continent,
`Country Name` as artists_country
FROM objects_constituents as b
INNER JOIN (
    SELECT *
    FROM (SELECT *
          FROM constituents
          WHERE constituents.artistofngaobject = 1) a
    INNER JOIN la_geographicStatistics
    ON a.nationality = la_geographicStatistics.Demonym) x
ON b.constituentid = x.constituentid