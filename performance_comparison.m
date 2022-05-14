function [hits, misses] = performance_comparison(performance_path, performance_name, filename, filepath, zzz, chunk)
%this function would run faster if hits and misses were preallocated by
%number of total hits
%chunk and zzz refer to field names, e.g pre1, rtr respectively
    T = readmatrix(sprintf('%s%s', performance_path, performance_name));
    performance = T(:,3);
        for i = 2:1:size(electrodes, 2)
           if task_id < i
                data = altered_main(electrodes(i), electrodes(task_id), filename, filepath); %fix this line
                length = size(data.atoms.(chunk));
                hits = zero(1,length(2)); misses = hits;
                for j = 1:1:length(2)
                    if performance(j) == 1
                        hits(j) = data.atoms.(chunk)(j).(zzz);
                    else
                        misses(j) = data.atoms.(chunk)(j).(zzz);
                    end
                end
            end
         end
 end
    
   
    
    
  