import pandas as pd
import shutil
import requests
import time

# data to download LA art / contains path to place images into
verified_la = pd.read_csv('../../data_samples/results/whole_set_results/downloaded_LaArt.csv')
# code which downloads the images & places them into directory


def download_image(url, path, name, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(name, "wb") as f:
            f.write(response.content)
        shutil.move(name, path)
    else:
        print(response.status_code)


# Define HTTP Headers
ua_header = {
    "User-Agent": "Chrome/51.0.2704.103",
}
# This block iterates over all the images
for i in range(0, len(verified_la)):
    # Define URL of an image
    expanded_url = verified_la.expanded_url[i]
    # Define image file name, file path to place
    file_name = verified_la.file_name[i]
    fp = verified_la.image_fp[i]
    # Download image
    # timer delay (15 seconds)
    time.sleep(15)
    download_image(expanded_url, fp, file_name, ua_header)