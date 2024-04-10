import time

import boto3
from redis import Redis

from common.exceptions import ItemDoesNotExistException
from common.models.analytic import AnalyticRecordData
from common.models.urlobject import URLObject
from common.services.sqs import AnalyticsTaskService


class URLObjectCacheService:
    cache_prefix = "url:"

    def __init__(self):
        self.redis = Redis()

    def get(self, short_url: str):
        """Get the long URL from the cache by using the short URL key."""
        try:
            orig_url = self.redis.get(f"{self.cache_prefix}{short_url}")
            return orig_url
        except Exception as e:
            print(f"Error getting URL from cache: {e}")
            return None

    def add(self, short_url: str, long_url: URLObject):
        self.redis.set(f"{self.cache_prefix}{short_url}", long_url)

    def delete(self, short_url: str):
        # TODO
        pass
        # self.redis.delete(f"{self.cache_prefix}{short_url}")


class URLObjectServices:
    cache_prefix = "url:"

    def __init__(self):
        self.dynamodb = boto3.resource("dynamodb")
        self.redis = boto3.client("elasticache")

    def get_orig_url(self, short_url: str, analytics: dict = None) -> str:
        """
        Get the original URL from the short URL key, either from the cache or the database.
        If the URL is not found in the cache, it will be fetched from the database.

        :param analytics: The analytics data to be recorded. If None, no analytics will be recorded.
            Structure:
            {
                "ip": "<ip_address>",
                "user_agent": "<user_agent>",
                "language": "<language>"
            }

        :param short_url: The short URL key
        :return: The original URL
        """
        orig_url: str = self.get_orig_url_from_cache(short_url)
        if not orig_url:
            # Handle the cache miss, get the URL from the database
            long_url_obj = self.get_from_database(short_url)
            if long_url_obj:
                self.add_to_cache(short_url, long_url_obj)
                orig_url = long_url_obj.long_url
            else:
                raise ItemDoesNotExistException(params={"short_url": short_url})

        if analytics:
            AnalyticsTaskService().send(
                AnalyticRecordData(
                    short_url=short_url,
                    long_url=orig_url,
                    ip=analytics.get("ip"),
                    timestamp=int(time.time()),
                    user_agent=analytics.get("user_agent"),
                    language=analytics.get("language"),
                )
            )

        return orig_url

    def get_orig_url_from_cache(self, short_url: str):
        """Get the original URL from the cache"""
        try:
            orig_url = self.redis.get(f"{self.cache_prefix}{short_url}")
            return orig_url
        except Exception as e:
            print(f"Error getting URL from cache: {e}")
            return None

    def get_from_database(self, short_url: str):
        try:
            url_item = URLObject.get(short_url)
            return url_item.long_url
        except URLObject.DoesNotExist:
            print("URL not found in database")
            return None

    def add_to_cache(self, short_url: str, long_url: URLObject):
        try:
            # TODO: needs to evaluate if corresponds
            # Eg. if the URL is too old, maybe it should not be cached
            self.redis.set(f"{self.cache_prefix}{short_url}", long_url)
        except Exception as e:
            print(f"Error adding URL to cache: {e}")

    def delete_url(self, short_url: str):
        try:
            URLObject.delete(short_url)
        except URLObject.DoesNotExist:
            print(f"URL not found in database: {short_url}")
            raise URLNotFound(short_url=short_url)

    def delete_cache(self, short_url: str):
        try:
            self.redis.delete(f"{self.cache_prefix}{short_url}")
        except Exception as e:
            print(f"Error deleting URL from cache: {e}")
