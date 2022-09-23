from typing import List

def dict_to_tuples(dict: dict) -> List[tuple]:
    keys = list(dict.keys())
    values = list(dict.values())
    
    result = [(key, dict[key]) for key in keys]
    
    return result
