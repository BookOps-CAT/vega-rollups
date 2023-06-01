# vega-rollups
Scripts manipulating bibs to properly roll up in Vega


## Running the script
```bash
$ python manipulate.py [path to src marcfile] [path to output file]
```

The script produces three files:
+ processed marcfile - MARC21 recods successfuly processed with modified 240
+ `processed.csv` - a list of bib #s, 245s, and new 240s output the marc file
+ `skipped.csv` - a list of bib #s and 245s skipped by script


## Strategy
+ consider only bibs that have $n in the 245 field but no equivalent in the 240
+ consider only print materials (BIB MAT "a")
+ consider only branch materials (910  $a BL) 
+ ignore complex cases:
    + presence of other than $a$n$l subfields in the original 240
    + no digits in $n of the 245 (example: Book two, Volume IX, etc)
    + typos that concatenate words with digits, example: Book2
