import math
import qrcode
import re
from PIL import Image, ImageDraw, ImageFont

width, height, border = 666, 900, 73

font_path = './SF-Mono-Bold.otf'
logo_path = './homekitLogo.png'

def getXUrl():
    try:
        xin = input("Enter the X-Callback URL provided by Homebridge: ").upper()
        xurl = re.search('X-HM:\/\/\S{13}$', xin)[0]
        print()
        return xurl
    except Exception as e:
        print('Invalid X-Callback URL provided. Enter a URL that matches this pattern H-HM://0123456789ABC')
        exit()

def getCode():
    try:
        cin = input("Enter the pairing code provided by Homebridge: ")
        code = re.search('\d{3}-*\d{2}-*\d{3}', cin)[0]
        print()
        return code.replace('-','')
    except Exception as e:
        print('Invalid code provided. Enter a code that matches this pattern 123-45-678 or 12345678')
        exit()

def generateImage(xurl,code):

    c = str(code[0:4] + '\n' + code[4:])

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
    code_img.text(((width-border)-290, border/2), c, font=font, fill=(0, 0, 0))

    # Save pairing code image
    try:
        parent_img.show()
        print("Pairing code successfully saved as homebridge_pairing_code.png")
    except:
        print("An error occured while saving the homebridge pairing code")

if __name__ == '__main__':
    print('\nHomebridge Pairing Code Generator\nFor full instructions, see the README on GitHub\nhttps://github.com/austintrujillo/Homebridge-Enclosure-Pi\n')
    xurl = getXUrl()
    code = getCode()
    generateImage(xurl,code)
