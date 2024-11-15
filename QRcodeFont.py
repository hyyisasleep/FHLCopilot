
# https://www.bilibili.com/video/BV1Sm2BY7EoS/
# 二维码字体，但是缺个库跑不通


import io,json,tqdm
import qrcode
data = []
for x in tqdm.tqdm(range(0x4E00,0x9FFF)):
    qr = qrcode.QRCode()
    qr .add_data(chr(x))
    f = io.StringIO()
    qr .print_ascii(out=f)
    f.seek(0)
    data.append(f.read())
with open("han-qrcode.json" ,"w" , encoding="U8") as out:
    out.write(json. dumps(data))



def draw_char(font, code, text):
    glyph = font.createChar(code)
    glyph.width = 1000
    pen = glyph.glyphPen()
    lines = text.split("\n")
    x= 0
    y = 800
    w=1000 / 32
    h = 1000 / 16
    for rid, row in enumerate(lines) :
        y_pos = y - rid * h
        for cid,col in enumerate(row):
            x_pos = x + cid * w
            match col:
                case '▀':
                    draw_box(pen, x_pos, y_pos, w , -w)
                case '█':
                    draw_box(pen,x_pos, y_pos,w,-w* 2)
                case '▄' :
                    draw_box(pen,x_pos,y_pos - w, w,-w)
# "https://tw.piliapp.com/symbol/square/"
# 绘制字符中的方块
def draw_box(pen, x, y, w, h):
    pen. moveTo( (x,y))
    pen. lineTo((x + w,y))
    pen . lineTo((x + w,y + h))
    pen. lineTo( (x, y + h))
    pen. closePath()


# 生成字体
import fontforge,json
with open( "han-qrcode.json") as src:
    data = json. load(src)
    font = fontforge.font()
    font.fontname = "QRHan"
    font.fullname = "QRHan"
    font .familyname = "QRHan"
    font.copyright = "Created by Clerk Ma . "
    base = 0x4E00
    for index, text in enumerate(data) :
        code = base + index
        draw_char(font,code,text)
        font.save( "qrcode-han.sfd ")
    font.generate( "qrcode-han.ttf ")

