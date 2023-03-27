class IntConverter:
    regex = r'[1-9]\d*'

    def to_python(self, positive: str):
        return int(positive)

    def to_url(self, positive: int):
        return f'{positive}'
