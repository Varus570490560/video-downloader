import sys

from analysis import get_m3u8, analysis_m3u8, download, generate_list, merge
if __name__ =='__main__':
    get_m3u8(url=sys.argv[1])
    split = analysis_m3u8(sys.argv[1])
    download(split_count=split)
    generate_list(split_count=split)
    merge(name=sys.argv[2])




