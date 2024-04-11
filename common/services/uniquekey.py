import string

from flask import current_app


class UniqueShortURLKeyService:
    """Uses Zookeeper to generate unique short URL keys."""

    SHORT_URL_KEY_LENGTH = 6  # fixme: should be in the config
    BASE62_SHUFFLED_CHARS = (
        "WLG68zgdrqifbMOJljoHBcQxThAm3ZN4wPkECy2npe91FV5Dt7YXUvRs0SKuIa"
    )
    # was generated with the following code:
    # import random
    # import string
    # base62_chars = string.digits + string.ascii_letters
    # shuffled_chars = list(base62_chars)
    # random.shuffle(shuffled_chars)
    # base62_chars = ''.join(shuffled_chars)
    STARTING_SEQUENCE_NUMBER = 3500000  # skip the first 3.5M keys

    def __init__(self):
        from kazoo.client import KazooClient

        # FIXME: to improve, there is a flask extension for Zookeeper/kazoo
        self.zk = KazooClient(hosts=current_app.config["ZOOKEEPER_HOSTS"])
        self.zk.start()
        # Zookeeper path to the monotonic and atomic counter
        self.counter = "/short_url_counter"

    def get_unique_short_url(self):
        with self.zk.Lock(self.counter):
            # More info on the Lock class: https://kazoo.readthedocs.io/en/latest/api/recipe/lock.html
            # Create a new node with a sequence number
            new_node = self.zk.create(
                self.counter + "/", ephemeral=False, sequence=True
            )
            # Extract the sequence number
            sequence_number = int(new_node.split("/")[-1])
            # Convert the sequence number to a base62 string
            return self.encode_unique_number(sequence_number)

    @classmethod
    def encode_unique_number(cls, number):
        """This is like mapping a number in base 10 to base 62."""
        number += cls.STARTING_SEQUENCE_NUMBER
        result = []
        while number > 0:
            number, remainder = divmod(number, 62)
            result.append(cls.BASE62_SHUFFLED_CHARS[remainder])
        pre_result = "".join(reversed(result)).zfill(cls.SHORT_URL_KEY_LENGTH)
        # Interchange the characters to make it harder to guess
        # Example: 00ABCD -> C0ABD0
        return (
            pre_result[4]
            + pre_result[1]
            + pre_result[2:4]
            + pre_result[5]
            + pre_result[0]
        )
