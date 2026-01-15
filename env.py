# Environment: immutable dictionary mapping names -> values
class Env(dict):
    def extend(self, name, value):
        new_env = Env(self)
        new_env[name] = value
        return new_env
