from enum import Enum



__all__ = ['EEnv', 'EnvManager']



class EEnv(Enum):
    PRODUCTION = "production"
    ACCEPTATION = "acceptation"
    TEST = "test"
    DEVELOPMENT = "development"

env_val_norm_dict = {
    'prod': EEnv.PRODUCTION,
    'production': EEnv.PRODUCTION,
    'release': EEnv.PRODUCTION,
    'acc': EEnv.ACCEPTATION,
    'acceptation': EEnv.ACCEPTATION,
    'test': EEnv.TEST,
    'dev': EEnv.DEVELOPMENT,
    'development': EEnv.DEVELOPMENT,
}


class EnvManager:
    env: EEnv
    def __init__(self, env:str):
        self.env = self._validate_normalize(env)

    def __repr__(self) -> str:
        return f"{self.env.value}"

    def _validate_normalize(self, env:str) -> EEnv:
        """ Checks if the env is of a valid type and translates to Enum value """
        if not isinstance(env, str):
            raise ValueError(f"Proviced env is of type {type(env)}; must be a string")

        _env = env.lower()

        if (_env not in env_val_norm_dict):
            raise ValueError(f"Invalid environment: {env}. Valid environments are: {', '.join(env_val_norm_dict)}")

        return env_val_norm_dict.get(_env)

    @property
    def is_dev(self) -> bool:
        return self.env == EEnv.DEVELOPMENT
    @property
    def is_prod(self) -> bool:
        return self.env == EEnv.PRODUCTION


print(EnvManager('dev'))
print(EnvManager('test'))
print(EnvManager('acc'))
print(EnvManager('prod'))
ENV = EnvManager('dev')
APP_NAME = 'aids'
APP_NAME_ENV = f"jojoo ({ENV})" if (not ENV.is_prod) else APP_NAME
print(APP_NAME_ENV)