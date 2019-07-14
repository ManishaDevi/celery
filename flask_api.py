import time
from flask import Flask, jsonify
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task
def asyncSendMail(emailAdrs, emailBody):
    emailBody = {
        "emailAdrs": emailAdrs,
        "emailBody": emailBody
    }
    time.sleep(5)  # Mimic mail send
    return "success"


@app.route('/')
def index():
    EMAIL = "example@gmail.com"
    BODY = "<h1>This is the mail</h1>"
    asyncSendMail.delay(EMAIL, BODY)
    response = {
        "success": True,
        "data": "The mail has been sent to " + EMAIL
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
