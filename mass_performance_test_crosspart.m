function mass_performance_test_crosspart(atoms, zzz, chunk)
%this function would run faster if hits and misses were preallocated by
%number of total hits
%chunk and zzz refer to field names, e.g pre1, rtr respectively
%requires local copies of performance_name and atoms
    for participant = 1:1:60
        try
            T = readmatrix(sprintf('Original_epochs_pilot_%i', participant));
            Y = readmatrix(sprintf('final_good_epochs_%i', participant));
            performance = T(Y,3);
            length = size(atoms(participant).(chunk));
            hits = []; misses = [];
            for j = 1:1:length(2)
                if performance(j) == 1
                    hits = [hits, atoms(participant).(chunk)(j).(zzz)];
                else
                    misses = [misses, atoms(participant).(chunk)(j).(zzz)];
                end
            end
        catch err    
            disp(err)
        end 
    end
    hitlength = size(hits);
    misslength = size(misses);
    analysis.hits.mean = mean(hits);
    analysis.hits.std = std(hits)/sqrt(hitlength(2)-1);
    analysis.misses.mean = mean(misses);
    analysis.misses.std = std(misses)/sqrt(misslength(2)-1);
    [h,p] = ttest2(hits,misses, 'Tail', 'left');
    disp(mean(misses) - mean(hits))
    disp(sqrt(analysis.misses.std^2 + analysis.hits.std^2))
    disp(h)
    disp(p)
    save(sprintf('analysis_crosspart_%s_%s.mat', chunk, zzz), 'analysis')
 end