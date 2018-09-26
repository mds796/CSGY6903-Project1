import sched

PRIORITY = 2


class ScheduledTimeout:
    def __init__(self, milliseconds, error_message, scheduler):
        self.milliseconds = milliseconds
        self.error_message = error_message
        self.scheduler = scheduler

    def trigger_timeout(self):
        raise TimeoutError(self.error_message)

    def __enter__(self):
        self.event = self.scheduler.enter(self.milliseconds, PRIORITY, self.trigger_timeout)
        self.scheduler.run(False)

    def __exit__(self, type, value, traceback):
        if not self.scheduler.empty():
            for event in self.scheduler.queue:
                self.scheduler.cancel(event)


def timeout(milliseconds, error_message='Timeout', scheduler=sched.scheduler()):
    return ScheduledTimeout(milliseconds, error_message, scheduler)
