from typing import Dict

def get_mechanism_id_mapping() -> Dict[str, str]:
    """
    Central source of truth for mechanism name to ID mapping.

    Returns:
        Dict mapping mechanism names to their desired IDs
    """
    return {
        'MS1180': '1',
        'Portside CEMP': '2',
        'W6946/2024/1': '3'
    }

def get_reverse_mapping() -> Dict[str, str]:
    """
    Get reverse mapping from ID to original mechanism name.

    Returns:
        Dict mapping IDs to original mechanism names
    """
    return {v: k for k, v in get_mechanism_id_mapping().items()}
