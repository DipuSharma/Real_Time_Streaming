from celery import Celery
from celery.result import AsyncResult
import json
from typing import List

celery = Celery(
    __name__,
    backend='redis://localhost:6379/0',
    broker='redis://localhost:6379/0'
)
