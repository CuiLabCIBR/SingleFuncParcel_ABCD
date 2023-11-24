# SingleFuncParcel_ABCD
Data and codes for our paper **"Personalized Large-scale Functional Networks in Adolescent Brain Cognitive Development Children: Linking Functional Network Topography with Socioeconomic Status"**.

Here, we delineated 17 *personalized functional networks* for Adolescent Brain Cognitive Development (**ABCD**) children using 20 min high-quality fMRI data and have publicly shared this resource. 

We also provided an exemplary usage of this resource in predicting unseen individuals’ socioeconomic status (**SES**) with *personalized functional network topography*, and discovered that the association between functional topography and SES was hierarchically patterned on the cortex along the sensorimotor-association (**S-A**) cortical axis.  

## `scripts`
- The [step01_participantsSelection](step01_participantsSelection/) folder contains scripts used to select participants used for  personalized functional networks construction and SES prediction.

- The [step02_singleParcel_NMF](step02_singleParcel_NMF/) folder contains scripts used to generate personalized functional network topography with non-negative matrix factorization (**NMF**) for ABCD children and scripts used to get results of *Figure 1* and *Figure 2*.

- The [step03_SESprediction](step03_SESprediction/) folder contains scripts used to create topography feature used for SES prediction, perform partial least squares regression (**PLS-R**) and scripts used to get results of *Figure 3*.

- The [step04_associationWithSArank](step04_associationWithSArank) folder contains scripts used to perform association analysis with S-A gradient and scripts used to get results of *Figure 2* and *Figure 3* .

- The [step05_singleParcel_MSHBM](step05_singleParcel_MSHBM) folder contains scripts used to generate personalized atlas label with the multi-session hierarchical Bayesian model (**MS-HBM**).

- The [step06_supplementaryAnalyses](step06_supplementaryAnalyses) folder contains atlas label (both NMF and MS-HBM) prediction with PLS-R and atlas loading prediction with ridge regression and scripts used to get results of *Supplementary Figure 4*.

- Other used GitHub repositories:

  - gifti-master
  - cifti-matlab-master
  - spin-test-master
  - PANDA_1.3.0_64
  - Collaborative_Brain_Decomposition-master

  

