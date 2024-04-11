from common.models.analytic import AnalyticRecord


class AnalyticsServices:
    @classmethod
    def get_last_analytics(cls, limit=50, as_dict=True) -> list:
        """Return the last N analytic records."""
        res = AnalyticRecord.scan(limit=limit)

        return list(r.attribute_values for r in res) if as_dict else list(res)
