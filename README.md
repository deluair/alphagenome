# AlphaGenome Analytics

A genomic variant analysis toolkit built on top of Google DeepMind's AlphaGenome API. This project provides tools for batch processing, visualization, and analysis of genomic variant predictions.

## Features

- **Batch Variant Analysis**: Process multiple variants efficiently
- **Visualizations**: Interactive plots and genomic views
- **Statistical Analysis**: Variant effect statistics and significance testing
- **Report Generation**: Automated HTML/PDF reports
- **Data Management**: Storage and retrieval of prediction results
- **Quality Control**: Built-in validation and filtering tools

## Installation

```bash
git clone https://github.com/deluair/alphagenome.git
cd alphagenome
pip install -e .

# Install AlphaGenome API package
pip install alphagenome

# Install optional dependencies
pip install python-dotenv pysam matplotlib plotly
```

## Quick Start

### 1. Set Up Your API Key
Create a `.env` file in the project root:
```bash
cp .env.example .env
# Edit .env with your API key
ALPHAGENOME_API_KEY=your_api_key_here
```

### 2. Analyze Variants
```python
import os
from alphagenome_analytics.core.analyzer import VariantAnalyzer

# Initialize analyzer
api_key = os.getenv('ALPHAGENOME_API_KEY')
analyzer = VariantAnalyzer(api_key=api_key)

# Analyze a variant
result = analyzer.predict_variant(
    chromosome="chr17",
    position=43044295,
    ref="G",
    alt="A",
    gene_context=True,
    metadata={"gene": "BRCA1", "type": "missense"}
)

print(f"Variant: {result.chromosome}:{result.position}{result.reference}>{result.alternate}")
print(f"Predictions available: {list(result.predictions.keys())}")
```

### 3. Batch Processing
```python
from alphagenome_analytics.core.batch_processor import BatchProcessor

# Initialize batch processor
processor = BatchProcessor(analyzer)

# Define multiple variants
variants = [
    {"chromosome": "chr1", "position": 230710048, "ref": "A", "alt": "G", 
     "metadata": {"gene": "AGT", "rsid": "rs699"}},
    {"chromosome": "chr7", "position": 117548628, "ref": "C", "alt": "T",
     "metadata": {"gene": "CFTR", "rsid": "rs1042880"}},
]

# Process variants
results = processor.process_variants(variants)
print(f"Processed {len(results)} variants")

# Save results
processor.save_results(results, "batch_results.json")
```

## Configuration

Create a configuration file `config.yaml`:

```yaml
api:
  key: "your_alphagenome_api_key"
  rate_limit: 100
  
analysis:
  default_interval_size: 1000000
  min_effect_threshold: 0.1
  
output:
  base_directory: "./results"
  include_raw_data: true
```

## Project Structure

```
alphagenome-analytics/
├── alphagenome_analytics/           # Main package
│   ├── core/                        # Core analysis modules
│   │   ├── analyzer.py              # Main VariantAnalyzer class
│   │   ├── batch_processor.py       # Batch processing utilities
│   │   └── data_manager.py          # Data storage and retrieval
│   ├── analysis/                    # Specialized analysis modules
│   ├── visualization/               # Visualization tools
│   └── utils/                       # Utility functions
├── scripts/                         # Analysis scripts
├── tests/                           # Test suite
├── examples/                        # Example notebooks
└── docs/                           # Documentation
```

## Status

### Completed
- Core variant analysis framework with AlphaGenome API integration
- Batch processing capabilities with error handling
- Environment-based API key management
- Comprehensive validation utilities for genomic data
- Configurable caching and rate limiting
- Professional package structure with proper imports

### In Development
- Advanced visualization modules
- Statistical analysis and enrichment tools
- VCF file processing
- Interactive dashboards and web interface
- Population genomics and pathogenicity analysis

## License

MIT License

## Requirements

- Python 3.8 or higher
- AlphaGenome API key
