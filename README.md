# Latin American Art & A.I 
Hello! Welcome to my work-in-progress project, where I am using Machine Learning to understand Latin American Art (Open-Source) from the National Gallery of Art (NGA). The NGA did not endorse or sponsor this work. This project is fully for educational & research purposes. 

Keywords: Style Transfer/Interpolation, text-to-image generation. 

To unpack the data and the models:
1. Scripts are stored in the Art_and_Ai/scripts directory, where exists:
    a. The bash script in the source_sql directory which runs code that:
         I.  Sets the project working directory.
         II. Unpacks the SQL scripts (for later use).
         III. Moves the CSV data into the data_sample directory.
    b. The bash script runs the python which extract, download, and clean & prepare the data.
         I. The two pipelines are separated into the LaArt/NonLaArt directories.
         II. Each pipeline has code that Extracts/Transforms the data for use by Pytorch later.
         III. Differences exist between the code that operates on (e.g. differences in the size of data, feature generation requiring independent supervision in either) however both produce similar datasets and both will be used by the model.
