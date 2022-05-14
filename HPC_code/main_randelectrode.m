function main_randelectrode(task_id, max_task_id, randpath, filepath, range)
    %loads a list of randomly generated electrode pairs, computes PhiID
    %metrics for 1/max_task_id electrode pairs
    rand_electrodes = readmatrix(sprintf('%srand_electrode_list.csv', randpath));
    length = size(rand_electrodes);
    max_i = task_id*length(1)/max_task_id;
    min_i = (task_id - 1)*length(1)/max_task_id + 1;
    for index = min_i:1:max_i
        main_crosspart(rand_electrodes(index,2), rand_electrodes(index,3), filepath, range)
    end    
        
 