import os
from dataclasses import dataclass
import requests 
import hashlib
import shutil
from zipfile import ZipFile
import hashlib


@dataclass
class Configuration:
    link: str = "https://github.com/DeepSportRadar/player-reidentification-challenge/archive/refs/heads/master.zip"
    # md5: str = '05715857791e2e88b2f11e4037fbec7d'
    md5: str = '2a1cdbd10d2b8f0da6575e3581343e31'
    path: str = "./data"
    

def download_zip(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


#----------------------------------------------------------------------------------------------------------------------#  
# Config                                                                                                               #
#----------------------------------------------------------------------------------------------------------------------# 
config = Configuration()

#----------------------------------------------------------------------------------------------------------------------#  
# Download                                                                                                             #
#----------------------------------------------------------------------------------------------------------------------#
if not os.path.exists(config.path):
    os.makedirs(config.path) 

with open('./data/synergyreid_data.zip', 'rb') as f:
    file_md5 = hashlib.md5(f.read()).hexdigest()
    print(f"Calculated MD5: {file_md5}")
    print(f"Expected MD5: {config.md5}")

# only download if data zip is missing
if not os.path.isfile("{}/synergyreid_data.zip".format(config.path)):

    # download gihub repo
    download_zip(url=config.link,
                 save_path="{}/reid_challenge.zip".format(config.path),
                 chunk_size=128)

    # unzip only reid_challenge.zip
    path_in_zip = "player-reidentification-challenge-master/baseline/data/synergyreid/raw/synergyreid_data.zip"
         
    with ZipFile("{}/reid_challenge.zip".format(config.path)) as z:

        z.extract(path_in_zip,
                  config.path)
        
    shutil.move("{}/{}".format(config.path, path_in_zip), "{}/synergyreid_data.zip".format(config.path))
    
    # cleanup
    shutil.rmtree("{}/player-reidentification-challenge-master".format(config.path)) 
    os.remove("{}/reid_challenge.zip".format(config.path))


#----------------------------------------------------------------------------------------------------------------------#  
# Unzip                                                                                                                #
#----------------------------------------------------------------------------------------------------------------------#  

zip_file = "{}/synergyreid_data.zip".format(config.path)
      
if os.path.isfile(zip_file) and hashlib.md5(open(zip_file, 'rb').read()).hexdigest() == config.md5:
    print("Using downloaded file: " + zip_file)
    
    if not os.path.exists(config.path):
        os.makedirs(config.path)

    # Extract the file
    print("Extracting zip file")
    with ZipFile(zip_file) as z:
        z.extractall(path=config.path)
