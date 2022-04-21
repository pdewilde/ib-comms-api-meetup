# IB Comms API Meetup
## A talk on delivery reports

[Philadelphia Event](https://www.meetup.com/philadelphia-software-developers/events/283711560/)

[New York Event](https://www.meetup.com/infobip-developers/events/283710372/)

### About this Talk

I gave a talk about SMS Delivery Reports, and included a live demo showing how an SMS delivery report could be handled. 
This repo contains the code for my demo as well as the slides from my talk. The idea was to keep things simple, so here
is what you need to know:

#### Account Setup
You will need an api key and api prefix, both of which can be found at https://portal.infobip.com 
(blue link at bottom of login page to make a free account!)

I ran this as a demo on my laptop, so I didn't have a dedicated IP, and used a free https://ngrok.com/ account to 
accept callbacks. You will need an authtoken which you can get once signing up.




Talk modified from previous blog post:

https://dev.to/omtechblog/how-to-properly-process-a-delivery-receipt-36bd

### Environment Setup
```
$ git clone git@github.com:pdewilde/ib-comms-api-meetup.git
$ cd ib-comms-api-meetup
$ python3 –m venv demo
$ source demo/bin/activate  # "$ deactivate" to leave venv
$ pip3 install wheel
$ pip3 install –r requirements.txt
$ # put your api prefix in url (replce "prefix" with your prefix -- can be found on your infobip acct)
$ sed -i 's/api\.infobip\.com/prefix.api.infobip.com/g' src/MeetupTalk.py
$ export API_KEY="your_api_key"
$ export NGROK_TOKEN="your_ngrok_token"
```

####Environment Setup -- Receipt Printer
This talk used a receipt printer to demonstrate receiving a delivery receipt (I know, a very original pun). If you 
don't have one, its easy to modify ReceiptConsumer.py by removing anything mentioning the variable "p" and doing 
something else with the delivery report. Here are the steps I used to set up my receipt printer plugged in via USB: 
(Epson TM-T88V Model 
M244A):

######Find the usb device
```
$ lsusb
...
Bus 001 Device 009: ID 04b8:0202 Seiko Epson Corp. Interface Card UB-U05 for Thermal Receipt Printers [M129C/TM-T70/TM-T88IV]
...
```
We are interested in the vendor id and the product id, which are shown separated by a `:`. In my case the vendor id is `04b8` and the product id is `0202`.

###### Create group and udev rule to give group access to device (substitute your vendor and product id)
```
$ sudo groupadd usbusers
$ sudo addgroup <YOUR_USERNAME_HERE> usbusers
$ sudo sh -c  'echo "SUBSYSTEM==\"usb\", ATTRS{idVendor}==\"04b8\", ATTRS{idProduct}==\"0202\", MODE=\"0664\", GROUP=\"usbusers\"" > /etc/udev/rules.d/99-escpos.rules'
```

###### Reboot Computer to reload udev rules
In theory this can be done without a reboot, but I've never been able to get it to work.

### Using

You will need to put your phone number you used to sign up for your account, replace in `src/MeeupTalk.py`:
"13605551234" with your phone number in international format (no +).

Assuming your environment is setup correctly, it should be as simple as
```$ python3 src/MeetupTalk.py```

### Files
`src/MeetupTalk.py` -- Main entrypoint. Starts webapp and receipt consumer, then sends an SMS

`src/ReceiptConsumer.py` -- Sets up receipt printer and prints delivery reports

`src/WebApp.py` -- Sets up flask webapp listening through a ngrok tunnel for a delivery report on the /dr path

`requirements.txt` -- Python requirements file

`ib_logo.webp` -- Only 896 bytes! I thought that was pretty cool

`README.md` -- recursion
