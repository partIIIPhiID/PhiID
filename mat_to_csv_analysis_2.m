function mat_to_csv_analysis(filename, filepath, savename, savepath)
    FileData = load(sprintf('%s%s.mat', filepath, filename));
    largeStruct = repmat(FileData.analysis,2,1);
    table = struct2table(largeStruct);
    writetable(table(1,:), sprintf('%s%s.csv', savepath, savename));
end