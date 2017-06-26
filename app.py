import os
import sys
import json
from wit import Wit
import requests
import random
from flask import Flask, request
import threading
import unicodedata


app = Flask(__name__)
wit_client=Wit(access_token=os.environ["wit_access_token"])

def wit_sent(request, response):
    print('Sending to user..',response['text'])
def my_action(request):
    print('Received from user...',request['text'])
def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    print(response['text'])

def merge(request):
    context = request['context']
    entities = request['entities']
    
    if 'joke' in context:
        del context['joke']
    category = first_entity_value(entities, 'category')
    if category:
        context['cat'] = category
    sentiment = first_entity_value(entities, 'sentiment')
    if sentiment:
        context['ack'] = 'Glad you liked it.' if sentiment == 'positive' else 'Hmm.'
    elif 'ack' in context:
        del context['ack']
    return context

def start():
#def start(request):
#context=request['context']
#entities=request['entities']
#data=json.load(context)
    test = "this is a test value"
#print test
    print "something is working"

@app.route('/specdrum-chat', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    #log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    
                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    response = wit_client.converse(session_id=random.random(),message=message_text)
                    #print entry
                    print response
                    for stuff in response:
                        if 'msg' in stuff:
                            send_message(sender_id, response['msg'])
                        if 'action' in stuff:
                            print ("action!")
                            if response.get('action'):
                                #type(response[action]) is unicode
                                action = response['action']
                                b=action.decode('utf-8')
                                if b=='start'.encode('utf-8'):
                                    print (b)
                                    start();
                                    send_message(sender_id,"starting now")
            
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
