# Explainable-Clustering-Energy
This repository contains Python code and data files related to the BII project on explaining clustered energy data.

`cluster\_descriptor\_NLIP.py`: Python code for the Minimum Descriptors Problem expressed as a Nonlinear Integer Program.

`cluster\_descriptor\_ILP.py`: Python code for the Minimum Descriptors Problem expressed as a Linear Integer Program.

**Test 1** :

Charlottesville and Albermarle County data

Dates Chosen:

8th January 2014

8th July 2014

Associated Files:

`tag\_data\_analysis.ipynb`: Python code for preliminary analysis of data from RECS and SPEW for tag selection.

`initial\_test\_clustering.ipynb`: Python code for normalization, clustering, and tagging Charlottesville and Albermarle data.

**Test 2** :

| **County FIPS Code** | **County Name** | **State Name** | **Urban/Rural Classification** | **Households** |
| --- | --- | --- | --- | --- |
| 8013 | Boulder | Colorado | Urban | 125768 |
| 56013 | Fremont | Wyoming | Rural | 17494 |
| 4015 | Mohave | Arizona | Urban | 108396 |
| 32003 | Clark | Nevada | Urban | 812840 |
| 48031 | Blanco | Texas | Rural | 5237 |
| 12099 | Palm Beach | Florida | Urban/Mixed | 657106 |
| 6081 | San Mateo | California | Urban | 270039 |
| 41011 | Coos | Oregon | Rural | 30487 |
| 4025 | Yavapai | Arizona | Rural | 108244 |
| 36061 | New York | New York | Urban | 839013 |
| 51003 | Albermarle | Virginia | Mixed | 41357 |
| 27027 | Clay | Minnesota | Metropolitan | 23320 |

5% Sampling

Dates Chosen:

01/15/2014

03/15/2014

05/15/2014

07/15/2014

09/15/2014

11/15/2014

Associated Files:

`energy\_analysis.ipynb`: Python code for sampling, normalization, clustering, and tagging energy data + cluster membership and energy curve analysis

`temperature\_analysis.ipynb`: Python code for highest, lowest, and average temperature per month analysis for each county

**tagged\_data\_test\_2**

`tagged\_data\_test\_2\_c3.txt`: 3 clusters

`tagged\_data\_test\_2\_c5.txt`: 5 clusters

`tagged\_data\_test\_2\_c10.txt`: 10 clusters
