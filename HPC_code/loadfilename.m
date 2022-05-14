%load filename takes a filename and loads the appropriate matrix for main.m
function data = loadfilename(filename)
    EEGstruc = pop_fileio(filename);
    data = EEGstruc.data;
end