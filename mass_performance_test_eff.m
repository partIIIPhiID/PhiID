function mass_performance_test_eff(task_id, a, n, electrodes, filename, filepath, performance_path, performance_name, zzz, chunk)
%job is split into n chunks, electrode vector is of length a
%this function would run faster if hits and misses were preallocated by
%number of total hits
%chunk and zzz refer to field names, e.g pre1, rtr respectively
%This version of mass_performance_test is built for more efficient chunking
    T = readmatrix(sprintf('%s%s', performance_path, performance_name));
    performance = T(:,3);
    success_folder = '/rds/user/ae431/hpc-work/PhiID_results/success/';
    fail_folder = '/rds/user/ae431/hpc-work/PhiID_results/fail/';
    [i, j] = matrix_chunking(a,a);
    m = 1;
    while task_id - 1 < (m*n)/(a*a) && (m*n)/(a*a) <= task_id
          atoms = performance_test_data(electrodes(i(m)), electrodes(j(m)), filename, filepath);
          length = size(atoms.(chunk));
          hits = []; misses = [];
          for x = 1:1:length(2)
              if performance(x) == 1
                  hits = [hits, atoms.(chunk)(x).(zzz)];
              else
                  misses = [misses, atoms.(chunk)(x).(zzz)];
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
        m = m + 1;
     end
 end