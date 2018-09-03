import abc


class AbstractElement:
    """
    Kankei abstract data representation to transform it into a write query
    note :: raising exception by assert is bad
    """

    type = None
    fields = {}
    constraints = []
    parameters = []

    component_type = None

    def __init__(self, properties):
        invalid_prop = [prop for prop in properties.keys() if prop not in self.fields and prop not in self.parameters]
        if invalid_prop:
            raise AttributeError(f'invalid_property in Element: {",".join(invalid_prop)}')

        self.props = {name: type_.null for name, type_ in self.fields.items()}
        post_init_args = {par: properties.pop(par) if par not in properties else properties[par]
                          for par in self.parameters}

        for name, value in properties.items():
            self.props[name] = value

        self._post_init(**post_init_args)

    def __repr__(self):
        props_str = [f'{key}={value}' for key, value in list(self.props.items())]
        return f'<{self.type}:{",".join(props_str)}>'


    @abc.abstractmethod
    def merge(self,other):
        raise NotImplemented

    @property
    @abc.abstractmethod
    def csv(self):
        raise NotImplemented

    @property
    def _base_csv(self):
        # todo verify if this default dict is necessary
        result_dict = {'%s:%s' % (name, field.csv_type): "" for name, field in self.fields.items()}
        for name, value in self.props.items():
            header = '%s:%s' % (name, self.fields[name].csv_type)
            result_dict[header] = self.fields[name].csv_value(value)

        return result_dict

    def _post_init(self, **kwargs):
        pass
