#!/usr/bin/python3
import os
import subprocess
# use subprocess to run the following esearch

esearch - db protein - query "glucose-6-phosphatase [PROT] AND Aves [ORGN]" | efetch - format (fasta > glucose_6_phosphatase.fasta)
