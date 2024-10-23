#!/bin/bash
#SBATCH --job-name=submit
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem-per-cpu=20G
#SBATCH -p q_fat_2
#SBATCH -q high
#SBATCH -o /ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step01_PLSprediction/atlasLoading/bootstrap/job.%j.out
#SBATCH -e /ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step01_PLSprediction/atlasLoading/bootstrap/job.%j.error.txt

rand_ind=$1
echo "perform boostrap: $rand_ind"
python /ibmgpfs/cuizaixu_lab/zhaoshaoling/NMF_NeuronCui/BMCmed/step01_PLSprediction/atlasLoading/bootstrap/Step_1st_Prediction_OverallPsyFactor_RandomCV.py $rand_ind
