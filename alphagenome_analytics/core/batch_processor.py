"""
Batch processing module for AlphaGenome Analytics.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
import pandas as pd

from .analyzer import VariantAnalyzer, VariantResult

logger = logging.getLogger(__name__)


class BatchProcessor:
    """
    Batch processing class for handling multiple variant predictions.
    """
    
    def __init__(self, analyzer: VariantAnalyzer, max_workers: int = 4):
        self.analyzer = analyzer
        self.max_workers = max_workers
        self.processed_count = 0
        self.error_count = 0
        self.results: List[VariantResult] = []
        self.errors: List[Dict[str, Any]] = []
        
    def process_variants(self, variants: List[Dict[str, Any]]) -> List[VariantResult]:
        """Process a list of variant dictionaries."""
        results = []
        for variant in variants:
            try:
                result = self.analyzer.predict_variant(
                    chromosome=variant['chromosome'],
                    position=variant['position'],
                    ref=variant['ref'], 
                    alt=variant['alt'],
                    metadata=variant.get('metadata', {})
                )
                results.append(result)
                self.processed_count += 1
            except Exception as e:
                self.error_count += 1
                self.errors.append({'variant': variant, 'error': str(e)})
        return results
    
    def save_results(self, results: List[VariantResult], output_path: Union[str, Path]) -> None:
        """Save results to file."""
        import json
        data = [result.to_dict() for result in results]
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics."""
        total = self.processed_count + self.error_count
        return {
            'total_variants': total,
            'successful': self.processed_count,
            'errors': self.error_count,
            'success_rate': self.processed_count / total if total > 0 else 0
        } 