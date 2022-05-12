import os
from PIL import Image

def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
    return int(size / 1024)

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

def compress_image(infile, outfile='', mb=10000, step=0.01, quality=90):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小   
    """
    o_size = get_size(infile)
    print(o_size)

    if o_size <= mb:
        return infile
    outfile = get_outfile(infile, outfile)
    while o_size > mb:
        im = Image.open(infile)
        im.save(outfile, quality=quality)
        if quality - step < 0:
            break
        quality -= step
        o_size = get_size(outfile)
    return outfile, get_size(outfile)

if __name__ == "__main__":
    pwd=os.getcwd()
    w_path=os.path.join(pwd,"pic")

    target=os.path.join(pwd,"chr")

    for i in os.listdir(w_path):
        if(not i.startswith(".")):
            f=os.path.join(w_path,i)
            tf=os.path.join(target,i)
            compress_image(f,tf)