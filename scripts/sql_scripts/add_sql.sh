#! /bin/bash
#the SQL scripts in the 'create_schema' and 'insert_data' zips were created running MySQL>=8.0 DB
#the "la_art_tables" zip will be placed into the data_samples/LaArt directory to be used by the add_LaArt.sh script since it has CSV and is a data sample

mv la_art_tables.zip ../../data_samples/LaArt
unzip ../../data_samples/LaArt/la_art_tables.zip -d ../../data_samples/LaArt/

#these are used in the db
#assumes zip package installed on ubuntu
unzip ./create_schema.zip
unzip ./insert_data.zip
unzip ./query_tables.zip