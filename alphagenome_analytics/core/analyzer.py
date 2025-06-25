"""
Core variant analyzer module for AlphaGenome Analytics.

This module provides the main VariantAnalyzer class that serves as the
primary interface to AlphaGenome API with enhanced functionality.
"""

import logging
import time
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass

try:
    from alphagenome.data import genome
    from alphagenome.models import dna_client
    ALPHAGENOME_AVAILABLE = True
except ImportError:
    ALPHAGENOME_AVAILABLE = False

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


@dataclass
class VariantResult:
    """Container for variant analysis results."""
    chromosome: str
    position: int
    reference: str
    alternate: str
    predictions: Dict[str, Any]
    metadata: Dict[str, Any]
    timestamp: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format."""
        return {
            'chromosome': self.chromosome,
            'position': self.position,
            'reference': self.reference,
            'alternate': self.alternate,
            'predictions': self.predictions,
            'metadata': self.metadata,
            'timestamp': self.timestamp
        }


class VariantAnalyzer:
    """
    Main variant analyzer class that provides enhanced AlphaGenome functionality.
    
    This class serves as the primary interface for variant analysis, providing
    methods for single variant prediction, batch processing, and result management.
    
    Args:
        api_key: AlphaGenome API key
        rate_limit: Maximum requests per minute (default: 100)
        default_interval_size: Default genomic interval size (default: 1000000)
        cache_results: Whether to cache results (default: True)
    """
    
    def __init__(
        self,
        api_key: str,
        rate_limit: int = 100,
        default_interval_size: int = 1000000,
        cache_results: bool = True
    ):
        if not ALPHAGENOME_AVAILABLE:
            raise ImportError(
                "AlphaGenome package is required. Install with: pip install alphagenome"
            )
            
        self.api_key = api_key
        self.rate_limit = rate_limit
        self.default_interval_size = default_interval_size
        self.cache_results = cache_results
        
        # Initialize AlphaGenome client
        self.client = dna_client.create(api_key)
        
        # Internal state
        self._request_times = []
        self._cache: Dict[str, VariantResult] = {} if cache_results else {}
        
        logger.info(f"VariantAnalyzer initialized with rate limit: {rate_limit} req/min")
    
    def _check_rate_limit(self) -> None:
        """Check and enforce rate limiting."""
        current_time = time.time()
        
        # Remove requests older than 1 minute
        self._request_times = [
            t for t in self._request_times 
            if current_time - t < 60
        ]
        
        # Check if we're at the rate limit
        if len(self._request_times) >= self.rate_limit:
            sleep_time = 60 - (current_time - self._request_times[0])
            if sleep_time > 0:
                logger.warning(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
        
        self._request_times.append(current_time)
    
    def _create_cache_key(self, chromosome: str, position: int, ref: str, alt: str) -> str:
        """Create a cache key for variant."""
        return f"{chromosome}:{position}:{ref}:{alt}"
    
    def predict_variant(
        self,
        chromosome: str,
        position: int,
        ref: str,
        alt: str,
        interval_start: Optional[int] = None,
        interval_end: Optional[int] = None,
        ontology_terms: Optional[List[str]] = None,
        requested_outputs: Optional[List[Any]] = None,
        gene_context: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> VariantResult:
        """
        Predict the effects of a single variant.
        
        Args:
            chromosome: Chromosome name (e.g., 'chr1', 'chrX')
            position: Genomic position (1-based)
            ref: Reference allele
            alt: Alternate allele
            interval_start: Start of analysis interval (default: auto-calculate)
            interval_end: End of analysis interval (default: auto-calculate)
            ontology_terms: List of ontology terms to include
            requested_outputs: Specific outputs to request
            gene_context: Whether to include gene context information
            metadata: Additional metadata to store
            
        Returns:
            VariantResult object containing predictions and metadata
        """
        # Check cache
        cache_key = self._create_cache_key(chromosome, position, ref, alt)
        if self.cache_results and cache_key in self._cache:
            logger.debug(f"Returning cached result for {cache_key}")
            return self._cache[cache_key]
        
        # Rate limiting
        self._check_rate_limit()
        
        # Calculate interval if not provided
        if interval_start is None or interval_end is None:
            center = position
            half_size = self.default_interval_size // 2
            interval_start = max(1, center - half_size)
            interval_end = center + half_size
        
        # Create genomic objects
        interval = genome.Interval(
            chromosome=chromosome,
            start=interval_start,
            end=interval_end
        )
        
        variant = genome.Variant(
            chromosome=chromosome,
            position=position,
            reference_bases=ref,
            alternate_bases=alt
        )
        
        # Set default parameters
        if ontology_terms is None:
            ontology_terms = ['UBERON:0001157']  # anatomical system
            
        if requested_outputs is None:
            requested_outputs = [
                dna_client.OutputType.RNA_SEQ,
                dna_client.OutputType.CAGE,
                dna_client.OutputType.DNASE
            ]
        
        try:
            # Make prediction
            logger.debug(f"Predicting variant {cache_key}")
            outputs = self.client.predict_variant(
                interval=interval,
                variant=variant,
                ontology_terms=ontology_terms,
                requested_outputs=requested_outputs
            )
            
            # Process results
            predictions = self._process_outputs(outputs)
            
            # Create result object
            result = VariantResult(
                chromosome=chromosome,
                position=position,
                reference=ref,
                alternate=alt,
                predictions=predictions,
                metadata=metadata or {},
                timestamp=time.time()
            )
            
            # Cache result
            if self.cache_results:
                self._cache[cache_key] = result
            
            logger.info(f"Successfully predicted variant {cache_key}")
            return result
            
        except Exception as e:
            logger.error(f"Error predicting variant {cache_key}: {str(e)}")
            raise
    
    def _process_outputs(self, outputs: Any) -> Dict[str, Any]:
        """
        Process AlphaGenome outputs into a standardized format.
        
        Args:
            outputs: Raw AlphaGenome outputs
            
        Returns:
            Dictionary of processed predictions
        """
        predictions = {}
        
        try:
            # Process RNA-seq data
            if hasattr(outputs, 'reference') and hasattr(outputs.reference, 'rna_seq'):
                rna_ref = outputs.reference.rna_seq
                rna_alt = outputs.alternate.rna_seq if hasattr(outputs, 'alternate') else None
                
                predictions['rna_seq'] = {
                    'reference': self._extract_track_data(rna_ref),
                    'alternate': self._extract_track_data(rna_alt) if rna_alt else None,
                    'difference': self._calculate_difference(rna_ref, rna_alt) if rna_alt else None
                }
            
            # Process CAGE data
            if hasattr(outputs, 'reference') and hasattr(outputs.reference, 'cage'):
                cage_ref = outputs.reference.cage
                cage_alt = outputs.alternate.cage if hasattr(outputs, 'alternate') else None
                
                predictions['cage'] = {
                    'reference': self._extract_track_data(cage_ref),
                    'alternate': self._extract_track_data(cage_alt) if cage_alt else None,
                    'difference': self._calculate_difference(cage_ref, cage_alt) if cage_alt else None
                }
            
            # Process DNase data
            if hasattr(outputs, 'reference') and hasattr(outputs.reference, 'dnase'):
                dnase_ref = outputs.reference.dnase
                dnase_alt = outputs.alternate.dnase if hasattr(outputs, 'alternate') else None
                
                predictions['dnase'] = {
                    'reference': self._extract_track_data(dnase_ref),
                    'alternate': self._extract_track_data(dnase_alt) if dnase_alt else None,
                    'difference': self._calculate_difference(dnase_ref, dnase_alt) if dnase_alt else None
                }
                
        except Exception as e:
            logger.warning(f"Error processing outputs: {str(e)}")
            predictions['raw'] = str(outputs)
        
        return predictions
    
    def _extract_track_data(self, track: Any) -> Optional[Dict[str, Any]]:
        """Extract data from a genomic track."""
        if track is None:
            return None
            
        try:
            # Convert to numpy array if possible
            if hasattr(track, 'values'):
                values = np.array(track.values)
            elif hasattr(track, 'data'):
                values = np.array(track.data)
            else:
                values = np.array(track)
            
            return {
                'values': values.tolist(),
                'length': len(values),
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'max': float(np.max(values)),
                'min': float(np.min(values))
            }
        except Exception as e:
            logger.warning(f"Could not extract track data: {str(e)}")
            return {'raw': str(track)}
    
    def _calculate_difference(self, ref_track: Any, alt_track: Any) -> Optional[Dict[str, Any]]:
        """Calculate difference between reference and alternate tracks."""
        try:
            ref_data = self._extract_track_data(ref_track)
            alt_data = self._extract_track_data(alt_track)
            
            if ref_data is None or alt_data is None:
                return None
            
            ref_values = np.array(ref_data['values'])
            alt_values = np.array(alt_data['values'])
            
            if len(ref_values) != len(alt_values):
                logger.warning("Reference and alternate tracks have different lengths")
                return None
            
            diff = alt_values - ref_values
            
            return {
                'values': diff.tolist(),
                'mean_difference': float(np.mean(diff)),
                'max_difference': float(np.max(np.abs(diff))),
                'total_effect': float(np.sum(np.abs(diff))),
                'correlation': float(np.corrcoef(ref_values, alt_values)[0, 1])
            }
            
        except Exception as e:
            logger.warning(f"Could not calculate difference: {str(e)}")
            return None
    
    def get_cache_stats(self) -> Dict[str, Union[bool, int, float]]:
        """Get cache statistics."""
        if not self.cache_results:
            return {"cache_enabled": False}
        
        return {
            "cache_enabled": True,
            "cached_variants": len(self._cache),
            "cache_size_mb": sum(len(str(v)) for v in self._cache.values()) / (1024 * 1024)
        }
    
    def clear_cache(self) -> None:
        """Clear the variant cache."""
        if self.cache_results:
            self._cache.clear()
            logger.info("Variant cache cleared")
    
    def export_cache(self, filepath: str) -> None:
        """Export cache to file."""
        if not self.cache_results or not self._cache:
            logger.warning("No cache to export")
            return
        
        import pickle
        with open(filepath, 'wb') as f:
            pickle.dump(self._cache, f)
        logger.info(f"Cache exported to {filepath}")
    
    def import_cache(self, filepath: str) -> None:
        """Import cache from file."""
        if not self.cache_results:
            logger.warning("Cache is disabled")
            return
        
        import pickle
        try:
            with open(filepath, 'rb') as f:
                self._cache = pickle.load(f)
            logger.info(f"Cache imported from {filepath}")
        except Exception as e:
            logger.error(f"Failed to import cache: {str(e)}")
            raise 