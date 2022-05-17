# Digital Divide Map


## Python Libraries

<ul>
<li> Geopandas
<li> Pandas
<li> Numpy
</ul>

## Instructions

The first script which needs to run is ```BC_Collapse.py``` which creates the data at the Block Code level and is further used by subsequent scripts. Here each year will have a different output file.


    python BC_Collapse.py --year 2019


Subsequent scripts are run like this and are saved to the same file for each year.


    python BG_Collapse.py --year 2019
    python CD_Collapse.py --year 2019
    python County_Collapse.py --year 2019
    python Tract_Collapse.py --year 2019