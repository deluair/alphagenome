# Getting Started with AlphaGenome Analytics

Welcome to **AlphaGenome Analytics** - a comprehensive genomic variant analysis toolkit built on top of Google DeepMind's AlphaGenome API!

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- AlphaGenome API key from [AlphaGenome website](https://www.alphagenomedocs.com)

### 2. Installation

```bash
# Clone the repository
git clone <your-repository-url>
cd alphagenome-analytics

# Install the package in development mode
pip install -e .

# Install the AlphaGenome package
pip install alphagenome

# (Optional) Install additional dependencies for full functionality
pip install python-dotenv pysam
```

### 3. API Key Configuration

Your AlphaGenome API key is already configured in the `.env` file:

```
ALPHAGENOME_API_KEY=AIzaSyBxLoHZ8xDGllhqJalho9bM3FLUBQVjZhA
```

> ⚠️ **Security Note**: The `.env` file containing your API key is ignored by Git to prevent accidental commits to version control.

### 4. Test Your Setup

Run the setup test to verify everything is working:

```bash
python test_setup.py
```

This will check:
- ✅ Package imports
- ✅ API key configuration
- ✅ Validation functions
- ✅ Core functionality

## 📊 Basic Usage Examples

### Analyze a Single Variant

```python
from alphagenome_analytics import VariantAnalyzer

# Initialize with your API key (loaded from environment)
analyzer = VariantAnalyzer(api_key="your_api_key")

# Analyze a variant
result = analyzer.predict_variant(
    chromosome="chr17",
    position=43044295,  # BRCA1 region
    ref="G",
    alt="A",
    gene_context=True
)

print(f"Predictions: {list(result.predictions.keys())}")
```

### Batch Process Multiple Variants

```python
from alphagenome_analytics import VariantAnalyzer, BatchProcessor

# Initialize
analyzer = VariantAnalyzer(api_key="your_api_key")
processor = BatchProcessor(analyzer)

# Define variants
variants = [
    {"chromosome": "chr1", "position": 230710048, "ref": "A", "alt": "G"},
    {"chromosome": "chr7", "position": 117548628, "ref": "C", "alt": "T"},
    {"chromosome": "chr19", "position": 11201138, "ref": "T", "alt": "C"}
]

# Process variants
results = processor.process_variants(variants)
print(f"Processed {len(results)} variants")
```

### Process VCF Files

```python
# Process variants from a VCF file
results = processor.process_vcf(
    vcf_path="my_variants.vcf",
    output_path="results.json",
    max_variants=100  # Limit for testing
)
```

## 🛠️ Available Tools

### Core Modules
- **`VariantAnalyzer`**: Main interface for variant predictions
- **`BatchProcessor`**: Handle multiple variants efficiently  
- **`DataManager`**: Store and retrieve analysis results

### Analysis Modules
- **`PathogenicityAnalyzer`**: Assess variant pathogenicity
- **`PopulationAnalyzer`**: Population genomics analysis
- **`ClinicalInterpreter`**: Clinical interpretation tools

### Visualization Tools
- **`GenomicPlotter`**: Genomic visualization functions
- **`StatisticalPlotter`**: Statistical analysis plots
- **`InteractiveDashboard`**: Interactive web dashboards

### Utilities
- **File I/O**: VCF loading, result saving, configuration
- **Validation**: Variant and interval validation
- **Statistics**: Effect size calculation, enrichment analysis

## 📝 Example Scripts

### Run the Demo Analysis

```bash
# Run with your API key
python scripts/example_analysis.py --api-key YOUR_KEY

# Or run without API calls for testing
python scripts/example_analysis.py --no-api --output demo/
```

### Command Line Tools

The package includes several command-line tools:

```bash
# Analyze variants (coming soon)
alphagenome-analyze --vcf input.vcf --output results/

# Batch processing (coming soon)  
alphagenome-batch --input variants.txt --workers 4

# Generate visualizations (coming soon)
alphagenome-visualize --results results.json --output plots/
```

## 🔧 Configuration

### Environment Variables
- `ALPHAGENOME_API_KEY`: Your API key (required)
- `ALPHAGENOME_RATE_LIMIT`: API rate limit (default: 100 req/min)
- `DEFAULT_INTERVAL_SIZE`: Default genomic interval size
- `OUTPUT_BASE_DIR`: Base directory for results

### Configuration File
Customize analysis settings in `config.yaml`:

```yaml
api:
  rate_limit: 100

analysis:
  default_interval_size: 1000000
  min_effect_threshold: 0.1
  cache_results: true

visualization:
  default_format: "html"
  color_scheme: "viridis"

output:
  base_directory: "./results"
  include_raw_data: true
```

## 📚 Next Steps

1. **Explore Examples**: Check out the `examples/` directory for Jupyter notebooks
2. **Read Documentation**: Visit the `docs/` directory for detailed guides
3. **Join the Community**: Participate in discussions and report issues
4. **Contribute**: See `CONTRIBUTING.md` for contribution guidelines

## 🆘 Troubleshooting

### Common Issues

**Import Errors**: Make sure you've installed the package with `pip install -e .`

**API Key Issues**: Verify your `.env` file contains the correct API key

**Rate Limiting**: Reduce the rate limit in your configuration if you encounter API limits

**Missing Dependencies**: Install optional dependencies based on your use case:
```bash
pip install python-dotenv pysam plotly dash
```

### Get Help

- 📧 Email: support@alphagenome-analytics.org  
- 💬 GitHub Discussions: [Project Discussions](https://github.com/your-username/alphagenome-analytics/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/alphagenome-analytics/issues)

---

**Happy analyzing! 🧬✨** 