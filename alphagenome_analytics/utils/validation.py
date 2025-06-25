"""
Validation utilities for AlphaGenome Analytics.
"""

import re
from typing import Dict, Any, Tuple, Optional

def validate_variant(chromosome: str, position: int, ref: str, alt: str) -> Tuple[bool, Optional[str]]:
    """Validate a variant specification."""
    # Check chromosome format
    if not re.match(r'^chr[0-9XYM]+$', chromosome):
        return False, f"Invalid chromosome format: {chromosome}"
    
    # Check position
    if position <= 0:
        return False, f"Position must be positive: {position}"
    
    # Check alleles
    if not re.match(r'^[ATCG]+$', ref.upper()):
        return False, f"Invalid reference allele: {ref}"
    
    if not re.match(r'^[ATCG]+$', alt.upper()):
        return False, f"Invalid alternate allele: {alt}"
    
    return True, None

def validate_interval(chromosome: str, start: int, end: int) -> Tuple[bool, Optional[str]]:
    """Validate a genomic interval."""
    # Check chromosome format
    if not re.match(r'^chr[0-9XYM]+$', chromosome):
        return False, f"Invalid chromosome format: {chromosome}"
    
    # Check coordinates
    if start <= 0:
        return False, f"Start position must be positive: {start}"
    
    if end <= start:
        return False, f"End position must be greater than start: {end} <= {start}"
    
    return True, None 