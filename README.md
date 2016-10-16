# IotSMSButton

This project basically utilizes Amazon IOT service to trigger SMS based on events.

Amazon button is used as a clicker.
When the button is clicked, AWS lambda function is triggered. That function then uses Amazon SNS service to send SMS to the phone number subscribed to the SNS topic.
