from ..vendor import debtcollector


# https://stackoverflow.com/a/26853961
def merge_dicts(x, y):
    """Returns a copy of y merged into x."""
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


def get_module_name(module):
    """Returns a module's name or None if one cannot be found.
    Relevant PEP: https://www.python.org/dev/peps/pep-0451/
    """
    if hasattr(module, "__spec__"):
        return module.__spec__.name
    return getattr(module, "__name__", None)


# Based on: https://stackoverflow.com/a/7864317
class removed_classproperty(property):
    def __get__(self, cls, owner):
        debtcollector.deprecate(
            "Usage of ddtrace.ext.AppTypes is not longer supported, please use ddtrace.ext.SpanTypes"
        )
        return classmethod(self.fget).__get__(None, owner)()


def integration_service(config, pin, global_service_fallback=False):
    """Compute the service name that should be used for an integration
    based off the given config and pin instances.
    """
    if pin.service:
        return pin.service

    # Integrations unfortunately use both service and service_name in their
    # configs :/
    elif "service" in config:
        return config.service
    elif "service_name" in config:
        return config.service_name
    elif global_service_fallback:
        return config.global_config._get_service()
    else:
        return None
