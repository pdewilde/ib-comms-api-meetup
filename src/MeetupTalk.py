import WebApp
import os

from infobip_api_client.api.send_sms_api import SendSmsApi
from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.exceptions import ApiException
from infobip_api_client.model.sms_advanced_textual_request import SmsAdvancedTextualRequest
from infobip_api_client.model.sms_destination import SmsDestination
from infobip_api_client.model.sms_response import SmsResponse
from infobip_api_client.model.sms_textual_message import SmsTextualMessage

# See https://github.com/infobip/infobip-api-python-client

###### IB STUFF ######
client_config = Configuration(
    host="gyq536.api.infobip.com",  # Different for every user, see https://portal.infobip.com/homepage/
    api_key={"APIKeyHeader": os.getenv("API_KEY")},
    # Set your API key as an environment variable https://portal.infobip.com/settings/accounts/api-keys
    api_key_prefix={"APIKeyHeader": "App"},  # See https://www.infobip.com/docs/essentials/api-authentication
)

api_client = ApiClient(client_config)

sent_messages = {}

def send_sms_message(message_text: str, destination_address: str, notify_url: str):
    api_instance = SendSmsApi(api_client)
    sms_request = SmsAdvancedTextualRequest(
        messages=[
            SmsTextualMessage(
                destinations=[
                    SmsDestination(
                        to=destination_address,
                    ),
                ],
                _from="InfoSMS", # in this case _ is due to "from" being a reserved keyword in Python, and is not intended to mark from as an internal field
                                 # proper PEP would be to have trailing _ but the code gen library didn't default to it and was not found until after release
                text=message_text,
                # notify_url only needed if you haven't contacted support team to set a default for your account
                # and still want to get delivery report sent to you
                notify_url=notify_url + "/dr"
            )
        ])
    try:
        api_response: SmsResponse = api_instance.send_sms_message(sms_advanced_textual_request=sms_request)
        api_response.get("messages")
        print(api_response, flush=True)
    except ApiException as ex:
        print("Error occurred while trying to send SMS message.")
        print("Error status: %s\n" % ex.status)
        print("Error headers: %s\n" % ex.headers)
        print("Error body: %s\n" % ex.body)

def main():
    public_url, flask_thread = WebApp.start_app()
    send_sms_message("test123", "13605551234", public_url)
    flask_thread.join() # app will exit unless we wait for flask to join

if __name__ == "__main__":
    main()
