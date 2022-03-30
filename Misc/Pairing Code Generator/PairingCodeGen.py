import math
import qrcode
from PIL import Image, ImageDraw, ImageFont

width, height, border = 666, 900, 73

font_path = './Scancardium_2.0.ttf'
logo_path = './homekitLogo.png'

xurl = 'X-HM://0023ISYWY28A0'
code = "0314\n5154"

parent_img = Image.new("RGBA", (width, height), (255,0,0,0))

# Draw Background
bg_img = ImageDraw.Draw(parent_img)
bg_img.rounded_rectangle((0, 0, width, height), fill="#FFF", outline="#000", width=13, radius=67)

# Apply Logo
logo_img = Image.open(logo_path, mode='r')
logo_img = logo_img.resize((210, 186), Image.ANTIALIAS)
parent_img.paste(logo_img,(border,border))

# Generate QR Code
qr = qrcode.QRCode(border=0)
qr.add_data(xurl)
qr.make(fit=True)
qr_img = qr.make_image()
qr_img = qr_img.resize(((width - (border * 2)),(width - (border * 2))))
parent_img.paste(qr_img, (border,(height - border - (width - (border * 2)))))

# Generate Text
code_img = ImageDraw.Draw(parent_img)
font = ImageFont.truetype(font_path, 120)
code_img.text(((width-border)-290, border), code, font=font, fill=(0, 0, 0))

parent_img.show()
