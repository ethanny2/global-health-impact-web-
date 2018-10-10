#import scholar as scholar_file 
#As opposed to scholar.py (a command line API) use scholarly.py which is more robust and simple. No API key needed 

#Once a study is determined as meeting our criteria--gauging the efficacy of a drug of interest against
# e.g. uncomplicated p. falciparum--the abstract is read and basic information is recorded in a spreadsheet for that 
# particular drug, organized by country. This sort of information can include, but is not limited to, region of the study, 
# the year, the sample size, the comparator, the study design, and characteristics of the sample population.

#Difficult part:
#	How to choose relevant articles from side bar of current article: There's a scholarly function for this.
#	More importantly, what defines a "usable/meeting criteria paper"? Can it be determined by a program?
#	Once the PDF is scanned and parsed into plain text by the Google OCR API, we could potentially...
#		-Scan for keywords  
#	Another problem... how to get around the Google Scholar Captcha? 	


#Questions:
# 1.When querying Google Scholar/Pub Med etc... with the format specified in the Systematic Review Handbook 
#	format  ==> [drug name] "efficacy" [disease name]
#	Do you search every possible drug name on the drug list with with every possible disease?
#	For example the query "Abacavir efficacy HIV" makes sense because that drug is used for the treatment of HIV/AIDS but
#	the query "ART/Artemisinin efficacy HIV" doesn't really make sense because that Artemisinin is used to treat Malaria.
#	If this is the case do you have list that associates each the drugs with a disease it treats?

# 2. When querying Google scholar/Pub Med etc... After the initial query e.g ("Abacavir efficacy HIV") how do we decide which 
# related articles are "relvant"? 
# 
# 3. How can we tell which articles found on the sites are satisfatory to use in the Global Health Index project? 
# For the sake of using making a function that can ideally identify what reports/studies are usuable by the project,
# is there anything in particular can quantify how likely an article is to be used. 
# For example: Maybe you choose the reports to be used in the project based on their... 
# Author, number appearences of a certain word, publisher, release date etc... 
# 
# 4.  Is there a list of medical/techincal terms for all the diseases represented on the site?
# 
# 5. Is there a list of generic names for all the drugs listed on the Systematic Review handbook google document? (pg 11/12)
# 




#INFO: Short script demonstrating Google Scholar scraping...
#URLs are in varying formats... (don't link directly to PDFs). 

import scholarly
from pprint import pprint
# -*- coding: utf-8 -*-
#Search query formats:	
	#[drug name] "efficacy" [disease technical name]
	#[drug name] "efficacy" [disease name]
	#[drug name] "efficacy"
	#[drug name] "clinical trial" [disease name]
def main():
		def debugQuery(msg):
				print('Currently executing query ['+msg + ']')
		class Drug():
			def __init__(self,brand_name_in, generic_name_in):
				self.brand_name = brand_name_in
				self.generic_name = generic_name_in
		#Object to hold all values of disease name 
		class Disease():
			def __init__(self,reg_name_in, tech_name_in):
				self.reg_name = reg_name_in
				self.tech_name = tech_name_in
				self.drug_arr = []	
				self.pub_arr = []
			#Checks if article already exists in array, if so, don't add it
			#False if already in array, don't add
			def checkID(self,pubObj):
				retVal = True
				for pub in self.pub_arr:
					if pubObj.id_scholarcitedby == pub.id:
						retVal =  False; 
				return retVal
			def addDrug(self,brand,generic):
				temp = Drug(brand,generic)
				self.drug_arr.append(temp)
			def addPublicationRecord(self,pubObj,query_in):
				if self.checkID(pubObj):
					temp = Publication(pubObj,query_in)
					self.pub_arr.append(temp)
			def print_publications(self):
				for pub in self.pub_arr:
					print("------------------------------------------------------------------------------------------------")
					pprint(vars(pub))
					print("------------------------------------------------------------------------------------------------")
			def print_drugs(self):
				for drug in self.drug_arr:
					pprint(vars(drug))
		# record important fields, 
		# Abstract , author, title ,url , source, # of other articles cited by,
		# drug and disease associated with it, and finally the query that was responsible for finding the article
		class Publication():
			#pass in object returned by scholarly search function
			def __init__(self,pubObj,query_in):
				self.title = pubObj.bib['title']
				self.author = pubObj.bib['author']
				self.abstract = pubObj.bib['abstract']
				self.url = pubObj.bib['url']
				self.citedby = pubObj.citedby
				self.source = pubObj.source
				#query that yielded result
				self.used_query = query_in
				#Cited by ID generated 
				self.id  = pubObj.id_scholarcitedby


		query_efficacy = " efficacy " #append rest of queries to the left and right
		query_clinical = " clinical trial "
		query_num = 1


#Drug disease association:
#	3TC/Lamivudine -> HIV/AIDS | ABC/Abacavir -> HIV/AIDS | AL/Artemether-Lumefantrine -> Malaria ,  Amk/Amikacin ->??? TB (Maybe)
#	 ART/Artemisinin -> Malaria , AS+AQ/Artesunate + Amodiaquin --> Malaria , ATV/r Atazanavir/Ritonavir --> HIV

		malaria = Disease('Malaria','Plasmodium')
		malaria.addDrug('Artemether-Lumefantrine','')
		malaria.addDrug('Artemisinin','')
		malaria.addDrug('Amodiaquin','')
		tb = Disease('TB','Tuberculosis')
		hiv = Disease('HIV','Human Immunodeficiency Virus')
		hiv.addDrug('Lamivudine','')
		hiv.addDrug('Abacavir','')
		hiv.addDrug('Ritonavir','')
		aids = Disease('AIDS','Acquired Immune Deficiency Syndrome')
		onchocerciasis = Disease('Onchocerciasis','')
		schistosomiasis = Disease('Schistosomiasis','Bilharzia')
		elephantiasis =  Disease('Elephantiasis','Lymphatic Filariasis')
		hookworm = Disease('Hookworm','')
		roundworm = Disease('Roundworm','')
		whipworm = Disease('Whipworm','')

		disease_objs = [malaria , tb , hiv , aids , onchocerciasis , schistosomiasis , elephantiasis , hookworm , roundworm , 
		whipworm]

		#Technicals names taken from google search, change later
		#Splitting AIDS & HIV technical terms into 2 separate elements.
		#Onchocerciasis may be the technical name as well, (there's also river blindness)
		#Schistosomiasis Also known as bilharzia and "Snail fever" 
		# elephantiasis <===> Lymphatic Filariasis
		# Hookworm <==> (Refers to infection as well as species) Necator americanus and Ancylostoma duodenale speices of worm infect ppl
		# Roundworm <==> Ascaris Lumbricoides
		# Whipworm <==> Trichuris Trichiura
		# 
		


	#[drug name] "efficacy" [disease technical name]
	#[drug name] "efficacy" [disease name]
	#[drug name] "efficacy"
	#[drug name] "clinical trial" [disease name]
	#Repeat with both generic and brand name drugs, 
	
		for i in range(query_num):
			for disease in disease_objs:
				for drug in disease.drug_arr:
					#recall drugs have 2 names
					query1 = drug.brand_name + query_efficacy + disease.tech_name
					query2 = drug.brand_name + query_efficacy + disease.reg_name
					query3 = drug.brand_name + query_efficacy
					query4 = drug.brand_name + query_clinical + disease.reg_name
					'''
					Don't know any generic names yet but this can just be uncommented.
					query5 = drug.generic_name + query_efficacy + disease.tech_name
					query6 = drug.generic_name + query_efficacy + disease.reg_name
					query7 = drug.generic_name + query_efficacy
					query8 = drug.generic_name + query_clinical + disease.reg_name
					'''
					#grab the URLs from here
					#print(next(scholarly.search_pubs_query(query1)))
					#Record publication data on Disease object in an array
					#Could not have a tech name
					obj = next(scholarly.search_pubs_query(query1))
					if not disease.tech_name== '': 
						debugQuery(query1)
						disease.addPublicationRecord(obj,query1)
					debugQuery(query2)
					obj = next(scholarly.search_pubs_query(query2))
					disease.addPublicationRecord(obj,query2)

					debugQuery(query3)
					obj = next(scholarly.search_pubs_query(query3))
					disease.addPublicationRecord(obj,query3)

					debugQuery(query4)
					obj = next(scholarly.search_pubs_query(query4))
					disease.addPublicationRecord(obj,query4)
					print("Printing contents of the current Disease obj")
					print(disease.__dict__)
					disease.print_publications()
					disease.print_drugs()






if __name__ == '__main__':
	main()
