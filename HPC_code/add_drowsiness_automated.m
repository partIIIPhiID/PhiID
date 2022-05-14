function add_drowsiness_automated(datapath, elecA, elecB, performancepath, savepath, savename)
%takes cross participant performance data and adds a drowsiness column to
%each participant
    olddata = load(sprintf('%sdata_%i%i_cross.mat', datapath, elecA, elecB));
    metrics = ["rtr" "rts" "rtx" "rty" "str" "sts" "stx" "sty" "xtr" "xts" "xtx" "xty" "ytr" "yts" "ytx" "yty"]
    chunks = ["pre1" "pre2" "post1" "post2"]
    for k = 1:1:4
      chunk = chunks(k)
      for j = 1:1:16
        newdata = olddata.atoms;
        length = 0;
        struc4csv.metric = [];
        struc4csv.performance = [];
        struc4csv.drowsiness = [];
        metric = metrics(j)
        for i = 1:1:60
            try
                newdata(i).drowsiness = [];
                newdata(i).performance = [];
                Y = readmatrix(sprintf('performance_data/final_good_epochs_%i', i));
                drowsiness = load(sprintf('%sSubject_%i_MicromeasureSplit_for_each_trial', performancepath, i));
                x = drowsiness.Micromeasure_split(:,1);
                xlength = size(x);
                Ylength = size(Y);
                newdata(i).drowsiness = zeros(Ylength(1), 1);
                newdata(i).performance = zeros(Ylength(1), 1);
                for k = 1:1:xlength(1)
                    for j = 1:1:Ylength(1)
                        if x(k) == Y(j)
                            newdata(i).drowsiness(j) = drowsiness.Micromeasure_split(k, 5);
                            newdata(i).performance(j) = drowsiness.Micromeasure_split(k, 3);
                        end
                    end
                end
                struc4csv.metric = [struc4csv.metric; zeros(Ylength(1), 1)];
                for index = 1:1:Ylength(1)
                    struc4csv.metric(index + length) = newdata(i).(chunk)(index).(metric);
                end
                drow_words = ["throwaway" "awake" "light drowsy" "heavy drowsy"];
                perf_words = ["throwaway" "hit" "miss"];
                disp([newdata(i).performance, newdata(i).drowsiness])
                struc4csv.performance = [struc4csv.performance, perf_words(newdata(i).performance + 1)];
                struc4csv.drowsiness = [struc4csv.drowsiness, drow_words(newdata(i).drowsiness + 1)];
                disp(struc4csv)
                length_vec = size(struc4csv.metric);
                disp(length_vec)
                length = length_vec(1);
                disp(length)
            catch err
                disp(err)
            end
        end
        struc4csv.performance = transpose(struc4csv.performance);
        struc4csv.drowsiness = transpose(struc4csv.drowsiness);
        writetable(struct2table(struc4csv), sprintf('%s%s_%i%i_%s_%s.csv', savepath, savename, elecA, elecB, metric, chunk));
  end
end