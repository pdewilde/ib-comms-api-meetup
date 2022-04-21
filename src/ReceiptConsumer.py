from escpos.printer import *
from PIL import Image

# Open image from file using PIL and resize to fit printer width
def getImage(fileName):
    MAX_WIDTH = 512
    img = Image.open(fileName)
    wpercent = (MAX_WIDTH / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((MAX_WIDTH, hsize), Image.ANTIALIAS)
    return img

# https://ramonh.dev/2020/09/22/usb-device-linux-startup/
# $ cat /etc/udev/rules.d/99-escpos.rules
# SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0202", MODE="0664", GROUP="usbusers"

## Set up printer using the vendor id and product id gotten with lsusb
p = Usb(0x04b8, 0x0202)

CHARS_PER_LINE=42


def getCurrencyString(currency: str) -> str:
    if (currency == 'EUR'):
        return 'E' # couldn't get euro sign to print :(
    elif (currency == 'USD'):
        return '$'
    else:
        return currency + " "

def splitPad(left:str, right:str, width=CHARS_PER_LINE) -> str:
    return left + (' ' * (width - len(left) - len(right))) + right

def printMessage(smsCount=2, messageId='123456789', pricePerMessage =0.01, currency='EUR', errorId=32, statusName='REJECTED_DESTINATION_NOT_REGISTERED', errorName='EC_DEST_ADDRESS_NOT_IN_SMS_DEMO'):
    p.set()
    p.text(splitPad(f'{messageId} -- SMS Message', f'{getCurrencyString(currency)}{pricePerMessage * smsCount:.2f}') + '\n')
    if (smsCount > 1):
        p.text(f'  {smsCount} @ {getCurrencyString(currency)}{pricePerMessage:.2f} ea\n')
    p.text(f'  {"status" if errorId == 0 else "error"}: {statusName if errorId == 0 else errorName}'[:CHARS_PER_LINE] + '\n')
    return pricePerMessage * smsCount

def handleMessage(message : object):

    p.set() # resets the printer

    p.image(getImage('ib_logo.webp'))
    p.set(align='center', text_type='B')
    p.text("\nDELIVERY RECEIPT\n\n")

    p.set()
    total = 0
    for result in message['results']:
        total = total + printMessage(result['smsCount'], result['messageId'], result['price']['pricePerMessage'], result['price']['currency'], result['error']['id'], result['status']['name'], result['error']['name'])

    p.text('\n' + splitPad("TOTAL", getCurrencyString('EUR') + str(total)) + '\n')

    p.set(align='center')
    p.text('\n' + '-'*CHARS_PER_LINE + '\n')
    p.set(align='left', text_type='B')
    p.text('YOUR PRESENTER TODAY WAS PARKER DEWILDE\n')
    p.set(align='center')
    p.text('-'*CHARS_PER_LINE + '\n')
    p.text('\nTHANK YOU FOR ATTENDING\n')
    p.text('AN INFOBIP MEETUP\n')
    p.text('www.infobip.com\n')

    p.barcode('{BMADEYOULOOK', 'CODE128', function_type="B", pos='OFF')
    p.cut()


def close():
  p.close()