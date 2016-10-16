from __future__ import print_function

import json
import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('sns')
SMS = '+1**********' #Phone number to send message to

def getSubscription(topicArn, nextToken=''):
    data = client.list_subscriptions_by_topic(TopicArn=topicArn, NextToken=nextToken)
    subscriptions = data['Subscriptions']
    subs = list(filter(lambda x:x['Protocol']=='sms' and x['Endpoint']==SMS, subscriptions))
    subscription = subs[0] if subs else None
    if not subscription:
        if data.get('NextToken'):
            getSubscription(topicArn, data['NextToken'])
        else:
            return None
    logger.info("Found subscription: {0}".format(subscription))
    return subscription
        
    
def createSubscription(topicArn):
    subscription = getSubscription(topicArn)
    if not subscription:
        logger.info("Subscription Not found. Creating one.")
        response = client.subscribe(TopicArn=topicArn, Protocol='sms', Endpoint=SMS)
        if not response:
            logger.error("Failed to create the subscription")
            return None
        logger.info("Subscribed {0} to {1}".format(SMS, topicArn))
            

def createTopic(topicName):
    topic = client.create_topic(Name=topicName)
    if not topic:
        logger.error("Topic creation/get Failed")
        return None
    logger.info("Created Topic: {0}".format(topic))
    logger.info("Creating Subscription")
    topicArn = topic.get('TopicArn')
    createSubscription(topicArn)
    return topicArn

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    print("Received event: " + event['clickType'])
    logger.info("Received event: {0}".format(event['clickType']))
    topicArn = createTopic('aws-iot-button-sns-topic-2')
    response = client.publish(
        Message='Alert Notification. Event type: {0}'.format(event['clickType']),
        Subject='Hello from your IoT Button',
        PhoneNumber=SMS
    )
    logger.info("Message Id: {0}".format(response.get('MessageId')))
    
    

