%% get subjects ADI(Area Deprivation Index) from led_l_adi provided by ABCD
clear;
work_dir = '/Users/zhaoshaoling/Documents/Project/ABCD_indivTopography/BMCmed/step00_newSelection/';
demoArranged = readtable([work_dir '/ABCD_table/abcd_demo_merged_n6001_withoutsibilings.csv']);
demo_subject_id = demoArranged.subject_id;

%%
ADI_table = readtable([work_dir '/ABCD_table/demo/led_l_adi.csv']);
ADI_index1 = ADI_table.reshist_addr1_adi_wsum;
ADI_index2 = ADI_table.reshist_addr1_adi_perc;
ADI_subject_id = ADI_table.src_subject_id;

%%
used_subject_id = intersect(demo_subject_id, ADI_subject_id);
[~, loc_demo] = ismember(used_subject_id, demo_subject_id);
[~, loc_adi] = ismember(used_subject_id, ADI_subject_id);

used_demo = demoArranged(loc_demo,:);
used_adi = [ADI_index1(loc_adi,:), ADI_index2(loc_adi,:)];
used_adi = table(used_adi(:,1), used_adi(:,2), 'VariableNames', {'reshist_addr1_adi_wsum', 'reshist_addr1_adi_perc'});
used_table = [used_demo, used_adi];

writetable(used_table, [work_dir '/ABCD_table5/abcd_demo_merged_forADI.csv']);
