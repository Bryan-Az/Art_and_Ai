SELECT *
FROM published_images
INNER JOIN nonLA_artists_works
ON published_images.depictstmsobjectid = nonLA_artists_works.objectid