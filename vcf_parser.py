# vcf_parser.py
import gzip
import os
def parse_info(info_string):
    """Parse INFO field into dictionary"""
    info_dict = {}
    
    for item in info_string.split(';'):
        if '=' in item:
            key, value = item.split('=')
            # Try to convert to number
            try:
                info_dict[key] = float(value)
            except:
                info_dict[key] = value
        else:
            info_dict[item] = True
    
    return info_dict

def read_vcf(vcf_file):
    """
    Read VCF file - handles:
    .vcf
    .vcf.gz
    """
    #Check if file exist first!
    if not os.path.exists(vcf_file):
        raise FileNotFoundError(f"VCF file not found: {vcf_file}")
    
    #check if compressed 
    if vcf_file.endswith('.gz'):
        print(f"Reading compressed file: {vcf_file}")
        opener = gzip.open(vcf_file, 'rt')
    else:
        print(f"Reading uncompressed file: {vcf_file}")
        opener = open(vcf_file, 'r')

    #parse variants
    
    variant_count = 0

    with opener as f :
        for line in f:

            #Skip metadata headers
            if line.startswith('##'):
                continue

            #skip column header 
            if line.startswith('#CHROM'):
                continue

            #parse variants
            fields = line.strip().split('\t')
            if len(fields) < 8:
                continue

            variant = {
                'CHROM': fields[0],
                'POS': int(fields[1]),
                'ID': fields[2],
                'REF': fields[3],
                'ALT': fields[4],
                'QUAL': float(fields[5]) if fields[5] != '.' else 0.0,
                'FILTER': fields[6],
                'INFO': fields[7]
            }

            variant['info_dict'] = parse_info(variant['INFO'])
            variant_count += 1

            yield variant
    
    print(f"total variants parsed: {variant_count}")



if __name__ == "__main__":
    # Test your parser
    vcf_file = "data/clinvar.vcf.gz"
    
    total = 0
    for variant in read_vcf(vcf_file):
        total += 1
        if total <= 5:  # Print first 5
            print(f"Variant {total}: {variant['CHROM']}:{variant['POS']} {variant['REF']}→{variant['ALT']}")
    
    print(f"\nTotal variants: {total}")