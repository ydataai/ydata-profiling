from pandas_profiling.config import config


class ConfigManager:
    counter = 0

    @classmethod
    def register(cls, config_):
        cls.counter += 1
        config.update(config_)

    @classmethod
    def unregister(cls):
        cls.counter -= 1
        if cls.counter <= 0:
            config.clear()

    @classmethod
    def build_wrapper(cls, func):
        def wrapper(pp):
            ConfigManager.register(pp.config)
            res = func(pp)
            ConfigManager.unregister()
            return res

        return wrapper
