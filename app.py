# Download the helper library from https://www.twilio.com/docs/python/install
import os, sys
from twilio.rest import Client
import time
import sched
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

#Have to pay for twilio
#Have to replace API token

app = Flask(__name__)

#virtualenv sendsms
#source sendsms/bin/activate 
#sudo pip3 install twilio --upgrade
#sudo pip install flask
#cd documents
#cd notification
#python app.py
#Let it run
 
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
client = Client('AC2532db93c2b68f7b6cf14312456bf732', 'db39b9a763f69b7f7c7b1ee4de822db1')

on = True
s = sched.scheduler(time.time, time.sleep)
maxTime = 5 * 60 * 60 #5 hours * 60 mins * 60 sec
def getMsg():
    msgs = client.messages.list(limit=1)
    for m in msgs:
        return m.sid
def getBody(sid):
    return client.messages(sid).fetch().body
def getTo(sid):
    return client.messages(sid).fetch().to
def getFrom(sid):
    return client.messages(sid).fetch().from_
def getStatus(sid):
    return client.messages(sid).fetch().direction
def msg():
    message = client.messages \
        .create(
            body='Stamina Maxed Out in Project Sekai',
            from_='+19897474557',
            to='+19196187361'
        )
    send()
    
def test(sc):
    message = client.messages \
        .create(
            body='Test',
            from_='+19897474557',
            to='+19196187361'
        )
    # test(sc)
    
def send():
    #print(getStatus(getMsg()))
    # if body == 'automated reply':
  #  if getFrom(getMsg()) == '+19196187361':
        s.enter(maxTime, 1, msg)
    # else:
    #     send()
    # if getTo(getMsg()) != '+19196187361':
    #     s.enter(0, 1, msg)
    #     # print(getStatus(getMsg()))
    # else:
    #     send()

s.enter(0, 1, msg)
s.run()

#print(getBody(getMsg()))
#print(message.sid)

# messages = client.messages.list(limit=20)

# for record in messages:
#     print(record.body)