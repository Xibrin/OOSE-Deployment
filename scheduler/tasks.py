from eventPlanner.celery import app
from dateutil import parser

from .models import Event
from .support import states, event_finder
import datetime


@app.task
def refresh():
    Event.objects.all().delete()
    for state in states.get_all_states().values():
        event_finder_object = event_finder.EventFinder(
            location=state,
            start_time=int(parser.parse(datetime.datetime.now().isoformat()).timestamp())
        )
        event_finder_object.save_all_events()