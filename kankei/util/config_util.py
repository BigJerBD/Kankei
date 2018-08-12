# config structure definition
class SubConfig:
    ...


class Config:
    """
    empty class to make a configuration object simply
    """

    def __init__(self, source_dct):
        for key, value in source_dct.items():
            access_seq = key.split(".")
            _append_dot_path(self, access_seq, value)

    def __getattr__(self, item):
        # specifies that a get_attribute (.) call is dynamic
        return super().__getattribute__(item)


def _append_dot_path(dct, accesses, value):
    if accesses:
        subdict = getattr(dct, accesses[0], SubConfig())
        setattr(dct, accesses[0], _append_dot_path(subdict, accesses[1:], value))
        return dct
    else:
        return value
