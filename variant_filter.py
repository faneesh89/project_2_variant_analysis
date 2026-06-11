# variant_filter.py

def filter_variants(variants, min_qual=20, min_depth=10):
    """
    Filter variants by quality metrics
    """
    
    filtered = []
    rejected = []
    
    for var in variants:
        qual = var['QUAL']
        info = var['info_dict']
        
        # Get depth
        depth = info.get('DP', 0)
        
        # Apply filters
        reasons = []
        
        if qual < min_qual:
            reasons.append(f"Low QUAL ({qual})")
        
        if depth < min_depth:
            reasons.append(f"Low DP ({depth})")
        
        if var['FILTER'] != 'PASS':
            reasons.append(f"FILTER={var['FILTER']}")
        
        # Decide
        if not reasons:
            filtered.append(var)
        else:
            rejected.append({
                'variant': var,
                'reasons': reasons
            })
    
    return filtered, rejected


if __name__ == "__main__":
    from vcf_parser import read_vcf
    
    variants = list(read_vcf("data/sample.vcf"))
    good, bad = filter_variants(variants, min_qual=20, min_depth=10)
    
    print(f"Total: {len(variants)}")
    print(f"Passed: {len(good)}")
    print(f"Rejected: {len(bad)}")