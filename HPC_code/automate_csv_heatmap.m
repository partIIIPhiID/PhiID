function automate_csv_heatmap(filepath, savepath, min, max, chunk, index)
   zzz = ["rtr" "rtx" "rty" "rts" "str" "stx" "sty" "sts" "xtr" "xtx" "xty" "xts" "ytr" "ytx"' "yty" "yts"];
   csv_heatmap_gen(filepath, savepath, min, max, zzz(index), chunk)
end