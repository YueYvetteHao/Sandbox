#!/bin/bash
#SBATCH --job-name="xmlxml"                                                     
#SBATCH --ntasks=8                # Number of cores requested                  
#SBATCH --qos=cmeqos               # The queue (line) we are in                 
#SBATCH --partition=cmecpu1         # The compute node set to submit to         
#SBATCH --output=stentor_%j.out                                                      
#SBATCH --error=stentor_%j.err                                                       
#SBATCH --time=7-00:00:00                                                       
#SBATCH --mail-type=ALL                                                         
##SBATCH --mail-user=yue.hao@asu.edu  



cd /scratch/yhao38/Proteomics

sed -i -e 's/ xmlns="http:\/\/uniprot.org\/uniprot"//g' uniprot_trembl_invertebrates.xml

python uniprot_xml_parser.py uniprot_trembl_invertebrates.xml 5963