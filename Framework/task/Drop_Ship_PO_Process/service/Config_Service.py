from task.Drop_Ship_PO_Process.db.Mapping import DBSession, Config


class ConfigService(object):
    @staticmethod
    def get_config_dict():
        session = DBSession()
        configs = session.query(Config.key_name, Config.key_value).filter_by(app_id=101, delete_time=None)
        result = dict()
        for config in configs.all():
            result[config.key_name] = config.key_value

        return result

