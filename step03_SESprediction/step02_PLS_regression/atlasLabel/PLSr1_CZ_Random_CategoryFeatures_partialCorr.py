# -*- coding: utf-8 -*-
import os
import scipy.io as sio
import numpy as np
import pandas as pd
import time
from sklearn import linear_model
from sklearn import preprocessing
from sklearn import cross_decomposition
from joblib import Parallel, delayed
import statsmodels.formula.api as sm
import pingouin as pg
from datetime import datetime
CodesPath = '/ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/replication_ZSL/step01_prediction/PLS_regression/NMF_n3198/CovariatesControlled/zaixu/atlasLabel_10k/NMF/';
 
def PLSr1_KFold_RandomCV_MultiTimes(Subjects_Data, Subjects_Score, Covariates, Fold_Quantity, ComponentNumber_Range, CVRepeatTimes, ResultantFolder, Parallel_Quantity, Permutation_Flag, RandIndex_File_List=''):

    if not os.path.exists(ResultantFolder):
        os.makedirs(ResultantFolder);
    Subjects_Data_Mat = {'Subjects_Data': Subjects_Data}
    Subjects_Data_Mat_Path = ResultantFolder + '/Subjects_Data.mat'
    sio.savemat(Subjects_Data_Mat_Path, Subjects_Data_Mat);

    Finish_File = [];
    Corr_MTimes = np.zeros(CVRepeatTimes);
    MAE_MTimes = np.zeros(CVRepeatTimes);
    for i in np.arange(CVRepeatTimes):
        ResultantFolder_TimeI = ResultantFolder + '/Time_' + str(i)
        if not os.path.exists(ResultantFolder_TimeI):
            os.makedirs(ResultantFolder_TimeI);
        if not os.path.exists(ResultantFolder_TimeI + '/Res_NFold.mat'):
            
            if RandIndex_File_List != '':
                RandIndex_File = RandIndex_File_List[i]
            else:
                RandIndex_File = '';

            Configuration_Mat = {'Subjects_Data_Mat_Path': Subjects_Data_Mat_Path,   'Subjects_Score': Subjects_Score, 'Covariates': Covariates, 'Fold_Quantity': Fold_Quantity, 'ComponentNumber_Range': ComponentNumber_Range, 'CVRepeatTimes': CVRepeatTimes, 'ResultantFolder_TimeI': ResultantFolder_TimeI, 'Parallel_Quantity': Parallel_Quantity, 'Permutation_Flag': Permutation_Flag, 'RandIndex_File': RandIndex_File};
            sio.savemat(ResultantFolder_TimeI + '/Configuration.mat', Configuration_Mat);

            system_cmd = 'python3 -c ' + '\'import sys;\
                sys.path.append("' + CodesPath + '");\
                from PLSr1_CZ_Random_CategoryFeatures_partialCorr import PLSr1_KFold_RandomCV_MultiTimes_Sub; \
                import os;\
                import scipy.io as sio;\
                Configuration = sio.loadmat("' + ResultantFolder_TimeI + '/Configuration.mat");\
                Subjects_Data_Mat_Path = Configuration["Subjects_Data_Mat_Path"];\
                Subjects_Score = Configuration["Subjects_Score"];\
                Covariates = Configuration["Covariates"];\
                Fold_Quantity = Configuration["Fold_Quantity"];\
                ComponentNumber_Range = Configuration["ComponentNumber_Range"];\
                ResultantFolder_TimeI = Configuration["ResultantFolder_TimeI"];\
                Permutation_Flag = Configuration["Permutation_Flag"];\
                RandIndex_File = Configuration["RandIndex_File"];\
                Parallel_Quantity = Configuration["Parallel_Quantity"];\
                PLSr1_KFold_RandomCV_MultiTimes_Sub(Subjects_Data_Mat_Path[0], Subjects_Score[0], Covariates, Fold_Quantity[0][0], ComponentNumber_Range[0], 20, ResultantFolder_TimeI[0], Parallel_Quantity[0][0], Permutation_Flag[0][0], RandIndex_File)\' ';
            system_cmd = system_cmd + ' > "' + ResultantFolder_TimeI + '/Time_' + str(i) + '.log" 2>&1\n'
            Finish_File.append(ResultantFolder_TimeI + '/Res_NFold.mat');
            script = open(ResultantFolder_TimeI + '/script.sh', 'w');      
            # # Submit jobs
            script.write('#!/bin/bash\n');
            #script.write('#SBATCH --job-name=ridge' + str(i) + '\n');
            script.write('#SBATCH --job-name=permR' + str(i) + '\n');
            script.write('#SBATCH --nodes=1\n');
            script.write('#SBATCH --ntasks=1\n');
            script.write('#SBATCH --cpus-per-task=4\n');
            script.write('#SBATCH --mem-per-cpu=5G\n');
            script.write('#SBATCH -p q_fat_c\n');
            script.write('#SBATCH -q high_c\n');
            script.write('#SBATCH -o ' + ResultantFolder_TimeI + '/job.%j.out\n');
            script.write('#SBATCH -e ' + ResultantFolder_TimeI + '/job.%j.error.txt\n\n');
            script.write(system_cmd);
            script.close();
            os.system('chmod +x ' + ResultantFolder_TimeI + '/script.sh');
            os.system('sbatch ' + ResultantFolder_TimeI + '/script.sh');
            # # Submit jobs
            # Option = ' -V -o "' + ResultantFolder_TimeI + '/RandomCV_' + str(i) + '.o" -e "' + ResultantFolder_TimeI + '/RandomCV_' + str(i) + '.e" ';
            # #os.system('chmod +x ' + ResultantFolder_TimeI + '/script.sh');
            # os.system(' -l h_vmem=10G,s_vmem=10G -q ' + Queue + ' -N RandomCV_' + str(i) + Option + ResultantFolder_TimeI + '/script.sh')  
            # #os.system('qsub -l h_vmem=10G ' + ResultantFolder_TimeI + '/script.sh')          

def PLSr1_KFold_RandomCV_MultiTimes_Sub(Subjects_Data_Mat_Path, Subjects_Score, Covariates, Fold_Quantity, ComponentNumber_Range, CVRepeatTimes, ResultantFolder, Parallel_Quantity, Permutation_Flag, RandIndex_File=''):

    data = sio.loadmat(Subjects_Data_Mat_Path);
    Subjects_Data = data['Subjects_Data'];

    PLSr1_KFold_RandomCV(Subjects_Data, Subjects_Score, Covariates, Fold_Quantity, ComponentNumber_Range, CVRepeatTimes, ResultantFolder, Parallel_Quantity, Permutation_Flag, RandIndex_File);

def PLSr1_KFold_RandomCV(Subjects_Data, Subjects_Score, Covariates, Fold_Quantity, ComponentNumber_Range, CVRepeatTimes_ForInner, ResultantFolder, Parallel_Quantity, Permutation_Flag, RandIndex_File=''):

    if not os.path.exists(ResultantFolder):
        os.makedirs(ResultantFolder)
    Subjects_Quantity = len(Subjects_Score)
    EachFold_Size = np.int(np.fix(np.divide(Subjects_Quantity, Fold_Quantity)))
    Remain = np.mod(Subjects_Quantity, Fold_Quantity)
    if len(RandIndex_File) == 0:
        RandIndex = np.arange(Subjects_Quantity)
        np.random.shuffle(RandIndex)
    else:
        tmpData = sio.loadmat(RandIndex_File[0])
        RandIndex = tmpData['RandIndex'][0];
    RandIndex_Mat = {'RandIndex': RandIndex}
    sio.savemat(ResultantFolder + '/RandIndex.mat', RandIndex_Mat);
    
    Fold_Corr = [];
    Fold_MAE = [];
    Fold_Weight = [];
    
    Features_Quantity = np.shape(Subjects_Data)[1]
    for j in np.arange(Fold_Quantity):
        Fold_J_Index = RandIndex[EachFold_Size * j + np.arange(EachFold_Size)]
        if Remain > j:
            Fold_J_Index = np.insert(Fold_J_Index, len(Fold_J_Index), RandIndex[EachFold_Size * Fold_Quantity + j])
        
        Subjects_Data_test = Subjects_Data[Fold_J_Index, :]
        Subjects_Score_test = Subjects_Score[Fold_J_Index]
        Covariates_test = Covariates[Fold_J_Index, :]
        
        Subjects_Data_train = np.delete(Subjects_Data, Fold_J_Index, axis=0)
        Subjects_Score_train = np.delete(Subjects_Score, Fold_J_Index) 
        Covariates_train = np.delete(Covariates, Fold_J_Index, axis=0)
        
        #Convert categorical features into one-zero
        enc = preprocessing.OneHotEncoder(sparse=False, handle_unknown='ignore')
        Subjects_Data_train = enc.fit_transform(Subjects_Data_train)
        Subjects_Data_test = enc.transform(Subjects_Data_test)

        if Permutation_Flag:
            # If do permutation, the training scores should be permuted, while the testing scores remain
            Subjects_Index_Random = np.arange(len(Subjects_Score_train))
            np.random.shuffle(Subjects_Index_Random)
            Subjects_Score_train = Subjects_Score_train[Subjects_Index_Random]
            if j == 0:
                PermutationIndex = {'Fold_0': Subjects_Index_Random}
            else:
                PermutationIndex['Fold_' + str(j)] = Subjects_Index_Random

        Optimal_ComponentNumber, Inner_Corr, Inner_MAE_inv = PLSr1_OptimalComponentNumber_KFold(Subjects_Data_train, Subjects_Score_train, Fold_Quantity, ComponentNumber_Range, CVRepeatTimes_ForInner, ResultantFolder, Parallel_Quantity)

        clf = cross_decomposition.PLSRegression(n_components = Optimal_ComponentNumber)
        clf.fit(Subjects_Data_train, Subjects_Score_train)
        Fold_J_Score = clf.predict(Subjects_Data_test)
        Fold_J_Score = np.transpose(Fold_J_Score)[0]

        ## construct covariates
        c = {"predict": Fold_J_Score,
             "true": Subjects_Score_test,
             "age": Covariates_test[:, 0],
             "sex": Covariates_test[:, 1],
             "fd": Covariates_test[:, 2],
             "site": Covariates_test[:, 3]}

        data_temp = pd.DataFrame(c)
        dummySite = pd.get_dummies(data_temp['site'])
        covNum = data_temp['site'].unique()
        if covNum.shape[0] == 22:
            # add 21 sites
            siteNum = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11',
                                 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22']
            covar=['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11',
                                 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'c22','age','sex','fd']
        else:
            siteNum = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11',
                                 'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21',]
            covar = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11',
                     'c12', 'c13', 'c14', 'c15', 'c16', 'c17', 'c18', 'c19', 'c20', 'c21', 'age', 'sex', 'fd']

        dummySite.columns=siteNum
        data_cov = pd.concat((data_temp, dummySite), axis=1)
        # partial correlation
        stat = pg.partial_corr(data=data_cov, x='true', y='predict',
                               covar=covar)
        PartR = np.array(stat['r'])[0]

        #Fold_J_Corr = np.corrcoef(Fold_J_Score, Subjects_Score_test)
        Fold_J_Corr = PartR
        #Fold_J_Corr = Fold_J_Corr[0,1]
        Fold_Corr.append(Fold_J_Corr)
        Fold_J_MAE = np.mean(np.abs(np.subtract(Fold_J_Score,Subjects_Score_test)))
        Fold_MAE.append(Fold_J_MAE)
        
        # get one-hot feature weight
        Weight = clf.coef_ / np.sqrt(np.sum(clf.coef_ **2))          
        feature_weight_file = pd.DataFrame({'feature_names': enc.get_feature_names_out(),
                                             'coef': np.squeeze(clf.coef_)})
                                             
        feature_weight_file.to_csv(ResultantFolder + '/feature_weight_'  + 'partial_corr_' + str(round(PartR, 5)) + '_fold' +str(j) +'_' + str(datetime.now().strftime('%Y_%m_%d')) + '.csv')
        
        Fold_J_result = {'Index':Fold_J_Index, 'Test_Score':Subjects_Score_test, 'Predict_Score':Fold_J_Score, 'Corr':Fold_J_Corr, 'MAE':Fold_J_MAE, 'ComponentNumber':Optimal_ComponentNumber, 'Inner_Corr':Inner_Corr, 'Inner_MAE_inv':Inner_MAE_inv, 'w_Brain':Weight}
        Fold_J_FileName = 'Fold_' + str(j) + '_Score.mat'
        ResultantFile = os.path.join(ResultantFolder, Fold_J_FileName)
        sio.savemat(ResultantFile, Fold_J_result)

    Fold_Corr = [0 if np.isnan(x) else x for x in Fold_Corr]
    Mean_Corr = np.mean(Fold_Corr)
    Mean_MAE = np.mean(Fold_MAE)
    Res_NFold = {'Mean_Corr':Mean_Corr, 'Mean_MAE':Mean_MAE};
    ResultantFile = os.path.join(ResultantFolder, 'Res_NFold.mat')
    sio.savemat(ResultantFile, Res_NFold)
    
    if Permutation_Flag:
        sio.savemat(ResultantFolder + '/PermutationIndex.mat', PermutationIndex)

    return (Mean_Corr, Mean_MAE)  

def PLSr1_OptimalComponentNumber_KFold(Training_Data, Training_Score, Fold_Quantity, ComponentNumber_Range, CVRepeatTimes, ResultantFolder, Parallel_Quantity):
   
    if not os.path.exists(ResultantFolder):
        os.makedirs(ResultantFolder);
 
    Subjects_Quantity = len(Training_Score)
    Inner_EachFold_Size = np.int(np.fix(np.divide(Subjects_Quantity, Fold_Quantity)));
    Remain = np.mod(Subjects_Quantity, Fold_Quantity);    

    Inner_Corr_Mean = np.zeros((CVRepeatTimes, len(ComponentNumber_Range)))
    Inner_MAE_inv_Mean = np.zeros((CVRepeatTimes, len(ComponentNumber_Range)))
    ComponentNumber_Quantity = len(ComponentNumber_Range)
    for i in np.arange(CVRepeatTimes):
        
        RandIndex = np.arange(Subjects_Quantity)
        np.random.shuffle(RandIndex)

        Inner_Corr = np.zeros((Fold_Quantity, len(ComponentNumber_Range)))
        Inner_MAE_inv = np.zeros((Fold_Quantity, len(ComponentNumber_Range)))
        ComponentNumber_Quantity = len(ComponentNumber_Range)

        for k in np.arange(Fold_Quantity):

            Inner_Fold_K_Index = RandIndex[Inner_EachFold_Size * k + np.arange(Inner_EachFold_Size)]
            if Remain > k:
                Inner_Fold_K_Index = np.insert(Inner_Fold_K_Index, len(Inner_Fold_K_Index), RandIndex[Inner_EachFold_Size * Fold_Quantity + k])

            Inner_Fold_K_Data_test = Training_Data[Inner_Fold_K_Index, :]
            Inner_Fold_K_Score_test = Training_Score[Inner_Fold_K_Index]
            Inner_Fold_K_Data_train = np.delete(Training_Data, Inner_Fold_K_Index, axis = 0)
            Inner_Fold_K_Score_train = np.delete(Training_Score, Inner_Fold_K_Index);

            Scale = preprocessing.MinMaxScaler()
            Inner_Fold_K_Data_train = Scale.fit_transform(Inner_Fold_K_Data_train);
            Inner_Fold_K_Data_test = Scale.transform(Inner_Fold_K_Data_test); 
   
            Parallel(n_jobs=Parallel_Quantity,backend="threading")(delayed(PLSr1_SubComponentNumber)(Inner_Fold_K_Data_train, Inner_Fold_K_Score_train, Inner_Fold_K_Data_test, Inner_Fold_K_Score_test, ComponentNumber_Range[l], l, ResultantFolder) for l in np.arange(len(ComponentNumber_Range)))        
        
            for l in np.arange(ComponentNumber_Quantity):
                print(l)
                ComponentNumber_l_Mat_Path = ResultantFolder + '/ComponentNumber_' + str(l) + '.mat';
                ComponentNumber_l_Mat = sio.loadmat(ComponentNumber_l_Mat_Path)
                Inner_Corr[k, l] = ComponentNumber_l_Mat['Corr'][0][0]
                Inner_MAE_inv[k, l] = ComponentNumber_l_Mat['MAE_inv']
                os.remove(ComponentNumber_l_Mat_Path)
            
            Inner_Corr = np.nan_to_num(Inner_Corr)
        Inner_Corr_Mean[i, :] = np.mean(Inner_Corr, axis = 0)
        Inner_MAE_inv_Mean[i, :] = np.mean(Inner_MAE_inv, axis = 0)
    Inner_Corr_CVMean = np.mean(Inner_Corr_Mean, axis = 0)
    Inner_MAE_inv_CVMean = np.mean(Inner_MAE_inv_Mean, axis = 0)
    Inner_Corr_CVMean = (Inner_Corr_CVMean - np.mean(Inner_Corr_CVMean)) / np.std(Inner_Corr_CVMean)
    Inner_MAE_inv_CVMean = (Inner_MAE_inv_CVMean - np.mean(Inner_MAE_inv_CVMean)) / np.std(Inner_MAE_inv_CVMean)
    Inner_Evaluation = Inner_Corr_CVMean + Inner_MAE_inv_CVMean
    
    Inner_Evaluation_Mat = {'Inner_Corr':Inner_Corr, 'Inner_MAE_inv':Inner_MAE_inv, 'Inner_Corr_CVMean': Inner_Corr_CVMean, 'Inner_MAE_inv_CVMean': Inner_MAE_inv_CVMean, 'Inner_Evaluation':Inner_Evaluation}
    sio.savemat(ResultantFolder + '/Inner_Evaluation.mat', Inner_Evaluation_Mat)
    
    Optimal_ComponentNumber_Index = np.argmax(Inner_Evaluation) 
    Optimal_ComponentNumber = ComponentNumber_Range[Optimal_ComponentNumber_Index]
    return (Optimal_ComponentNumber, Inner_Corr, Inner_MAE_inv)

def PLSr1_SubComponentNumber(Training_Data, Training_Score, Testing_Data, Testing_Score, ComponentNumber, ComponentNumber_ID, ResultantFolder):
    clf = cross_decomposition.PLSRegression(n_components=ComponentNumber)
    clf.fit(Training_Data, Training_Score)
    Predict_Score = clf.predict(Testing_Data)
    Predict_Score = np.transpose(Predict_Score)[0]
    Corr = np.corrcoef(Predict_Score, Testing_Score)
    Corr = Corr[0,1]
    MAE_inv = np.divide(1, np.mean(np.abs(Predict_Score - Testing_Score)))
    result = {'Corr': Corr, 'MAE_inv':MAE_inv}
    ResultantFile = ResultantFolder + '/ComponentNumber_' + str(ComponentNumber_ID) + '.mat'
    sio.savemat(ResultantFile, result)
    

