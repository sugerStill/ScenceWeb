from django.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING


class AuthRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'TrafficView':
            return 'trafficdatabase'

        if model._meta.app_label == "ScenceView":
            return "webdata"
        if model._meta.app_label == "weather":
            return "weather"
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'TrafficView':
            return 'trafficdatabase'
        if model._meta.app_label == "ScenceView":
            return "webdata"
        if model._meta.app_label == "weather":
            return "weather"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        db_list = ['trafficdatabase', 'webdata', 'weather']
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'TrafficView':
            return 'trafficdatabase ' if db == "trafficdatabase" else False

        elif app_label == 'ScenceView':

            return 'webdata' if db == "webdata" else False
        elif app_label == 'weather':
            return 'weather' if db == "weather" else False

        return None
