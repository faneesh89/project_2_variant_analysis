# variant_analyzer.py

def analyze_variants(variants):
    """
    Calculate statistics about variants
    """
    
    stats = {
        'total': len(variants),
        'snps': 0,
        'indels': 0,
        'quality_scores': [],
        'depths': [],
        'chromosomes': {}
    }
    
    for var in variants:
        # Count SNPs vs Indels
        if len(var['REF']) == len(var['ALT']):
            stats['snps'] += 1
        else:
            stats['indels'] += 1
        
        # Collect metrics
        stats['quality_scores'].append(var['QUAL'])
        
        depth = var['info_dict'].get('DP', 0)
        stats['depths'].append(depth)
        
        # Count by chromosome
        chrom = var['CHROM']
        stats['chromosomes'][chrom] = stats['chromosomes'].get(chrom, 0) + 1
    
    # Calculate averages
    if stats['quality_scores']:
        stats['avg_quality'] = sum(stats['quality_scores']) / len(stats['quality_scores'])
    
    if stats['depths']:
        stats['avg_depth'] = sum(stats['depths']) / len(stats['depths'])
    
    return stats


if __name__ == "__main__":
    from vcf_parser import read_vcf
    from variant_filter import filter_variants
    
    variants = list(read_vcf("data/sample.vcf"))
    good, bad = filter_variants(variants)
    
    stats = analyze_variants(good)
    
    print(f"SNPs: {stats['snps']}")
    print(f"Indels: {stats['indels']}")
    print(f"Avg Quality: {stats['avg_quality']:.1f}")
    print(f"Avg Depth: {stats['avg_depth']:.1f}")