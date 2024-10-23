%% needed demo: id, age, sex, motion, site, race, income, family size,  and others
clear;
abcd_dir = '/Users/zhaoshaoling/Documents/Project/ABCD_indivTopography/BMCmed/step00_newSelection/git_ver/ABCDtable';
%%% demopraphic: age, sex, race, parent edu, income, family size
demo_dir = [abcd_dir '/demo/abcd_p_demo_baseline.csv'];
demoT = readtable(demo_dir); 
%%% longitudinal Track: age, interview date, site_id, rel_family_id
longTrack_dir = [abcd_dir '/demo/abcd_y_lt_baseline.csv'];
longtrackT = readtable(longTrack_dir); 
%%% mri_info: motion
mri_info_dir = [abcd_dir '/imaging/abcd_mrirstv02_baseline_part.csv'];
mriT = readtable(mri_info_dir); 

%% demo: sex, race, 2 parent edu, income, family size
demo_subject_id = demoT.src_subject_id;
demo_sex = demoT.demo_sex_v2; %% sex at birth
demo_race = demoT.race_ethnicity;
demo_parent1_edu = demoT.demo_prnt_ed_v2;
demo_parent2_edu = demoT.demo_prtnr_ed_v2;
demo_income = demoT.demo_comb_income_v2;
demo_familysize = demoT.demo_roster_v2;

%% longitudinal track: age, date, site_id, rel_family_id
long_subject_id = longtrackT.src_subject_id;
long_age = longtrackT.interview_age;
long_date = longtrackT.interview_date;
long_site = longtrackT.site_id_l;
long_familyid = longtrackT.rel_family_id;

%% mri_info: motion
mri_subject_id = mriT.src_subject_id;
mri_motion = mriT.rsfmri_var_meanmotion;

%% merge all the used subject_id
load subject_id_s01Passed.mat;
used_subject_id = intersect(demo_subject_id, long_subject_id);
used_subject_id = intersect(used_subject_id, mri_subject_id);
used_subject_id = intersect(used_subject_id, subject_id_s01Passed); %% n=6004

%%
[~, loc_mri] = ismember(used_subject_id, mri_subject_id);

%% get used table information
demo_table = table(demoT.src_subject_id, demoT.demo_sex_v2, demoT.race_ethnicity, demoT.demo_prnt_ed_v2, demoT.demo_prtnr_ed_v2, demoT.demo_comb_income_v2, demoT.demo_roster_v2,...
    'VariableNames', {'subject_id', 'sex', 'race', 'parent1_edu', 'parent2_edu', 'income', 'family_size'});
long_table = table(longtrackT.src_subject_id, longtrackT.interview_age, longtrackT.interview_date, longtrackT.site_id_l, longtrackT.rel_family_id,...
    'VariableNames', {'subject_id', 'age', 'interview_date', 'site_id', 'real_family_id'});

mri_table_used = table(mriT.src_subject_id(loc_mri), mriT.rsfmri_var_meanmotion(loc_mri), 'VariableNames', {'subject_id', 'motion'});

mergedTable_demo_long = join(demo_table, long_table, 'Keys', 'subject_id'); 
mergedTable_demo_long_mri = join(mri_table_used, mergedTable_demo_long, 'Keys', 'subject_id');
mergedTable_used = mergedTable_demo_long_mri;

writetable(mergedTable_used,  [abcd_dir '/abcd_demo_merged.csv']);






