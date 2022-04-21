import os
import json
from flask import Flask, request
from threading import Thread # flask app.run() blocks so we want to run it on its own thread
import ReceiptConsumer

# Ngrok Binding For Python, so our flask endpoint will be accessible from the general internet
from pyngrok import ngrok, conf
import time

HTTP_LISTEN_PORT = 8086

#### FLASK STUFF #####
app = Flask(__name__)

@app.route('/dr', methods=['POST'])
def receive_dr():
    print('======================================================\ndelivery receipt endpoint hit!\n', json.dumps(request.json, indent=4))
    ReceiptConsumer.handleMessage(request.json)
    return "OK"


def start_app() -> (str, Thread):
    #### NGROK STUFF ######
    # https://dashboard.ngrok.com/get-started/your-authtoken
    ngrok_conf = conf.get_default().auth_token = os.getenv("NGROK_TOKEN")
    http_tunnel = ngrok.connect(addr=HTTP_LISTEN_PORT, bind_tls=True, conf=ngrok_conf)
    public_url = http_tunnel.public_url
    print("Public URL: ", public_url)
    # Start in own thread to not block main thread, use_reloader needs to be false due to reloader expecting to be in main thread
    flask_thread: Thread = Thread(target=lambda: app.run(host='0.0.0.0', port=HTTP_LISTEN_PORT, use_reloader=False))
    flask_thread.start()
    time.sleep(0.5) # wait a bit for flask to start up before returning
    return public_url, flask_thread
