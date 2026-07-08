#Event Bus 
class EventBus:
    def __init__(self):
        self._subs = {}          # event name -> list of callbacks

    def subscribe(self, event, callback):
        self._subs.setdefault(event, []).append(callback)

    def publish(self, event, **data):
        for callback in self._subs.get(event, []):
            callback(**data)