import uuid
from typing import Union

from common.exceptions import ItemDoesNotExistException
from common.models.urlobject import URLObject
from common.services.urlobject import URLObjectCacheService


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


class URLObjectServices:
    @staticmethod
    def create_short_url(long_url: str, user_id: str):
        """
        Creates a new short URL Object in the database.

        :param long_url: The original long URL.
        :param user_id : The ID of the user creating the short URL.

        :return (str): The generated short URL.
        """

        # Request a unique short URL key
        short_url = UniqueShortURLKeyService().get_unique_short_url()

        # Create a new URLObject instance
        url_object = URLObject(
            short_url=short_url,
            long_url=long_url,
            user_id=user_id,
        )

        # Save the URLObject to the database
        url_object.save()

        return short_url

    @staticmethod
    def _get_one(short_url: str, incl_deleted: bool) -> URLObject:
        """Wrapper for scan to simulate the URLObject.get method with/without deleted items."""
        url_object = list(
            URLObject.scan(
                (URLObject.short_url == short_url) & (URLObject.deleted == incl_deleted)
            )
        )
        if not url_object:
            raise ItemDoesNotExistException(
                error_code="url_object_not_found", params={"short_url": short_url}
            )
        else:
            return url_object[0]

    @classmethod
    def get_short_urls(
        cls, user_id=None, limit=50, incl_deleted=False, as_dict=False
    ) -> list[Union[URLObject, dict]]:
        """Return a collection of URLs, limited to the given user ID and limit."""
        qry_filter = URLObject.deleted == incl_deleted
        if user_id:
            qry_filter &= URLObject.user_id == user_id
        return (
            list(u.attribute_values for u in URLObject.scan(qry_filter, limit=limit))
            if as_dict
            else list(URLObject.scan(qry_filter, limit=limit))
        )

    @classmethod
    def get_urlobject(
        cls, short_url, incl_deleted=False, as_dict=False
    ) -> Union[URLObject, dict]:
        """
        Retrieves the URLObject with the given short URL key.

        :param short_url: The short URL key.
        :return: The original URL, or None if not found.
        """
        url_object = cls._get_one(short_url, incl_deleted)
        return url_object.attribute_values if as_dict else url_object

    @classmethod
    def get_long_from_short_url(cls, short_url, incl_deleted=False) -> str:
        """
        Retrieves the original URL based on the given short URL key.

        :param short_url: The short URL key.
        :return: The original URL, or None if not found.
        """
        try:
            url_object = cls.get_urlobject(short_url, incl_deleted=incl_deleted)
            return url_object.long_url
        except URLObject.DoesNotExist:
            raise ItemDoesNotExistException(
                error_code="short_url_not_found", params={"short_url": short_url}
            )

    @classmethod
    def delete_url(cls, short_url) -> URLObject:
        """
        Deletes the URLObject with the given short URL key.

        :param short_url: The short URL key.
        :return: The virtuallt deleted URLObject.
        """
        url_object = cls._get_one(short_url=short_url, incl_deleted=False)
        # virtually delete the URLObject by setting the 'deleted' attribute to True
        url_object.deleted = True
        url_object.save()

        # Delete the short url from the cache, if it exists
        URLObjectCacheService().delete(short_url)

        return url_object
