import json


def test_redirector_app(mocker, redirector_app, redirector_client):
    # mock the DB connection, inspired in https://github.com/pynamodb/PynamoDB/blob/master/tests/test_model.py#L51
    PATCH_METHOD = "pynamodb.connection.Connection.dispatch"
    # PATCH_METHOD = "pynamodb.connection.Connection._make_api_call"
    fake_db = mocker.MagicMock()
    mocker.patch(PATCH_METHOD, fake_db)
    # silence the cache
    cache_get = mocker.patch(
        "common.services.urlobject.URLObjectCacheService.get", mocker.MagicMock()
    )
    cache_get.return_value = None

    # Test not existent URL
    fake_db.return_value = {"Items": [], "Count": 0, "ScannedCount": 0}
    response = redirector_client.get("/AABBCC")
    assert response.status_code == 404

    # Test existent URL
    fake_db.return_value = {
        "Items": [
            {
                "short_url": {"S": "AABBCC"},
                "long_url": {"S": "https://www.nature.com/articles/d41586-023-03144-w"},
                "user_id": {"S": "admin_127001"},
                "created_at": {"S": "2024-04-01T00:00:00.259475+0000"},
                "deleted": {"BOOL": False},
            }
        ],
        "Count": 1,
        "ScannedCount": 1,
    }
    response = redirector_client.get("/AABBCC")
    assert response.status_code == 302
    assert (
        response.headers["Location"]
        == "https://www.nature.com/articles/d41586-023-03144-w"
    )


def test_analytic_tasks_service(mocker, redirector_app, redirector_client):
    # silence the cache
    cache_get = mocker.patch(
        "common.services.urlobject.URLObjectCacheService.get", mocker.MagicMock()
    )
    cache_get.return_value = None

    from common.services.sqs import AnalyticsServices

    service = AnalyticsServices()
    assert service is not None
    assert service.client is not None
    assert service.queue_url is not None

    arecord = {
        "short_url": "AABBCC",
        "long_url": "www.jpchavat.com",
        "ip": "127.0.0.1",
        "timestamp": 1712534133,
        "user_agent": "Mozilla",
        "language": "EN",
    }

    # FIXME: the cases below needs to be moc
    #   right now, they need the SQS service to be running

    # Send a task message
    response = service.send(arecord)
    assert response is not None

    # Receive the task message
    message = service.receive()
    assert message is not None
    assert message.get("Messages") is not None
    assert len(message.get("Messages")) > 0
    assert "Body" in message.get("Messages")[0]
    message = json.loads(message.get("Messages")[0]["Body"])
    assert "short_url" in message
    # assert message["short_url"] == "AABBCC"
    # assert message["long_url"] == "www.jpchavat.com"
    # assert message["ip"] == "127.0.0.1"
    # assert message["timestamp"] == 1712534133
    # assert message["user_agent"] == "Mozilla"
    # assert message["language"] == "EN"
