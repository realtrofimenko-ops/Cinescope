class CustomRequester:
    def __init__(self, session):
        self.session = session

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    def patch(self, url, **kwargs):
        return self.session.patch(url, **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)