################################################################################
# 
# Human Variome Database Portal.
#
# === License ===
#
# Last Author:   $Author: AlanLo $
# Last Revision: $Rev: 558 $
# Last Modified: $Date: 2011-08-24 13:43:55 +1000 (Wed, 24 Aug 2011) $ 
#
# === Description ===
#
#
################################################################################

from Portal.hvp.models.search import Gene

import csv

class genename_reader:
	INDICES =					   \
		{						   \
			"HGNC_ID": 0,		   \
			"ApprovedSymbol": 1,	\
			"ApprovedName": 2,	  \
			"Status": 3,			\
			"PreviousSymbols": 6,   \
			"PreviousNames": 7,	 \
			"AliasSymbols": 8,	  \
			"AliasNames": 9,		\
			"Chromosome": 10,	   \
			"RefSeqID": 23,		 \
			"RefSeqIDNCBI": 34,	 \
		}
		
	def __init__(self, filename, indices = INDICES):
		self.filename = filename
		self.indices = indices
		self.entries = []
		
	def read( self ):
		reader = csv.reader(open(self.filename, 'rb'), dialect = 'excel-tab')
		self.entries = []
				
		i = 0;
		for row in reader:
			# Do not use the first row (header)
			if i > 0:
				### Mapping ###
				entry = self.map_entry(row, self.indices)
				### Filtering ###
				if not( self.filter_entry(entry) ):
					continue
				### Transform ###
				self.entries.append(entry)
				
				ref_seq_str = ''
				if len(entry["RefSeqID"]) > 0:
					ref_seq_str = entry["RefSeqID"]
				else:
					ref_seq_str = entry["RefSeqIDNCBI"]
				
				ref_seq = ref_seq_str.split('.')
				ref_seq_ver = ''
				if len(ref_seq) > 1:
					ref_seq_ver = ref_seq[1]
				
				gene = Gene()
				gene.GeneName = entry["ApprovedSymbol"]
				gene.GeneDescription = entry["ApprovedName"]
				gene.RefSeqName = ref_seq[0]
				gene.RefSeqVer = ref_seq_ver
				gene.RefSeqValidStart = None
				gene.RefSeqValidEnd = None
				gene.HGNC_ID = entry["HGNC_ID"]
				gene.AlternateSymbols = entry["AliasSymbols"]
				gene.AlternateNames = entry["AliasNames"]
				gene.Chromosome = entry["Chromosome"]
				gene.PreviousSymbols = entry["PreviousSymbols"]
				gene.PreviousNames = entry["PreviousNames"]
									
				gene.save()
			i = i + 1

	def map_entry( self, row, indices ):
		result = {}
		for item in indices:
			result[item] = row[indices[item]]
			
		return result;

	def filter_entry( self, entry ):
		return \
			entry["Status"].find('Withdrawn') < 0 and \
			(len(entry["RefSeqID"]) > 0 or len(entry["RefSeqIDNCBI"]) > 0)
		

   


