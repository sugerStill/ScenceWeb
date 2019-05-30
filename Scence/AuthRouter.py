class AuthRouter:
    def db_for_read(self, model, **hints):

        if model._meta.app_label == 'TrafficView':
            return 'trafficdatabase'

        if model._meta.app_label == "ScenceView":
            return "webdata"
        return None

    def db_for_write(self, model, **hints):

        if model._meta.app_label == 'TrafficView':
            return 'trafficdatabase'
        if model._meta.app_label == "ScenceView":
            return "webdata"
        return None

    def allow_relation(self, obj1, obj2, **hints):

        db_list = ['trafficdatabase', 'WebData']
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if app_label == 'TrafficView':
            return  'trafficdatabase'
        elif app_label == 'ScenceView' or db == 'WebData':
            return 'WebData'

        return None
