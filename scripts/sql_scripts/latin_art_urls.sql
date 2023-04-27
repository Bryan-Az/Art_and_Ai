/*
   The output of this query is the second file containing all information in latin_art_people,      and adds more columns like urls and digital info in published_images. 
*/
SELECT uuid,
iiifurl,
iiifthumburl,
viewtype,
sequence,
width,
height,
maxpixels,
assistivetext,
depictstmsobjectid,
objectid,
constituentid,
roletype,
`role`,
birthyear,
deathyear,
displaydate_artistAssigned,
beginyear_artistAssigned,
endyear_artistAssigned,
country_artistAssigned,
zipcode_artistAssigned,
ulanid,
forwarddisplayname,
artistofngaobject,
nationality,
constituenttype,
demonym,
pct_country_NGA,
artists_countryCode,
artists_continent,
artists_country
FROM published_images
INNER JOIN latin_art_people
ON published_images.depictstmsobjectid = latin_art_people.objectid
