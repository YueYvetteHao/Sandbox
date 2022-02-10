#!/usr/bin/python

#Parse uniprot xml, find all entries with tax id.

import sys
from xml.etree import ElementTree as ET

def main():
	file = sys.argv[1]
	taxid = sys.argv[2] # NCBI taxonomy id     Stentor coeruleus 	5963
	tree = ET.parse(file)
	root = tree.getroot() #uniprot
  
	for entry in root:  #entry
		# check organism
		found = 0
		for item in entry.findall('organism'):
			for subitem in item.findall('dbReference'):
				id = subitem.get('id')
				if id == taxid:
					found = 1
		
	#	Parse protein name and annotation
		if found == 1:
			entryname = entry.find('name').text
			entryid = entry.find('accession').text
			sys.stdout.write(entryid + '\t' + entryname + '\t')
			for item in entry.findall('protein'): 
				for subitem in item.findall('recommendedName'):
					for subsubitem in subitem.findall('fullName'):
						sys.stdout.write(subsubitem.text + '\t')
			for item in entry.findall('comment'):
			#	GOid = ''
				if item.get('type') == "subcellular location":
					for subitem in item:
						for subsubitem in subitem:
							sys.stdout.write(subsubitem.text + '; ')
					for subitem in item.findall('text'):
						sys.stdout.write(subitem.text + '\t')
			for item in entry.findall('dbReference'):
				GOid = ''
				if item.get('type') == "GO":
					GOid = item.get('id')
					sys.stdout.write(GOid + ' ')
					for subitem in item.findall('property'):
						GOvalue = ''
						if subitem.get('type') == "term":
							GOvalue = subitem.get('value')
							sys.stdout.write(GOvalue + '; ')
			sys.stdout.write('\n')
		
	
 #    	 
 #        	
 #   print ('\n')  
  
  
 #   for item in entry.findall('.//pathways'):
 #     for subitem in item.getentryren():
 #       pathname = subitem.find('name').text
 #       print pathname
 #   print '\r'   
     
if __name__ == '__main__':
  main()