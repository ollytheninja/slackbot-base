import os
import requests
from flask import Flask
from flask_slack import SlackManager

# Comment out this section if you don't want to use Sentry of error monitoring
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_URL"),
    integrations=[FlaskIntegration()]
)

slack_base_url = "https://slack.com/api/"

app = Flask(__name__)
app.config['SLACK_SIGNING_SECRET'] = os.environ.get("SLACK_SIGNING_SECRET")
auth_token = os.environ.get("SLACK_BOT_TOKEN")

slack_manager = SlackManager()
slack_manager.init_app(app)

hed = {'Authorization': 'Bearer ' + auth_token}


def slack_call(action, channel, text):
    url = slack_base_url + action
    response = requests.post(url, headers=hed, json={'text': text, 'channel': channel})
    response.raise_for_status()


@slack_manager.on('app_mention')
def reply_to_app_mention(sender, data, **extra):
    event = data['event']

    slack_call(
        'chat.postMessage',
        channel=event['channel'],
        text=f":robot_face: Hello <@{event['user']}>!")


@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0
