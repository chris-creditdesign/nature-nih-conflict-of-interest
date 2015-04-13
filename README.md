# Nature NIH conflict of interest investigation

Working process to determine the percentage of grants given to each institution that have a FCOI (financial conflict of interest) investigation associated with them. 

`FCOI working doc.xlsx` - NIH FOI document listing all conflict of interest reports that investigators filed in 2012 and 2013

**NIH Research Portfolio Online Reporting Tools (RePORT)** - A repository of NIH-funded research projects and access publications and patents resulting from that funding.

**ExPORTER Data Catalog** [http://exporter.nih.gov/ExPORTER_Catalog.aspx](http://exporter.nih.gov/ExPORTER_Catalog.aspx) - makes downloadable versions of the data accessed through the RePORT Expenditures and Results (RePORTER) interface available to the public. 

Download CSV and unzip files relating to fiscal years 2011-14:

- [http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2014.zip](http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2014.zip)
- [http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2013.zip](http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2013.zip)
- [http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2012.zip](http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2012.zip)
- [http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2011.zip](http://exporter.nih.gov/CSVs/final/RePORTER_PRJ_C_FY2011.zip)

## Merge FCOI document with NIH RePorter documents

Extract the relevant sheet from `FCOI working doc.xlsx` as a csv

	in2csv --sheet Colored "ref/excel/FCOI working doc.xlsx" > csv/fcoi.csv

Columns of interest in the NIH documents to match with the FCOI document

NIH RePorter document	| FCOI document
----------------------	| -------------  
APPLICATION_ID			| #  
PROJECT_TITLE			| GRANT TITLE 
PI_NAMEs				| CONTACT PD/PI NAME
ORG_NAME				| SUBMITTING INSTITUTION
FY						| #  
PROJECT_START			| #  
PROJECT_END				| #  
TOTAL_COST				| #  

Extract just the relevant columns from the four NIH documents into new documents and Convert `iso-8859-1` to `utf-8`:

	in2csv -e iso-8859-1 ref/csv/RePORTER_PRJ_C_FY2014.csv | csvcut -c 'APPLICATION_ID, PROJECT_TITLE, PI_NAMEs, ORG_NAME, FY, PROJECT_START, PROJECT_END, TOTAL_COST' > csv/nih_2014.csv
	in2csv -e iso-8859-1 ref/csv/RePORTER_PRJ_C_FY2013.csv | csvcut -c 'APPLICATION_ID, PROJECT_TITLE, PI_NAMEs, ORG_NAME, FY, PROJECT_START, PROJECT_END, TOTAL_COST' > csv/nih_2013.csv
	in2csv -e iso-8859-1 ref/csv/RePORTER_PRJ_C_FY2012.csv | csvcut -c 'APPLICATION_ID, PROJECT_TITLE, PI_NAMEs, ORG_NAME, FY, PROJECT_START, PROJECT_END, TOTAL_COST' > csv/nih_2012.csv
	in2csv -e iso-8859-1 ref/csv/RePORTER_PRJ_C_FY2011.csv | csvcut -c 'APPLICATION_ID, PROJECT_TITLE, PI_NAMEs, ORG_NAME, FY, PROJECT_START, PROJECT_END, TOTAL_COST' > csv/nih_2011.csv

Combine all of the entries for all four years into one CSV file:

	csvstack csv/nih_2014.csv csv/nih_2013.csv csv/nih_2012.csv csv/nih_2011.csv > csv/nih_all.csv

Use `wc -l` to count the number of lines in our two files

-	`csv/nih_all.csv` **315,065**
-	`csv/fcoi.csv` **4,416**

Join the two files, matching on `PROJECT_TITLE` and `GRANT TITLE`:

	csvjoin -c "PROJECT_TITLE, GRANT TITLE" --outer  csv/nih_all.csv csv/fcoi.csv > csv/nih-fcoi-join.csv

We can now remove the individual csv files to keep things tidy:
	
	rm csv/nih_2014.csv csv/nih_2013.csv csv/nih_2012.csv csv/nih_2011.csv

The new file has an extra 13563 entries. 

-	`csv/nih-fcoi-join.csv` **328,628**

We want to remove duplicated `APPLICATION_ID` and `FCOI_ID` presuming these to be unique. These are columns 1 and 9 respectively. This can be checked with:

	csvcut -n csv/nih-fcoi-join.csv

Remove the duplicate `APPLICATION_ID`s:

	python python/remove-duplicate-entries.py csv/nih-fcoi-join.csv csv/nih-fcoi-clean-a.csv 0

-	`csv/nih-fcoi-clean-a.csv` **315,265**

Remove the duplicate `FCOI_ID`s:
	
	python python/remove-duplicate-entries.py csv/nih-fcoi-clean-a.csv csv/nih-fcoi-clean-b.csv 8

-	`csv/nih-fcoi-clean-b.csv` **312,272**

Let's also count how many conflicts of interest remain:

	python python/count-fcoi.py csv/nih-fcoi-clean-b.csv

**1,188**

Now we can attempt to count the number of grants for each institution as well as the number of fcoi investigations:

	python python/sum-fcoi.py csv/nih-fcoi-clean-b.csv csv/nih-fcoi-summed.csv








