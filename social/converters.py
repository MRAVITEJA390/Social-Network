class StatusConverter:
    regex = 'accept|reject'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
