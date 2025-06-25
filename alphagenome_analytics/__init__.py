"""
AlphaGenome Analytics: A comprehensive genomic variant analysis toolkit
built on top of Google DeepMind's AlphaGenome API.

This package provides tools for:
- Batch variant analysis
- Advanced visualization
- Statistical analysis
- Report generation
- Data management
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__license__ = "MIT"

# Core imports (simplified for initial testing)
try:
    from .core.analyzer import VariantAnalyzer
    from .core.batch_processor import BatchProcessor
    from .core.data_manager import DataManager
except ImportError as e:
    # Fallback for development
    VariantAnalyzer = None
    BatchProcessor = None
    DataManager = None

# Utility functions
try:
    from .utils.file_io import load_config
    from .utils.validation import validate_variant, validate_interval
except ImportError:
    pass

__all__ = [
    # Core classes
    "VariantAnalyzer",
    "BatchProcessor", 
    "DataManager",
    
    # Analysis classes
    "PathogenicityAnalyzer",
    "PopulationAnalyzer",
    "ClinicalInterpreter",
    
    # Visualization classes
    "GenomicPlotter",
    "StatisticalPlotter",
    "InteractiveDashboard",
    
    # Utility functions
    "load_vcf",
    "save_results",
    "load_config",
    "validate_variant",
    "validate_interval",
    "calculate_effect_sizes",
    "enrichment_analysis",
    
    # Metadata
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]

# Configure logging
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Version check
import sys
if sys.version_info < (3, 8):
    raise RuntimeError("AlphaGenome Analytics requires Python 3.8 or later")

# Optional dependency warnings
try:
    import alphagenome
except ImportError:
    import warnings
    warnings.warn(
        "AlphaGenome package not found. Please install it with: "
        "pip install alphagenome",
        ImportWarning
    ) 