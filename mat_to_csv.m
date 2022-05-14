function mat_to_csv(filename, filepath, savename, savepath)
    FileData = load(sprintf('%s%s.mat', filepath, filename));
    writetable(struct2table(FileData.atoms.pre1), sprintf('%s%s.csv', savepath, savename));
end