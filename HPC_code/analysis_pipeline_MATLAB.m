function analysis_pipeline_MATLAB(task_id, electrodes, filename, filepath, performance_path, performance_name, good_epochs_name)
%this function calculates the PhiID atoms and adds a new field with
%performance data
    T = readmatrix(sprintf('%s%s', performance_path, performance_name));
    Y = readmatrix(sprintf('%s%s', performance_path, 'final_good_epochs_26'));
    performance = T(Y,3);
    save_folder = '/rds/user/ae431/hpc-work/PhiID_results/datasets/';
    patient_number = string(extractBetween(filename,6,7));
    for i = 2:1:size(electrodes, 2)
           if task_id < i
                dataset = performance_test_data(electrodes(i), electrodes(task_id), filename, filepath);
                dataset.response = transpose(performance);
                save(sprintf('%sdataset_%d%d_%s%s_%s.mat', save_folder, electrodes(i), electrodes(task_id), patient_number), 'dataset')
           end
          
     end
end
 
                    %length = size(dataset.(chunk));
                %dataset.response = [];
                %for j = 1:1:length(2)
                    %if performance(j) == 1
                        %dataset.response(j) = '1';
                    %else
                        %dataset.response(j) = '0';
                    %end
                %end
    
   