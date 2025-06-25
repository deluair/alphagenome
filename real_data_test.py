#!/usr/bin/env python3
"""
Real Data Testing Script for AlphaGenome Analytics
==================================================

This script tests the AlphaGenome Analytics toolkit with real pathogenic variants
from ClinVar database and generates comprehensive HTML results.

Test variants include well-documented pathogenic mutations from BRCA1, BRCA2,
and TP53 genes that are known to cause cancer predisposition.
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import traceback

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('real_data_test.log')
    ]
)
logger = logging.getLogger(__name__)

def get_real_variants():
    """
    Return a curated list of real pathogenic variants from ClinVar.
    These are well-documented variants with known clinical significance.
    """
    return [
        {
            "id": "BRCA1_c.140G>T",
            "chromosome": "chr17",
            "position": 43106528,  # GRCh38
            "ref": "G",
            "alt": "T",
            "gene": "BRCA1",
            "hgvs_c": "c.140G>T",
            "hgvs_p": "p.Cys47Phe",
            "clinical_significance": "Pathogenic/Likely pathogenic",
            "condition": "Breast-ovarian cancer, familial 1",
            "clinvar_id": "VCV000054247",
            "consequence": "missense_variant",
            "description": "Pathogenic missense variant in BRCA1 affecting DNA repair function"
        },
        {
            "id": "BRCA1_c.5277+1G>A",
            "chromosome": "chr17", 
            "position": 43057051,  # GRCh38
            "ref": "G",
            "alt": "A",
            "gene": "BRCA1",
            "hgvs_c": "c.5277+1G>A",
            "hgvs_p": None,  # splice site
            "clinical_significance": "Pathogenic",
            "condition": "Breast-ovarian cancer, familial 1",
            "clinvar_id": "VCV000037654",
            "consequence": "splice_donor_variant",
            "description": "Pathogenic splice donor variant disrupting normal splicing"
        },
        {
            "id": "BRCA2_c.3160_3163del",
            "chromosome": "chr13",
            "position": 32337515,  # GRCh38 
            "ref": "GATA",
            "alt": "",
            "gene": "BRCA2",
            "hgvs_c": "c.3160_3163del",
            "hgvs_p": "p.Asp1054fs",
            "clinical_significance": "Pathogenic",
            "condition": "Breast-ovarian cancer, familial 2",
            "clinvar_id": "RCV000031405",
            "consequence": "frameshift_variant",
            "description": "Pathogenic frameshift deletion causing truncated protein"
        },
        {
            "id": "TP53_c.524G>A",
            "chromosome": "chr17",
            "position": 7674220,  # GRCh38
            "ref": "G", 
            "alt": "A",
            "gene": "TP53",
            "hgvs_c": "c.524G>A",
            "hgvs_p": "p.Arg175His",
            "clinical_significance": "Pathogenic",
            "condition": "Li-Fraumeni syndrome",
            "clinvar_id": "VCV000012771",
            "consequence": "missense_variant",
            "description": "Well-known hotspot mutation in TP53 DNA-binding domain"
        },
        {
            "id": "CFTR_c.1521_1523delCTT",
            "chromosome": "chr7",
            "position": 117548628,  # GRCh38
            "ref": "CTT",
            "alt": "",
            "gene": "CFTR", 
            "hgvs_c": "c.1521_1523delCTT",
            "hgvs_p": "p.Phe508del",
            "clinical_significance": "Pathogenic",
            "condition": "Cystic fibrosis",
            "clinvar_id": "VCV000001393",
            "consequence": "inframe_deletion",
            "description": "Most common CFTR mutation causing cystic fibrosis"
        }
    ]

def analyze_variants_mock(variants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Mock analysis function that simulates AlphaGenome predictions.
    In a real scenario, this would use the actual AlphaGenome API.
    """
    import random
    import numpy as np
    
    results = []
    
    for variant in variants:
        # Simulate processing time
        time.sleep(0.5)
        
        # Generate mock prediction data based on variant type
        consequence = variant.get('consequence', 'unknown')
        
        # Base predictions on variant severity
        if 'pathogenic' in variant.get('clinical_significance', '').lower():
            effect_magnitude = random.uniform(0.6, 0.9)
        else:
            effect_magnitude = random.uniform(0.1, 0.4)
            
        # Generate mock RNA-seq effects
        rna_ref = np.random.normal(1.0, 0.2, 1000)
        rna_alt = rna_ref + np.random.normal(0, 0.1, 1000)
        
        # Add effect based on variant type
        if consequence == 'missense_variant':
            # Moderate effect for missense
            effect_region = slice(400, 600)
            rna_alt[effect_region] *= (1 + effect_magnitude * 0.5)
        elif consequence == 'splice_donor_variant':
            # Strong effect for splice variants
            effect_region = slice(450, 550) 
            rna_alt[effect_region] *= (1 + effect_magnitude * 1.2)
        elif consequence == 'frameshift_variant':
            # Very strong effect for frameshift
            effect_region = slice(300, 700)
            rna_alt[effect_region] *= (1 + effect_magnitude * 1.5)
        
        # Calculate difference
        diff = rna_alt - rna_ref
        
        # Generate mock CAGE and DNase data
        cage_effect = random.uniform(-0.3, 0.8) * effect_magnitude
        dnase_effect = random.uniform(-0.2, 0.6) * effect_magnitude
        
        result = {
            "variant_id": variant["id"],
            "chromosome": variant["chromosome"],
            "position": variant["position"],
            "reference": variant["ref"],
            "alternate": variant["alt"],
            "gene": variant["gene"],
            "hgvs_c": variant["hgvs_c"],
            "hgvs_p": variant.get("hgvs_p"),
            "clinical_significance": variant["clinical_significance"],
            "condition": variant["condition"],
            "consequence": consequence,
            "predictions": {
                "rna_seq": {
                    "reference": {
                        "mean": float(np.mean(rna_ref)),
                        "std": float(np.std(rna_ref)),
                        "max": float(np.max(rna_ref)),
                        "min": float(np.min(rna_ref))
                    },
                    "alternate": {
                        "mean": float(np.mean(rna_alt)),
                        "std": float(np.std(rna_alt)),
                        "max": float(np.max(rna_alt)),
                        "min": float(np.min(rna_alt))
                    },
                    "difference": {
                        "mean_difference": float(np.mean(diff)),
                        "max_difference": float(np.max(np.abs(diff))),
                        "total_effect": float(np.sum(np.abs(diff))),
                        "correlation": float(np.corrcoef(rna_ref, rna_alt)[0, 1])
                    }
                },
                "cage": {
                    "effect_size": cage_effect,
                    "significance": "high" if abs(cage_effect) > 0.3 else "moderate"
                },
                "dnase": {
                    "effect_size": dnase_effect,
                    "significance": "high" if abs(dnase_effect) > 0.2 else "moderate"
                }
            },
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "clinvar_id": variant["clinvar_id"],
                "description": variant["description"]
            }
        }
        
        results.append(result)
        logger.info(f"Analyzed variant {variant['id']}: {consequence}")
    
    return results

def generate_html_report(results: List[Dict[str, Any]], output_file: str):
    """Generate a comprehensive HTML report of the variant analysis results."""
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaGenome Analytics - Real Variant Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }}
        .header h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            color: #7f8c8d;
            font-size: 18px;
        }}
        .summary {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .summary h2 {{
            color: #2c3e50;
            margin-top: 0;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-box {{
            background-color: #3498db;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-box.pathogenic {{
            background-color: #e74c3c;
        }}
        .stat-box.missense {{
            background-color: #f39c12;
        }}
        .stat-box.splice {{
            background-color: #9b59b6;
        }}
        .stat-box.frameshift {{
            background-color: #e67e22;
        }}
        .stat-number {{
            font-size: 24px;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 14px;
            margin-top: 5px;
        }}
        .variant {{
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 25px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .variant-header {{
            background-color: #34495e;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
            font-size: 18px;
        }}
        .variant-content {{
            padding: 20px;
        }}
        .variant-details {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}
        .detail-section {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
        }}
        .detail-section h4 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }}
        .predictions {{
            margin-top: 20px;
        }}
        .prediction-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        .prediction-box {{
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #3498db;
        }}
        .prediction-box h5 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
        }}
        .metric-value {{
            font-weight: bold;
            color: #2980b9;
        }}
        .clinical-significance {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }}
        .pathogenic {{
            background-color: #e74c3c;
            color: white;
        }}
        .likely-pathogenic {{
            background-color: #f39c12;
            color: white;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
            border-top: 1px solid #e0e0e0;
            padding-top: 20px;
        }}
        .timestamp {{
            font-style: italic;
            color: #95a5a6;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AlphaGenome Analytics</h1>
            <div class="subtitle">Real Genomic Variant Analysis Report</div>
            <div class="timestamp">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
        </div>
        
        <div class="summary">
            <h2>Analysis Summary</h2>
            <p>This report presents the analysis of {len(results)} real pathogenic variants from the ClinVar database 
            using AlphaGenome Analytics. These variants represent well-documented genomic changes with known 
            clinical significance in cancer predisposition and genetic disorders.</p>
        </div>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{len(results)}</div>
                <div class="stat-label">Total Variants</div>
            </div>
            <div class="stat-box pathogenic">
                <div class="stat-number">{len([r for r in results if 'pathogenic' in r.get('clinical_significance', '').lower()])}</div>
                <div class="stat-label">Pathogenic Variants</div>
            </div>
            <div class="stat-box missense">
                <div class="stat-number">{len([r for r in results if r.get('consequence') == 'missense_variant'])}</div>
                <div class="stat-label">Missense Variants</div>
            </div>
            <div class="stat-box splice">
                <div class="stat-number">{len([r for r in results if 'splice' in r.get('consequence', '')])}</div>
                <div class="stat-label">Splice Variants</div>
            </div>
        </div>
"""

    # Add individual variant sections
    for i, result in enumerate(results, 1):
        clinical_class = result.get('clinical_significance', '').lower().replace(' ', '-').replace('/', '-')
        
        # Format prediction values
        rna_predictions = result.get('predictions', {}).get('rna_seq', {})
        cage_predictions = result.get('predictions', {}).get('cage', {})
        dnase_predictions = result.get('predictions', {}).get('dnase', {})
        
        html_content += f"""
        <div class="variant">
            <div class="variant-header">
                Variant #{i}: {result.get('variant_id', 'Unknown')} 
                <span class="clinical-significance {clinical_class}">
                    {result.get('clinical_significance', 'Unknown')}
                </span>
            </div>
            <div class="variant-content">
                <div class="variant-details">
                    <div class="detail-section">
                        <h4>Genomic Information</h4>
                        <div class="metric">
                            <span>Gene:</span>
                            <span class="metric-value">{result.get('gene', 'N/A')}</span>
                        </div>
                        <div class="metric">
                            <span>Location:</span>
                            <span class="metric-value">{result.get('chromosome', '')}:{result.get('position', '')}</span>
                        </div>
                        <div class="metric">
                            <span>Change:</span>
                            <span class="metric-value">{result.get('reference', '')} → {result.get('alternate', '')}</span>
                        </div>
                        <div class="metric">
                            <span>HGVS (c.):</span>
                            <span class="metric-value">{result.get('hgvs_c', 'N/A')}</span>
                        </div>
                        <div class="metric">
                            <span>HGVS (p.):</span>
                            <span class="metric-value">{result.get('hgvs_p', 'N/A')}</span>
                        </div>
                        <div class="metric">
                            <span>Consequence:</span>
                            <span class="metric-value">{result.get('consequence', 'N/A').replace('_', ' ').title()}</span>
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h4>Clinical Information</h4>
                        <div class="metric">
                            <span>Condition:</span>
                            <span class="metric-value">{result.get('condition', 'N/A')}</span>
                        </div>
                        <div class="metric">
                            <span>ClinVar ID:</span>
                            <span class="metric-value">{result.get('metadata', {}).get('clinvar_id', 'N/A')}</span>
                        </div>
                        <div style="margin-top: 10px;">
                            <strong>Description:</strong><br>
                            {result.get('metadata', {}).get('description', 'No description available.')}
                        </div>
                    </div>
                </div>
                
                <div class="predictions">
                    <h4>AlphaGenome Predictions</h4>
                    <div class="prediction-grid">
                        <div class="prediction-box">
                            <h5>RNA-seq Effects</h5>
"""

        # Add RNA-seq metrics if available
        if rna_predictions:
            diff_data = rna_predictions.get('difference', {})
            html_content += f"""
                            <div class="metric">
                                <span>Mean Effect:</span>
                                <span class="metric-value">{diff_data.get('mean_difference', 0):.3f}</span>
                            </div>
                            <div class="metric">
                                <span>Max Effect:</span>
                                <span class="metric-value">{diff_data.get('max_difference', 0):.3f}</span>
                            </div>
                            <div class="metric">
                                <span>Total Effect:</span>
                                <span class="metric-value">{diff_data.get('total_effect', 0):.1f}</span>
                            </div>
                            <div class="metric">
                                <span>Correlation:</span>
                                <span class="metric-value">{diff_data.get('correlation', 0):.3f}</span>
                            </div>
"""
        
        html_content += f"""
                        </div>
                        
                        <div class="prediction-box">
                            <h5>CAGE Effects</h5>
                            <div class="metric">
                                <span>Effect Size:</span>
                                <span class="metric-value">{cage_predictions.get('effect_size', 0):.3f}</span>
                            </div>
                            <div class="metric">
                                <span>Significance:</span>
                                <span class="metric-value">{cage_predictions.get('significance', 'N/A').title()}</span>
                            </div>
                        </div>
                        
                        <div class="prediction-box">
                            <h5>DNase Effects</h5>
                            <div class="metric">
                                <span>Effect Size:</span>
                                <span class="metric-value">{dnase_predictions.get('effect_size', 0):.3f}</span>
                            </div>
                            <div class="metric">
                                <span>Significance:</span>
                                <span class="metric-value">{dnase_predictions.get('significance', 'N/A').title()}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
"""

    # Add footer
    html_content += f"""
        <div class="footer">
            <p><strong>AlphaGenome Analytics</strong> - Genomic Variant Analysis Toolkit</p>
            <p>Analysis based on real pathogenic variants from ClinVar database</p>
            <p>Generated with mock predictions for demonstration purposes</p>
            <p>Report created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
    </div>
</body>
</html>
"""

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"HTML report generated: {output_file}")

def main():
    """Main function to run the real data analysis."""
    print("=" * 60)
    print("AlphaGenome Analytics - Real Data Testing")
    print("=" * 60)
    print()
    
    # Get real variants
    print("Loading real pathogenic variants from ClinVar...")
    variants = get_real_variants()
    
    print(f"Loaded {len(variants)} real variants:")
    for variant in variants:
        print(f"  - {variant['id']}: {variant['gene']} ({variant['clinical_significance']})")
    print()
    
    # Create output directory
    output_dir = Path("real_data_results")
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Analyze variants (mock analysis since we don't have API access)
        print("Analyzing variants...")
        print("Note: Using mock predictions since AlphaGenome API access requires authentication")
        print()
        
        results = analyze_variants_mock(variants)
        
        # Save JSON results
        json_file = output_dir / "variant_analysis_results.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"JSON results saved: {json_file}")
        
        # Generate HTML report
        html_file = output_dir / "genomic_variant_analysis_report.html"
        generate_html_report(results, str(html_file))
        print(f"HTML report generated: {html_file}")
        
        # Generate summary statistics
        print("\n" + "=" * 60)
        print("ANALYSIS SUMMARY")
        print("=" * 60)
        
        total_variants = len(results)
        pathogenic_count = len([r for r in results if 'pathogenic' in r.get('clinical_significance', '').lower()])
        genes = {str(r.get('gene', '')) for r in results if r.get('gene')}
        consequences = {str(r.get('consequence', '')) for r in results if r.get('consequence')}
        
        print(f"Total variants analyzed: {total_variants}")
        print(f"Pathogenic variants: {pathogenic_count}")
        print(f"Genes analyzed: {', '.join(sorted(genes))}")
        print(f"Consequence types: {', '.join(sorted(consequences))}")
        
        # Calculate average effects
        total_effects = []
        for result in results:
            rna_diff = result.get('predictions', {}).get('rna_seq', {}).get('difference', {})
            if rna_diff.get('total_effect') is not None:
                total_effects.append(rna_diff['total_effect'])
        
        if total_effects:
            avg_effect = sum(total_effects) / len(total_effects)
            max_effect = max(total_effects)
            print(f"Average RNA-seq total effect: {avg_effect:.2f}")
            print(f"Maximum RNA-seq total effect: {max_effect:.2f}")
        
        print("\n" + "=" * 60)
        print("✅ Analysis completed successfully!")
        print(f"📁 Results saved in: {output_dir.absolute()}")
        print(f"🌐 Open the HTML report: {html_file.absolute()}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        print(f"\n❌ Error during analysis: {str(e)}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 