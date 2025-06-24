import os
import urllib.request as request
import zipfile
from textSummarizer.logging import logger
from textSummarizer.utils.common import get_size
from urllib.error import HTTPError, URLError
from pathlib import Path
from textSummarizer.entity import (DataIngestionConfig)

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        # try:
            if not os.path.exists(self.config.local_data_file):
                # print(self.config.source_URL)
                filename,headers = request.urlretrieve(url = self.config.source_URL, filename=self.config.local_data_file)
                logger.info(f"{filename} download! with following info: \n{headers}")
            else:
                logger.info(f"File {Path(self.config.local_data_file)} already exists of size {get_size(Path(self.config.local_data_file))}")
        # except HTTPError as e:
        #     if e.code == 404:
        #         print(f"HTTP Error 404: The requested resource at {url} was not found.")
        #     else:
        #         print(f"HTTP Error {e.code}: {e.reason} for URL: {url}")
        # except URLError as e:
        #     print(f"URL Error: {e.reason} for URL: {url}")
        # except Exception as e:
        #     print(f"An unexpected error occurred: {e}")

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
            logger.info(f"Extracted all the files to {unzip_path}")
    def download_extract_zip_file(self):
        zip_path, _ = request.urlretrieve(self.config.source_URL)
        logger.info(f"{zip_path} download! with following info:")
        with zipfile.ZipFile(zip_path, "r") as f:
            f.extractall(self.config.unzip_dir)   
