from celery import shared_task, current_app
import json

@shared_task
def add(x, y):
    sum = x + y
    json = {"result" : sum}
    return json

@shared_task
def callback(result):
    return result

@shared_task
def bg_process(x):
    ds = []
    for i in range(int(x)):
        ds.append({"nomor" : i})
    
    response = json.dumps(ds)
    return response

    

@shared_task
def get_tasks_in_queue():
    with current_app.connection() as conn:
        inspector = current_app.control.inspect(connection=conn)
        tasks_in_queue = inspector.scheduled()
    return tasks_in_queue