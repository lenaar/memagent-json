import os
from .json_parser import load_json, save_json
from typing import Dict, Any

def create_folder(name: str):
    return os.makedirs(name, exist_ok=True)

def get_file_path(folder_path: str, file_name: str) -> str:
    return os.path.join(folder_path, file_name)

def load_json_file(folder_path: str, file_name: str):
    path = get_file_path(folder_path, file_name)
    return load_json(path)

def save_to_json_file(folder_path: str, file_name: str, data: Dict[str, Any]):
    path = get_file_path(folder_path, file_name)
    return save_json(path, data)