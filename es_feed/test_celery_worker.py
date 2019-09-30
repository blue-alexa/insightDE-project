import celery
app = celery.Celery('test',
                    broker='amqp://rabbitmq:rabbitmq@10.0.0.14//',
                    backend='amqp://rabbitmq:rabbitmq@10.0.0.14//')

@app.task
def echo(message):
    return message

# celery -A test worker --loglevel=info