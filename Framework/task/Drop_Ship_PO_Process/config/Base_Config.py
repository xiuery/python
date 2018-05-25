from task.Drop_Ship_PO_Process.service.Config_Service import ConfigService


class BaseConfig(object):
    CONFIG = dict()

    @staticmethod
    def get_value(key):
        if not BaseConfig.CONFIG:
            BaseConfig.CONFIG = ConfigService.get_config_dict()
        if key in BaseConfig.CONFIG:
            return BaseConfig.CONFIG[key]
        else:
            return False


if __name__ == '__main__':
    pass

