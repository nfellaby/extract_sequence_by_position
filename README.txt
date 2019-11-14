### extract_sequence_by_position.py - originally built on 2019/11/12 - nfellaby

This program was built to extract the surrounding sequences from base positions previously identified.
The surrounding sequences can be tailored using the --buffer option.

Version 1.0

Software Dependencies 
Python >=2.7
biopython

Functionality


usage: extract_sequence_by_position.py [-h] -f FASTA -s START -e END -o OUTPUT
                                       [-r REVERSE] [-c COMPLEMENT]
                                       [-b BUFFER]

optional arguments:
  -h, --help            show this help message and exit
  -f FASTA, --fasta FASTA
                        Fasta Sequence from which to extract subsequence of
                        bases
  -s START, --start START
                        Starting base location of subsequence being extracted
  -e END, --end END     End base location of subsequence being extracted
  -o OUTPUT, --output OUTPUT
                        Output Directory
  -r REVERSE, --reverse REVERSE
                        Is the extratced sequence in the reverse orientation?
                        Will Correct if so. Specify: Yes/No
  -c COMPLEMENT, --complement COMPLEMENT
                        Is the extracted sequence in the complement strand?
                        Will correct if so. Specfify: Yes/No
  -b BUFFER, --buffer BUFFER
                        Extract bases around start and finish positions

### Known Errors or Issues

There is no accounting for when the buffer extracts sequence beyond the start or end of the DNA string.
This is likely to throw an error.
