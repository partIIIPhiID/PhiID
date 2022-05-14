%take 2 electrodes from the eeg array and compute phiID metrics do this
%across participants
function main_crosspart(electrode_a, electrode_b, filepath, range)
    addpath ~/tools/eeglab; eeglab nogui;
    addpath ~/tools/fieldtrip; ft_defaults;
    %participants are in numbered files with set prefixes and suffixes
    parfor participant = range
        prefix = 'AuMa_';
        suffix = '_filtd_avgd_epochd_importID_epdeleted_ICA_pruned_interp_avgd.set';
        try
            data = loadfilename(sprintf('%s%s%i%s',filepath,prefix,participant,suffix));
            [prestim1, prestim2, poststim1, poststim2] = trim_data(electrode_a, electrode_b, data);
            parfor i = 1: +1: size(data, 3)
                atoms(participant).pre1(i) = PhiIDFull(prestim1(:, :, i));
                atoms(participant).pre2(i) = PhiIDFull(prestim2(:, :, i));
                atoms(participant).post1(i) = PhiIDFull(poststim1(:, :, i));
                atoms(participant).post2(i) = PhiIDFull(poststim2(:, :, i));
            end
        catch me
            disp(me)
        end
            
    end
    
    
    results_folder = '/rds/user/ae431/hpc-work/PhiID_results/';
    save(sprintf('%sdata_%d%d_cross.mat', results_folder, electrode_a, electrode_b), 'atoms')
end