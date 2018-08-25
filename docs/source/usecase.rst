Use Cases
---------

Is SimPrily right for your research?

============================  =====================   =============================================
Use case                      Can SimPrily be used?   Notes
============================  =====================   =============================================
Coalescent simulation         yes
Forward simulation            no
Selection                     no
Demographic model             yes                     see MaCS/ms documentation
Recombination map             yes                     not necessary, but sims will be more accurate
Constant mutation rate        yes
Constant model parameters     yes
Uniform priors of parameters  yes
Non-uniform priors            no
Chromosome-size loci          yes
Whole genome                  no                      must simulate each chromosome separately
1000's of samples             no                      try msprime
Sequence (variant) data       yes
Exome data                    yes
SNP array data                yes
Microsatellite/str data       no
Known SNP ascertainment       yes
Unknown SNP ascertainment     yes                     see Quinto-Cortes et al. (2018)
AFS Summary statistics        yes
IBD Summary statistics        yes                     only with SNP array option
Raw simulated output          no
PLINK ped/map output          yes                     only with SNP array option
============================  =====================   =============================================