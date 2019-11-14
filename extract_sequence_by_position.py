##### Extracts the bases according to the positions you require


from itertools import groupby
import argparse
import sys, os, subprocess, glob
import re
import datetime
import random
from Bio.Seq import Seq
from Bio.Alphabet import generic_dna


### User inputs
### Read in FASTA file 
### Read in Start and Finish Sequence
### Is the sequence in reverse orientation?
### Is the sequence a complement?

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--fasta", required=True, help="Fasta Sequence from which to extract subsequence of bases")
ap.add_argument("-s", "--start", required=True, help="Starting base location of subsequence being extracted")
ap.add_argument("-e", "--end", required=True, help="End base location of subsequence being extracted")
ap.add_argument("-o", "--output", required=True, help="Output Directory")
ap.add_argument("-r", "--reverse", help="Is the extratced sequence in the reverse orientation? Will Correct if so. Specify: Yes/No")
ap.add_argument("-c", "--complement", help="Is the extracted sequence in the complement strand? Will correct if so. Specfify: Yes/No")
ap.add_argument("-b", "--buffer", help="Extract bases around start and finish positions")

args=vars(ap.parse_args())


input_fasta = args["fasta"]

#'/phengs/hpc_storage/home/nicholas.ellaby/data/20190208_St_Helier/Prokka_Analysis/20190830_Maria_Nanopore/IncLM_plasmids/fastas/H181780424_75455bp_plasmid.fasta'

working_dir=args["output"]


### Sequence for extraction Start and Finish position
start = args["start"]
end = args["end"]

if args['reverse'] is not None:
	reverse = args['reverse']
else:
	reverse = 'No'


if args['complement'] is not None:
	complement = args['complement']
else:
	complement = 'No'


if args['buffer'] is not None:
	buffer = args['buffer']
	buffer = int(buffer)
	start = int(start) - buffer
	end = int(end) + buffer		


#print folder	
sample_id = os.path.basename(input_fasta).split('.')[0]
reference = input_fasta
print reference
fasta = open(reference, 'r')

new_fasta = open(working_dir +'/'+sample_id+'_'+str(start)+'-'+str(end)+'bp.fasta', 'w')

def fasta_iter(fasta_name):
	contig_no = 0
	fh = fasta_name
	faiter=(x[1] for x in groupby(fh, lambda line: line[0]==">"))
	for header in faiter:
		contig_no += 1
		header = header.next()[1:].strip()
		seq="".join(s.strip() for s in faiter.next())
		extract=seq[int(start):int(end)]
		if reverse == 'No':
			pass
		elif reverse == 'Yes':
			extract = extract[::-1]
		else:
			print ' Please use only "Yes" or "No" when specifying if the sequence is in reverse orientation.'
			sys.exit()
		if complement == 'No':
			pass
		elif complement == 'Yes':
			dna=Seq(extract, generic_dna)
			extract = str(dna.complement())
		else:
			print 'Please use only "Yes" or "No" when specifying if the sequence is on the complement strand.'
                        sys.exit()

		print extract
		yield header, extract, contig_no

def insert_newlines(string, every=80):
        lines = []
        for i in xrange(0,len(string), every):
                lines.append(string[i:i+every])
        return '\n'.join(lines)



for fasta_file in fasta_iter(fasta):
	ref_header = fasta_file[0]
	ref_seq = fasta_file[1]
	contig_no = str(fasta_file[2])
	new_header = ref_header.split('|')[0]
	new_header = new_header+'_'+contig_no+'_'+str(start)+'_'+str(end)+'bp'
	new_header = re.sub('[^a-zA-Z0-9 \n]','', new_header)

		
	print >>new_fasta, '>'+new_header[0:18]
	ref_seq = insert_newlines(ref_seq)
	print >>new_fasta, ref_seq

