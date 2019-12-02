class Object:
    """Represents a generic Call of Duty object."""

    _type = None

    def __init__(self, client, data):
        self._client = client

    @property
    def type(self):
        return self._type

    def __repr__(self):
        repr_str = self.__class__.__name__

        return f"<{repr_str}>"

    def __str__(self):
        return self.__repr__()
