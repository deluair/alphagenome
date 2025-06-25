"""
File I/O utilities for AlphaGenome Analytics.
"""

import yaml
import json
import pickle
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def save_results(results: List[Any], output_path: Union[str, Path], format: str = 'json') -> None:
    """Save results to file."""
    if format == 'json':
        with open(output_path, 'w') as f:
            json.dump([r.to_dict() if hasattr(r, 'to_dict') else r for r in results], f, indent=2, default=str)
    elif format == 'pickle':
        with open(output_path, 'wb') as f:
            pickle.dump(results, f)

def load_vcf(vcf_path: Union[str, Path]) -> List[Dict[str, Any]]:
    """Load variants from VCF file (placeholder implementation)."""
    # This would require pysam or other VCF parser
    # For now, return empty list
    return [] 