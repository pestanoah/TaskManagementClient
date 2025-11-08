import boto3
from escpos.printer import Usb
from dotenv import load_dotenv
import printing

SQS_QUEUE_URL = "https://sqs.us-east-2.amazonaws.com/674010401876/TaskPrintingQueue"


def convertMessageToDict(message):
    messageDict = {
        "Body": message["Body"],
        "Title": message.get("MessageAttributes", {}).get("Title", {}).get("StringValue", ""),
        "Priority": message.get("MessageAttributes", {}).get("Priority", {}).get("StringValue", ""),
        "CreatedDate": message.get("MessageAttributes", {}).get("CreatedDate", {}).get("StringValue", ""),
        "DueDate": message.get("MessageAttributes", {}).get("DueDate", {}).get("StringValue", "") if message.get("MessageAttributes", {}).get("DueDate", {}) else None,
    }

    if messageDict["DueDate"] is None:
        del messageDict["DueDate"]
    if messageDict["Title"] == "":
        del messageDict["Title"]
    if messageDict["Priority"] == "":
        del messageDict["Priority"]
    if messageDict["CreatedDate"] == "":
        del messageDict["CreatedDate"]

    return messageDict


def processMessageLocal(_, message):
    print("Message", convertMessageToDict(message))
    im = printing.getTaskImage(convertMessageToDict(message))
    im.show()


def printTaskMessage(p, im):
    p.image(im, impl="bitImageColumn")
    p.text("\n")
    p.cut()
    print("Printed message to printer")


def processMessage(p, message):
    print("Message", message)
    im = printing.getTaskImage(convertMessageToDict(message))
    printTaskMessage(p, im)


def pollForMessages(processMessageFunc, sqs, p):
    while True:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=20
        )
        messages = response.get("Messages", [])
        if len(messages) == 0:
            print("No messages in queue")
        for message in messages:
            processMessageFunc(p, message)
            # Delete received message from queue
            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=message["ReceiptHandle"]
            )
            print("Deleted message from queue")


def main():
    print("Loading environment variables...")
    load_dotenv()
    print("Environment variables loaded.")
    sqs = boto3.client('sqs',
                       region_name='us-east-2'
                       )
    # poll for sqs messages
    try:
        p = Usb(0x0fe6, 0x811e, 0, profile="TM-T88III")
        pollForMessages(processMessage, sqs, p)
    except Exception as e:
        print("Error connecting to printer, just logging messages:", e)
        pollForMessages(processMessageLocal, sqs, None)
        return


if __name__ == "__main__":
    main()
