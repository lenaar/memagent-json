import json
import os
from typing import Optional, Dict, Any

def load_json(path: str):
    if not os.path.exists(path):
        return None
    
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {path}: {e}")
        return None
    
def save_json(path: str, data: Dict[str, Any]):
    try:
        with open(path, "w") as f:
            json.dump(data, f,  indent=2)
    except Exception as e:
        print(f"Error saving JSON file {path}: {e}")
        return None
    
