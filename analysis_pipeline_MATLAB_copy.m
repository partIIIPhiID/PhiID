function analysis_pipeline_MATLAB(task_id, electrodes, filename, filepath, performance_path, performance_name, zzz, chunk)
%this function would run faster if hits and misses were preallocated by
%number of total hits
%chunk and zzz refer to field names, e.g pre1, rtr respectively
    T = readmatrix(sprintf('%s%s', performance_path, performance_name));
    performance = T(:,3);
    save_folder = '/rds/user/ae431/hpc-work/PhiID_results/to_analyse/';
    for i = 2:1:size(electrodes, 2)
           if task_id < i
                atoms = performance_test_data(electrodes(i), electrodes(task_id), filename, filepath);
                length = size(atoms.(chunk));
                hits = []; misses = [];
                for j = 1:1:length(2)
                    if performance(j) == 1
                        hits(j) = atoms.(chunk)(j).(zzz);
                    else
                        misses(j) = atoms.(chunk)(j).(zzz);
                    end
                end
                analysis = []
                analysis.hits = hits(:);
                analysis.misses = misses(:);
                save(sprintf('%sanalysis_%d%d_%s%s_%s.mat', save_folder, electrodes(i), electrodes(task_id), chunk, zzz, filename), 'analysis')
           end
           
          
     end
 end
    
   