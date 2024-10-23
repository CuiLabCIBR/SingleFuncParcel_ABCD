#coding: utf-8
import scipy.io as sio
import numpy as np
import pandas as pd
import os
import sys
sys.path.append('/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step01_PLSprediction/atlasLoading/bootstrap');
import PLSr1_CZ_Random_RegressCovariates

# 
if len(sys.argv) < 2:
    print("need provide a serial number")
    sys.exit(1)
param = sys.argv[1]
print(f"serial number is: {param}")

try:
    param_str = str(param)
    print(f"string  fot serial number is: {param_str}")
except ValueError:
    print("not valid")

ResultsFolder =  '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step01_PLSprediction/atlasLoading/bootstrap/edu_new/results_' + param_str;
if not os.path.exists(ResultsFolder):
        os.makedirs(ResultsFolder);
        
# Import data
# 1. atlas loading
datapath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step00_getNewSubjData/s07_getAtlasFeature4Predict/AtlasLoading_fsaverage5_edu_new/AtlasLoading_All_RemoveZeros.txt';
data_files_all = np.loadtxt(datapath,delimiter=",")
data_files_all = np.float16(data_files_all) 
SubjectsData = data_files_all

#Subjects_Quantity = len(SubjectsData)/2
Subjects_Quantity = len(SubjectsData)
RandIndex = np.arange(Subjects_Quantity, dtype=int)
total_size = int(len(RandIndex) * 0.8)
np.random.shuffle(RandIndex)
RandIndex = RandIndex[:total_size]
data_dict = {'RandIndex': RandIndex}

RandIndexFolder = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step01_PLSprediction/atlasLoading/bootstrap/edu_new/RandIndex/'
if not os.path.exists(RandIndexFolder):
        os.makedirs(RandIndexFolder);
sio.savemat( RandIndexFolder + '/Index'+param_str+'.mat', data_dict)
rand_indices = RandIndex
print('first 10 randindex is ', rand_indices[:10])
SubjectsData_selected = SubjectsData[rand_indices, :]

# 2. subject label: cognition score
#labelpath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step00_getNewSubjData/s07_getAtlasFeature4Predict/topoLabel/topoLabel_SES_n4835.csv';
#labelpath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step00_getNewSubjData/s07_getAtlasFeature4Predict/topoLabel/new/topoLabel_n4965forADI_noNAN_new.csv';
labelpath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step00_getNewSubjData/s07_getAtlasFeature4Predict/topoLabel/new/topoLabel_n5308forEdu_new.csv';
label_files_all = pd.read_csv(labelpath)
#dimention = 'adjIncome' #ses_z_correct
#dimention = 'reshist_addr1_adi_perc' #percentage of ADI index
dimention = 'meanParentEdu' #parent edu
label = label_files_all[dimention]
y_label = np.array(label)
y_label_selected = y_label[rand_indices]
OverallPsyFactor = y_label_selected

# 3. covariates  
#covariatespath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step00_getNewSubjData/s07_getAtlasFeature4Predict/topoLabel/AgeSexMotionSite_SES.csv';
#covariatespath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step00_getNewSubjData/s07_getAtlasFeature4Predict/topoLabel/new/AgeSexMotionSite_n4965forADI_new.csv';
covariatespath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step00_getNewSubjData/s07_getAtlasFeature4Predict/topoLabel/new/AgeSexMotionSite_n5308forEdu_new.csv';
Covariates = pd.read_csv(covariatespath, header=0)
Covariates = Covariates.values
Covariates_selected = Covariates[rand_indices, 1:].astype(float) 
# age, sex, FD, site

# Range of parameters
ComponentNumber_Range = np.arange(10) + 1;
FoldQuantity = 2;
Parallel_Quantity = 1;
CVtimes = 1

# Predict
AtlasLoading_Folder = ResultsFolder + '/PLSr1/AtlasLoading';
ResultantFolder = AtlasLoading_Folder + '/RegressCovariates_RandomCV';
PLSr1_CZ_Random_RegressCovariates.PLSr1_KFold_RandomCV_MultiTimes(SubjectsData_selected, OverallPsyFactor, Covariates_selected, FoldQuantity, ComponentNumber_Range, CVtimes, ResultantFolder, Parallel_Quantity, 0)

# Permutation
#ResultantFolder = AtlasLoading_Folder + '/OverallPsyFactor_All_RegressCovariates_RandomCV_Permutation';
#PLSr1_CZ_Random_RegressCovariates.PLSr1_KFold_RandomCV_MultiTimes(SubjectsData, OverallPsyFactor, Covariates, #FoldQuantity, ComponentNumber_Range, 1000, ResultantFolder, Parallel_Quantity, 1, 'all.q')
