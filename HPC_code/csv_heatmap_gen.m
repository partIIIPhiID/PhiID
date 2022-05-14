function [csv_for_heatmap] = csv_heatmap_gen(filepath, savepath, min, max, zzz, chunk)
%loads data files of specified syntax, performs statistical tests and saves
%data to a table automatically, saves table as csv in savepath
length = (max - min + 1)*(max - min + 1);
csv_for_heatmap = zeros(length, 6);
csv_for_heatmap(:,1) = 65 + floor((0:1:16*16 - 1)/16);
csv_for_heatmap(:,2) = 65 + mod((0:1:16*16 - 1), 16);
    for x = min:1:max
        for y = x+1:1:max
            data = load(sprintf('%sdata_%i%i_cross.mat', filepath, x, y));
            for participant = 1:1:60
                try
                    T = readmatrix(sprintf('/home/ae431/performance_data/Original_epochs_pilot_%i', participant));
                    Y = readmatrix(sprintf('/home/ae431/performance_data/final_good_epochs_%i', participant));
                    performance = T(Y,3);
                    length = size(data.atoms(participant).(chunk));
                    hits = []; misses = [];
                    for j = 1:1:length(2)
                        if performance(j) == 1
                            hits = [hits, data.atoms(participant).(chunk)(j).(zzz)];
                        else
                            misses = [misses, data.atoms(participant).(chunk)(j).(zzz)];
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
            [h,p] = ttest2(hits,misses);
            a = (analysis.hits.mean - analysis.misses.mean);
            b = (sqrt(analysis.misses.std^2 + analysis.hits.std^2));
            stdnorm_a = a/b;
            meannorm_a = a*(hitlength+misslength)/(mean(abs(hits))*hitlength+mean(abs(misses))*misslength);
            csv_for_heatmap((16*(x - min) + (y - min) + 1), 3) = a;
            csv_for_heatmap((16*(y - min) + (x - min) + 1), 3) = a;
            csv_for_heatmap((16*(x - min) + (y - min) + 1), 4) = stdnorm_a;
            csv_for_heatmap((16*(y - min) + (x - min) + 1), 4) = stdnorm_a;
            csv_for_heatmap((16*(x - min) + (y - min) + 1), 5) = meannorm_a;
            csv_for_heatmap((16*(y - min) + (x - min) + 1), 5) = meannorm_a;
            csv_for_heatmap((16*(x - min) + (y - min) + 1), 6) = b;
            csv_for_heatmap((16*(y - min) + (x - min) + 1), 6) = b;
            csv_for_heatmap((16*(x - min) + (y - min) + 1), 7) = p;
            csv_for_heatmap((16*(y - min) + (x - min) + 1), 7) = p;
            disp(x)
            disp(y)
            disp(h)
        end
    end
    savename = sprintf('%scsv_for_heatmap_%i%i_%s%s.csv',savepath, min, max, zzz, chunk);
    writematrix(csv_for_heatmap,savename) 
 end