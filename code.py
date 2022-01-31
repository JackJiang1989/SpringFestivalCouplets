# -*- coding: utf-8 -*-

import os
import freetype
import numpy as np
from PIL import Image

FONT_FILE = r'C:\Users\CNJIANGJA\OneDrive - Tetra Pak\desktop\font\SIMLI.TTF'
BG_FILE = r'C:\Users\CNJIANGJA\OneDrive - Tetra Pak\desktop\bg1.png'

def text2image(word, font_file, size=128, color=(0,0,0)):
    """使用指定字库将单个汉字转为图像
    
    word        - 单个汉字字符串
    font_file   - 矢量字库文件名
    size        - 字号，默认128
    color       - 颜色，默认黑色
    """
    
    face = freetype.Face(font_file)
    face.set_char_size(size*size)
    
    face.load_char(word)
    btm_obj = face.glyph.bitmap
    w, h = btm_obj.width, btm_obj.rows
    pixels = np.array(btm_obj.buffer, dtype=np.uint8).reshape(h, w)
    
    dx = int(face.glyph.metrics.horiBearingX/64)
    if dx > 0:
        patch = np.zeros((pixels.shape[0], dx), dtype=np.uint8)
        pixels = np.hstack((patch, pixels))
    
    r = np.ones(pixels.shape) * color[0] * 255
    g = np.ones(pixels.shape) * color[1] * 255
    b = np.ones(pixels.shape) * color[2] * 255
    im = np.dstack((r, g, b, pixels)).astype(np.uint8)
    
    return Image.fromarray(im)

def write_couplets(text, horv='V', quality='L', out_file=None, bg=BG_FILE):
    """写春联
    
    text        - 春联字符串
    bg          - 背景图片路径
    horv        - H-横排，V-竖排
    quality     - 单字分辨率，H-640像素，L-320像素
    out_file    - 输出文件名
    """
    
    size, tsize = (320, 128) if quality == 'L' else (640, 180)
    ow, oh = (size, size*len(text)) if horv == 'V' else (size*len(text), size)
    im_out = Image.new('RGBA', (ow, oh), '#f0f0f0')
    im_bg = Image.open(BG_FILE)
    if size < 640:
        im_bg = im_bg.resize((size, size))
    
    for i, w in enumerate(text):
        im_w = text2image(w, FONT_FILE, size=tsize, color=(0,0,0))
        w, h = im_w.size
        dw, dh = (size - w)//2, (size - h)//2
        
        if horv == 'V':
            im_out.paste(im_bg, (0, i*size))
            im_out.paste(im_w, (dw, i*size+dh), mask=im_w)
        else:
            im_out.paste(im_bg, (i*size, 0))
            im_out.paste(im_w, (i*size+dw, dh), mask=im_w)
    
    im_out.save('%s.png'%text)
    os.startfile('%s.png'%text)

if __name__ == '__main__':
    write_couplets('身体健康', horv='V', quality='H')
    write_couplets('万事如意', horv='V', quality='H')
    write_couplets('虎年大吉', horv='H', quality='H')
