#!/usr/bin/env python3
"""
Example analysis script for AlphaGenome Analytics.

This script demonstrates how to use the toolkit for variant analysis
with a simple example workflow.
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add the package to path for development
sys.path.insert(0, str(Path(__file__).parent.parent))

from alphagenome_analytics import VariantAnalyzer, BatchProcessor
from alphagenome_analytics.visualization import GenomicPlotter
from alphagenome_analytics.utils import load_config


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('alphagenome_analysis.log')
        ]
    )


def analyze_single_variant(api_key: str, output_dir: Path) -> None:
    """Analyze a single variant example."""
    print("🧬 Analyzing single variant...")
    
    # Initialize analyzer
    analyzer = VariantAnalyzer(api_key=api_key)
    
    # Example variant from BRCA1 gene region
    try:
        result = analyzer.predict_variant(
            chromosome="chr17",
            position=43044295,  # Common BRCA1 variant
            ref="G",
            alt="A",
            gene_context=True,
            metadata={"gene": "BRCA1", "consequence": "missense"}
        )
        
        print(f"✅ Successfully analyzed variant: {result.chromosome}:{result.position}{result.reference}>{result.alternate}")
        print(f"   Predictions available: {list(result.predictions.keys())}")
        
        # Save result
        output_file = output_dir / "single_variant_result.json"
        import json
        with open(output_file, 'w') as f:
            json.dump(result.to_dict(), f, indent=2, default=str)
        print(f"   Result saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error analyzing variant: {str(e)}")
        if "API key" in str(e):
            print("   Make sure you have a valid AlphaGenome API key")


def analyze_variant_list(api_key: str, output_dir: Path) -> None:
    """Analyze a list of variants."""
    print("\n🧬 Analyzing multiple variants...")
    
    # Example variants for demonstration
    variants = [
        {
            "chromosome": "chr1", "position": 230710048, "ref": "A", "alt": "G",
            "metadata": {"gene": "AGT", "rsid": "rs699"}
        },
        {
            "chromosome": "chr7", "position": 117548628, "ref": "C", "alt": "T", 
            "metadata": {"gene": "CFTR", "rsid": "rs1042880"}
        },
        {
            "chromosome": "chr19", "position": 11201138, "ref": "T", "alt": "C",
            "metadata": {"gene": "LDLR", "rsid": "rs6511720"}
        }
    ]
    
    try:
        # Initialize analyzer and batch processor
        analyzer = VariantAnalyzer(api_key=api_key, rate_limit=50)  # Lower rate for demo
        processor = BatchProcessor(analyzer, max_workers=2)
        
        # Process variants
        results = processor.process_variants(variants, show_progress=True)
        
        print(f"✅ Successfully processed {len(results)} variants")
        
        # Save results
        output_file = output_dir / "batch_results.json"
        processor.save_results(results, output_file, format='json')
        print(f"   Results saved to: {output_file}")
        
        # Show summary stats
        stats = processor.get_summary_stats()
        print(f"   Success rate: {stats['success_rate']:.1%}")
        
    except Exception as e:
        print(f"❌ Error in batch processing: {str(e)}")


def generate_visualization(output_dir: Path) -> None:
    """Generate example visualizations."""
    print("\n📊 Generating example visualizations...")
    
    try:
        # Create sample data for visualization
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Example: Variant effect heatmap
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Mock RNA-seq effect data
        positions = np.arange(1000)
        ref_signal = np.random.normal(1.0, 0.3, 1000)
        alt_signal = ref_signal + np.random.normal(0, 0.1, 1000)
        alt_signal[450:550] += 0.8  # Add effect region
        
        ax1.plot(positions, ref_signal, label='Reference', alpha=0.7, color='blue')
        ax1.plot(positions, alt_signal, label='Alternate', alpha=0.7, color='red')
        ax1.axvline(x=500, color='black', linestyle='--', alpha=0.5, label='Variant')
        ax1.set_xlabel('Genomic Position (relative)')
        ax1.set_ylabel('RNA-seq Signal')
        ax1.set_title('Predicted RNA-seq Changes')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Effect difference
        diff = alt_signal - ref_signal
        ax2.bar(positions, diff, alpha=0.6, color='green', width=1)
        ax2.axvline(x=500, color='black', linestyle='--', alpha=0.5, label='Variant')
        ax2.set_xlabel('Genomic Position (relative)')
        ax2.set_ylabel('Effect Size (Alt - Ref)')
        ax2.set_title('Variant Effect Profile')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Save visualization
        viz_file = output_dir / "example_visualization.png"
        plt.savefig(viz_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Visualization saved to: {viz_file}")
        
    except Exception as e:
        print(f"❌ Error generating visualization: {str(e)}")


def create_sample_config(output_dir: Path) -> None:
    """Create a sample configuration file."""
    print("\n⚙️  Creating sample configuration...")
    
    config = {
        "api": {
            "key": "your_alphagenome_api_key_here",
            "rate_limit": 100
        },
        "analysis": {
            "default_interval_size": 1000000,
            "min_effect_threshold": 0.1,
            "cache_results": True
        },
        "visualization": {
            "default_format": "html",
            "color_scheme": "viridis",
            "figure_size": [12, 8]
        },
        "output": {
            "base_directory": "./results",
            "include_raw_data": True,
            "compression": "gzip"
        }
    }
    
    import yaml
    config_file = output_dir / "config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print(f"✅ Sample configuration saved to: {config_file}")


def main():
    """Main analysis workflow."""
    parser = argparse.ArgumentParser(
        description="AlphaGenome Analytics Example Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with API key
  python example_analysis.py --api-key YOUR_KEY
  
  # Full analysis with output directory
  python example_analysis.py --api-key YOUR_KEY --output results/ --verbose
  
  # Skip actual predictions (for testing)
  python example_analysis.py --no-api --output demo/
        """
    )
    
    parser.add_argument(
        "--api-key", "-k",
        help="AlphaGenome API key (or set ALPHAGENOME_API_KEY env var)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path("./example_output"),
        help="Output directory (default: ./example_output)"
    )
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Skip API calls (for testing/demo)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    
    # Get API key
    api_key = args.api_key or os.environ.get("ALPHAGENOME_API_KEY")
    
    if not api_key and not args.no_api:
        print("❌ Error: AlphaGenome API key required")
        print("   Use --api-key or set ALPHAGENOME_API_KEY environment variable")
        print("   Or use --no-api for demo mode")
        sys.exit(1)
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    print("🚀 AlphaGenome Analytics Example Analysis")
    print("=" * 50)
    print(f"Output directory: {args.output}")
    
    # Create sample configuration
    create_sample_config(args.output)
    
    # Generate visualization (doesn't need API)
    generate_visualization(args.output)
    
    if not args.no_api and api_key:
        # Run API-based analyses
        analyze_single_variant(api_key, args.output)
        analyze_variant_list(api_key, args.output)
    else:
        print("\n⚠️  Skipping API-based analyses (no API key provided)")
        print("   Run with --api-key to perform actual variant predictions")
    
    print("\n✅ Analysis complete!")
    print(f"   Check {args.output} for results")
    print("\n📚 Next steps:")
    print("   1. Get an AlphaGenome API key from https://www.alphagenomedocs.com")
    print("   2. Run: python example_analysis.py --api-key YOUR_KEY")
    print("   3. Explore the generated results and configuration files")


if __name__ == "__main__":
    main() 