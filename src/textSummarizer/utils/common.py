import os
from box.exceptions  import BoxValueError #pip install "python-box[all]~=7.0" --upgrade
import yaml #pip install pyyaml~=6.0 --upgrade
from textSummarizer.logging import logger
from ensure import ensure_annotations #pip install ensure~=0.0.3 --upgrade
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def get_file_path():
    cwd = os.getcwd()  
    files = os.listdir(cwd)  
    print("Files in %r: %s" % (cwd, files))
    print("test")

@ensure_annotations
def read_yaml(path_to_yaml:Path) -> ConfigBox:
    try:       
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully.")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")    
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories=list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def get_size(path: Path) -> str:
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"