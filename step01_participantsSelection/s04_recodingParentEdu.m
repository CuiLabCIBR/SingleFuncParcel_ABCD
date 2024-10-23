%% get parent edu, recoding from category to years and average between two parents
clear;
work_dir = '/Users/zhaoshaoling/Documents/Project/ABCD_indivTopography/BMCmed/step00_newSelection';
demoArranged = readtable([work_dir '/ABCD_table/abcd_demo_merged_n6001_withoutsibilings.csv']); %% remove parent edu invalid
edu1 = demoArranged.parent1_edu;
edu2 = demoArranged.parent2_edu;

%% Re-coding parent education categories to years
%%% edu mapping
mappingTable = containers.Map([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21], ...
    [0,1,2,3,4,5,6,7,8,9,10,11,12,12,12,14,14,14,16,18,20,22]);
%%% get with NaN and 777/999
specialValues = [777,999, NaN];
nanReplacement = NaN;
originalArray1 = edu1;
mappedArray1 = arrayfun(@(x) handleSpecialCases(x, mappingTable, specialValues, nanReplacement), originalArray1);
originalArray2 = edu2;
mappedArray2 = arrayfun(@(x) handleSpecialCases(x, mappingTable, specialValues, nanReplacement), originalArray2);

%% get mean of two parent edu
array1 = mappedArray1; 
array2 = mappedArray2;
% 
meanParentEdu = arrayfun(@(a1, a2) ...
    ifelse(isnan(a1) && ~isnan(a2), a2, ...  
           ifelse(~isnan(a1) && isnan(a2), a1, ...  
           (a1 + a2) / 2)), ...  
    array1, array2);

reCoding_parent_edu = table(meanParentEdu);
demoArranged1 = [demoArranged, reCoding_parent_edu];
writetable(demoArranged1, 'abcd_demo_merged_n6001_withoutsibilings_forEDU_n5308_coverted.csv');

%% 
function out = ifelse(condition, trueValue, falseValue)
    if condition
        out = trueValue;
    else
        out = falseValue;
    end
end

%% 
function out = handleSpecialCases(value, mappingTable, specialValues, nanReplacement) 
    if isnan(value) 
        out = nanReplacement; 
        elseif ismember(value, specialValues) 
            out = NaN; 
            elseif isKey(mappingTable, value) 
                out = mappingTable(value); 
    else 
        out = value; 
    end 
end
