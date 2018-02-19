###########################################
Calculating summary statistics on real data
###########################################

***********
Data format
***********

Real data must be in PLINK .tped file with 0's and 1's.
Sites in rows, individuals in columns (first 4 columns chr, rsnumber, site_begin, site_end).
The populations must be in the same order as specified in the model file for the simulations.

Put the individuals in the correct order
https://www.cog-genomics.org/plink2/data#indiv_sort
::

    plink --bfile bfile --indiv-sort f sample_order.txt --make-bed --out bfile_ordered


To get in the .tped format from .bed .bim .fam with 0's and 1's refer to
https://www.cog-genomics.org/plink2/formats#tped
::

    plink --bfile bfile --recode transpose 01 --output-missing-genotype N --out tfile01


*****
Usage
*****

``real_data_ss.py`` takes 5 arguments:
    1. ``model_file``
    2. ``param_file``
    3. ``output_dir``
    4. ``genome_file``
    5. ``array_file``

e.g.
::

    python real_data_ss.py examples/eg1/model_file_eg1.csv examples/eg1/param_file_eg1.txt out_dir ~/data/HapMap_example/test_10_YRI_CEU_CHB.tped ~/data/HapMap_example/test_10_YRI_CEU_CHB_KHV_hg18_ill_650.tped

