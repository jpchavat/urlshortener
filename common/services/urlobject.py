import time
from typing import Union

from common.exceptions import ItemDoesNotExistException
from common.models.analytic import AnalyticRecordData
from common.models.urlobject import URLObject
from common.services.sqs import AnalyticsTaskService
from common.redis import redis_cli
from common.services.uniquekey import UniqueShortURLKeyService


class URLObjectCacheService:
    """Service to interact with the URLObject cache."""

    cache_prefix = "url:"

    @classmethod
    def get(cls, short_url: str):
        """Get the long URL from the cache by using the short URL key."""
        return redis_cli.get(f"{cls.cache_prefix}{short_url}")

    @classmethod
    def add(cls, short_url: str, long_url: str):
        redis_cli.set(f"{cls.cache_prefix}{short_url}", long_url)

    @classmethod
    def delete(cls, short_url: str):
        redis_cli.delete(f"{cls.cache_prefix}{short_url}")


class URLObjectServices:
    """Service to interact with the URLObject logics and model."""

    cache_prefix = "url:"

    @staticmethod
    def create(long_url: str, user_id: str):
        """
        Creates a new URL Object and persist it in the database.
        The short URL key is generated using the UniqueShortURLKeyService.

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
        url_object.save()

        return short_url

    @staticmethod
    def _get_one(short_url: str, incl_deleted: bool) -> URLObject:
        """
        Wrapper for scan to simulate the URLObject.get method with/without deleted items.

        This is necessary since the URLObject.get method doesn't support conditional queries.
        """
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
    def get_collection(
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
    def delete_url(cls, short_url) -> URLObject:
        """
        Deletes the URLObject with the given short URL key.

        :param short_url: The short URL key.
        :return: The virtually deleted URLObject.
        """
        url_object = cls._get_one(short_url=short_url, incl_deleted=False)
        # virtually delete the URLObject by setting the 'deleted' attribute to True
        url_object.deleted = True
        url_object.save()

        # Delete the short url from the cache, if it exists
        URLObjectCacheService().delete(short_url)

        return url_object

    @classmethod
    def get_long_url(cls, short_url, incl_deleted=False) -> str:
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

    def process_redirection(self, short_url: str, analytics: dict = None) -> str:
        """
        Process the redirection of the short URL key to the original URL.
        This method does many things:
        - Get the original URL from the short URL key, either from the cache or the database.
            - If the URL is not found in the cache, it will be fetched from the database.
            - If the URL is found in the database, it will be added to the cache.
        - Record the analytics data if provided.
        - Return the original URL.

        :param short_url: The short URL key
        :param analytics: The analytics data to be recorded. If None, no analytics will be recorded.
            Structure:
            {
                "ip": "<ip_address>",
                "user_agent": "<user_agent>",
                "language": "<language>"
            }
        :return: The original URL
        """
        long_url: str = URLObjectCacheService.get(short_url)
        if not long_url:
            # Cache miss, then try to get the URL from the DB
            long_url = self.get_long_url(short_url, incl_deleted=False)
            # If found, add it to the cache
            URLObjectCacheService.add(short_url, long_url)

        if (
            analytics is not None
        ):  # even if the analytics is an empty dict, we still record it
            AnalyticsTaskService().send(
                AnalyticRecordData(
                    short_url=short_url,
                    long_url=long_url,
                    ip=analytics.get("ip"),
                    timestamp=int(time.time()),
                    user_agent=analytics.get("user_agent"),
                    language=analytics.get("language"),
                )
            )

        return long_url
