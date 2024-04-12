

import sys
import os

bam = sys.argv[1]

ToolDir = sys.path[0]
bam_name = bam.split('/')[-1]

chrom_list = ['chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10', 'chr11','chr12','chr13','chr14','chr15', 'chr16','chr17', 'chr18','chr19','chr20', 'chr21','chr22','chrX','chrY','HPV16', 'HPV33', 'HPV35']
def split_chrom(bam):
	order = []
	for chrom in chrom_list:
		os.system(f'samtools view -@ 70 {bam} {chrom} -b > {chrom}.{bam_name}')
		order.append(f'samtools view -@ 60 {bam} {chrom} -b > {chrom}.{bam_name}')
	os.system(' & '.join(order))

def index_chrom(bam):
	for chrom in chrom_list:
		os.system(f"samtools index -@ 70 {chrom}.{bam_name}")

def rmdup(bam):
	for chrom in chrom_list:
		chr_bam = f'{chrom}.{bam_name}'
		namesort_bam = chr_bam.replace('.bam', '.namesort.bam') 
		fixmate_bam = chr_bam.replace('.bam', '.fixmate.bam')
		sorted_bam = chr_bam.replace('.bam', 'sorted.bam') 
		rmdup_bam = chr_bam.replace('.bam', '.rmdup.bam')

		os.system(f'samtools sort -@ 70 -n -o {namesort_bam} {chr_bam}')
		os.system(f'samtools fixmate -@ 70 -m {namesort_bam} {fixmate_bam}')
		os.system(f'samtools sort -@ 70 -o {sorted_bam} {fixmate_bam}')
		os.system(f'samtools markdup -@ 70 -r {sorted_bam} {rmdup_bam}')
		os.system(f'samtools index -@ 70 {rmdup_bam}')
		os.system(f'rm {chr_bam} {namesort_bam} {fixmate_bam} {sorted_bam}')

def merge(bam_name):
	bam_list = [f"{chrom}.{bam_name.replace('.bam', '.rmdup.bam')}" for chrom in chrom_list]

	os.system(f'samtools merge -@ 50 {name}.Tumor.HiC.merged.bam {" ".join(bam_list)}')
	os.system(f'samtools sort -@ 50 -o {name}.Tumor.HiC.sort.bam {name}.Tumor.HiC.merged.bam')
	os.system(f'samtools index {name}.Tumor.HiC.sort.bam')
	os.system(f'rm {name}.Tumor.HiC.merged.bam')

split_chrom(bam)
index_chrom(bam)
rmdup(bam)
merge(bam_name)




