from common.models.analytic import AnalyticRecordData


def test_redirector_app(redirector_app, redirector_client):
    response = redirector_client.get("/AABBCC")
    assert response.status_code == 404


def test_analytic_tasks_service(redirector_app, redirector_client):
    from common.services.sqs import AnalyticsServices

    service = AnalyticsServices()
    assert service is not None
    assert service.client is not None
    assert service.queue_url is not None

    arecord = AnalyticRecordData(
        id=1,
        short_url="AABBCC",
        long_url="www.jpchavat.com",
        ip="127.0.0.1",
        timestamp=1712534133,
        user_agent="Mozilla",
        language="EN",
    )

    # Send a task message
    response = service.send(arecord)
    assert response is not None

    # Receive the task message
    message = service.receive()
    assert message is not None
    assert message.id == 1
    assert message.short_url == "AABBCC"
    assert message.long_url == "www.jpchavat.com"
    assert message.ip == "127.0.0.1"
    assert message.timestamp == 1712534133
    assert message.user_agent == "Mozilla"
    assert message.language == "EN"
