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
displaydate_linkMade,
beginyear_artMade,
endyear_artMade,
country_artMade,
zipcode_artMade,
ulanid,
forwarddisplayname,
artistofngaobject,
beginyear,
endyear,
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