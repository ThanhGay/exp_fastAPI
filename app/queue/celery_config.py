## Broker settings.
broker_url = "redis://localhost:6379/0"

# List of modules to import when the Celery worker starts.
imports = [
    "app.queue.tasks",
]

## Using the database to store task state and results.
result_backend = "redis://localhost:6379/0"

task_annotations = {"queue.add": {"rate_limit": "10/s"}}

result_expires = 3600

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

task_acks_late = True
worker_prefetch_multiplier = 1
task_reject_on_worker_lost = True


timezone = "Asia/Ho_Chi_Minh"
enable_utc = True
