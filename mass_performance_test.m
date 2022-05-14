function mass_performance_test(task_id, electrodes, filename, filepath, performance_path, performance_name, zzz, chunk)
%this function would run faster if hits and misses were preallocated by
%number of total hits
%chunk and zzz refer to field names, e.g pre1, rtr respectively
    T = readmatrix(sprintf('%s%s', performance_path, performance_name));
    performance = T(:,3);
    success_folder = '/rds/user/ae431/hpc-work/PhiID_results/success/';
    fail_folder = '/rds/user/ae431/hpc-work/PhiID_results/fail/';
    for i = 2:1:size(electrodes, 2)
           if task_id < i
                atoms = performance_test_data(electrodes(i), electrodes(task_id), filename, filepath);
                length = size(atoms.(chunk));
                hits = []; misses = [];
                for j = 1:1:length(2)
                    if performance(j) == 1
                        hits = [hits, atoms.(chunk)(j).(zzz)];
                    else
                        misses = [misses, atoms.(chunk)(j).(zzz)];
                    end
                end
                analysis.hits.mean = mean(hits);
                analysis.hits.std = std(hits);
                analysis.misses.mean = mean(misses);
                analysis.misses.std = std(misses);
                simple_test = abs(mean(hits) - mean(misses)) - sqrt(std(hits)^2 - std(misses)^2);
                
                if simple_test > 0
                    save(sprintf('%ssuccess_%d%d_%d%d_%s.mat', success_folder, electrodes(i), electrodes(task_id), chunk, zzz, filename), 'analysis')
                else
                    save(sprintf('%sfail_%d%d_%s.mat', fail_folder, electrodes(i), electrodes(task_id), filename), 'analysis')
                end
           end
           
          
     end
 end
    
   