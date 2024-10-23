%%
clear;
abcd_dir = '/Users/zhaoshaoling/Documents/Project/ABCD_indivTopography/BMCmed/step00_newSelection/git_ver/ABCDtable';
abcc_rawFileList = [abcd_dir '/dtseriesNameList_ABCC_n9396.csv']; %% 9396=9480-36(repeated ID)-48(missing nii data)
abcc_rawFile = readtable(abcc_rawFileList, 'Delimiter', ',');
abcc_rawName = abcc_rawFile.subjectkey;

%% get subjects pass rsfMRI QC
mri_qc_fileList = [abcd_dir '/imaging/mri_y_qc_incl_baseline.csv']; 
mri_qc_file = readtable(mri_qc_fileList);
subject_id_qc = mri_qc_file.src_subject_id;
qc_include = mri_qc_file.imgincl_rsfmri_include;
subject_id_qcPassed = subject_id_qc(qc_include==1);
subject_id_qcPassed_inABCC = intersect(subject_id_qcPassed, abcc_rawName);

%% get subjects with mean motion<0.5mm&scan length>20min from abcd
mri_fileList = [abcd_dir '/imaging/abcd_mrirstv02_baseline_part.csv'];
mri_file = readtable(mri_fileList);

ntpoints = mri_file.rsfmri_var_numtrs; %% Number of frames in acquisition
meanmotion = mri_file.rsfmri_var_meanmotion; %% Average framewise displacement in mm
validframe = mri_file.rsfmri_var_subthreshnvols; %% Number of frames with FD < 0.2
subject_id_mri = mri_file.subjectkey; 

%% find subjects with mean motion<0.5mm and valid frame no less than 600
motion_threshold = 0.5;
frame_threshold = 600;
subject_id_motionPassed = subject_id_mri(meanmotion<motion_threshold);
subject_id_motionPassed_inABCC = intersect(subject_id_motionPassed, abcc_rawName); 
subject_id_framePassed = subject_id_mri(validframe>=frame_threshold); %% more than 600 TR with FD<0.2mm
subject_id_framePassed_inABCC = intersect(subject_id_framePassed, abcc_rawName); %

subject_id_qc_motionPassed_inABCC = intersect(subject_id_qcPassed_inABCC, subject_id_motionPassed_inABCC);
subject_id_qc_motion_framePassed_inABCC = intersect(subject_id_framePassed_inABCC, subject_id_qc_motionPassed_inABCC);

%% find subjects with scan length>20min
timepoints_threshold = 1500;
subject_id_timePassed = subject_id_mri(ntpoints>=timepoints_threshold);
subject_id_timePassed_inABCC = intersect(subject_id_timePassed, abcc_rawName); 
subject_id_qc_motion_frame_timePassed_inABCC = intersect(subject_id_qc_motion_framePassed_inABCC, subject_id_timePassed_inABCC);

subject_id_s01Passed = subject_id_qc_motion_frame_timePassed_inABCC;
save('subject_id_s01Passed.mat', 'subject_id_s01Passed');
