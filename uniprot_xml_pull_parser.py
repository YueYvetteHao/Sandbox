#!/usr/bin/python

#Parse uniprot xml, find all entries with tax id.

import sys
from xml.etree.ElementTree import iterparse, XMLParser


def main():
#	file = 'uniprot_test.xml'
	file = sys.argv[1]
	taxid = sys.argv[2] # NCBI taxonomy id     Stentor coeruleus 	5963
	

	parser = XMLParser()
	context = iterparse(file, events=['start'], parser=parser)
	for index, (event, elem) in enumerate(context):
		if elem.tag == 'entry':
		#	print ('begin entry!')
			found = 0
			for item in elem.findall('organism'):
				for subitem in item.findall('dbReference'):
					id = subitem.get('id')
					if id == taxid:
						found = 1
				for subitem in item.findall('name'):
					type = subitem.get('type')
					#stentor
					if type == 'scientific' and subitem.text == 'Stentor coeruleus':
						found = 1
					#	print ('Yah!')
			if found == 1:
		#		entryname = elem.find('name').text
				entryid = elem.find('accession').text
		#		sys.stdout.write(entryid + '\t' + entryname + '\t')
				sys.stdout.write(entryid + '\t')
				for item in elem.findall('protein'): 
					for subitem in item.findall('recommendedName'):
						for subsubitem in subitem.findall('fullName'):
							sys.stdout.write(subsubitem.text + '\t')

				for item in elem.findall('dbReference'):
				
					GOid = ''
					if item.get('type') == "GO":
						GOid = item.get('id')
						sys.stdout.write(GOid + ' ')
						for subitem in item.findall('property'):
							GOvalue = ''
							if subitem.get('type') == "term":
								GOvalue = subitem.get('value')
								sys.stdout.write(GOvalue + '; ')
						sys.stdout.write('\t')
						
					PFid = ''
					if item.get('type') == "Pfam":
						PFid = item.get('id')
						sys.stdout.write(PFid + ' ')
						for subitem in item.findall('property'):
							PFvalue = ''
							if subitem.get('type') == "entry name":
								PFvalue = subitem.get('value')
								sys.stdout.write(PFvalue + '; ')								
						sys.stdout.write('\t')
								
				for item in elem.findall('comment'):
				#	GOid = ''
					if item.get('type') == "subcellular location":
						for subitem in item:
							for subsubitem in subitem:
								sys.stdout.write(subsubitem.text + '; ')
						sys.stdout.write('\t')
						for subitem in item.findall('text'):
							sys.stdout.write(subitem.text + '\t')
				sys.stdout.write('\n')
	#	print (event, elem.tag)
		elem.clear()			
	

if __name__ == '__main__':
	main()