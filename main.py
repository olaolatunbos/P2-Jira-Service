from datetime import datetime
import os
import time
import boto3
from jira import JIRA

sqs = boto3.client('sqs')
p2_queue_url = os.environ.get('SQS_QUEUE_URL_P2')
jira_server = os.environ.get('JIRA_SERVER')
auth_jira = JIRA(server=jira_server, basic_auth=('olaolat@hotmail.com', os.environ.get('JIRA_API_TOKEN')))


#-------------------------------------------------------------------------
def retrieve_messages_from_queue():
    response = sqs.receive_message(
        QueueUrl=p2_queue_url,
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=10,
        VisibilityTimeout=30,
        WaitTimeSeconds=5
    )

    return response.get("Messages", [])
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
def send_ticket_to_jira(messages):
    for message in messages:
        title = f"\n{message['MessageAttributes']['TicketID']['StringValue']}: {message['MessageAttributes']['Title']['StringValue']} "
        description = "\n\n----------------------------------------------------------------------------------------------------------------"
        description += f"\nTitle: {message['MessageAttributes']['Title']['StringValue']}"
        description += f"\nPriority: {message['MessageAttributes']['Priority']['StringValue']}"
        description += f"\nCreated At: {datetime.now().strftime('%Y-%m-%d, %H:%M')}"
        description += f"\nDescription: {message['Body']}"
        description += "\n\n----------------------------------------------------------------------------------------------------------------"
        
        auth_jira.create_issue(project='PT', summary=title,
                                description=description, issuetype={'name': 'Task'})
        sqs.delete_message(
            QueueUrl=p2_queue_url,
            ReceiptHandle=message['ReceiptHandle']
        )
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
def process_message():
    while True:
        messages = retrieve_messages_from_queue()
        print(f"Retrieved {len(messages)} messages from SQS")
        if messages:
            send_ticket_to_jira(messages)
        else:
            time.sleep(5)
#-------------------------------------------------------------------------

if __name__ == "__main__":
    process_message()