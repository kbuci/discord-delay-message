from flask import Flask, request, jsonify
import boto3
from os import environ
import requests
import time
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
#environ["AWS_CONFIG_FILE"] = "./env.txt"
dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
table = dynamodb.Table('ScheduledSend')

@app.route('/add_message', methods=['POST'])
def add_message():
    content = request.json
    webhook = content["webhook"]
    delay_minutes = int(content["delay_minutes"])
    hook_res = requests.get(webhook)
    guild = hook_res.json()['guild_id']
    send_time = datetime.now(timezone.utc) + timedelta(minutes=delay_minutes)
    response = table.put_item(
        Item={
            'Hour': send_time.hour,
            'Timestamp': send_time.isoformat() + "|" + webhook,
            'Guild': guild,
            'retries':0,
            'content': content["content"]
            }
    )
    print(response)

    return jsonify({"status":"success"})

if __name__ == '__main__':
    app.run(debug=True)