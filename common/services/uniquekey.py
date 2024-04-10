import uuid


class UniqueShortURLKeyService:
    """Uses Zookeeper to generate unique short URL keys."""

    def __init__(self):
        # TODO: Initialize the Zookeeper client
        self.zk = None

    def get_unique_short_url(self):
        """
        Generates a unique short URL key using Zookeeper.

        TODO: for now, return a random key

        :return (str): The unique short URL key.
        """
        # TODO: here comes the Zookeeper custom service to generate a unique short URL key
        # TODO: here comes the Zookeeper custom service to generate a unique short URL key
        # TODO: here comes the Zookeeper custom service to generate a unique short URL key
        return f"{uuid.uuid4().hex[:6]}"
