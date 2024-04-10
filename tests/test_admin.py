def test_urlobject_crud(mocker, admin_app, admin_client):

    # mock the DB connection, inspired in https://github.com/pynamodb/PynamoDB/blob/master/tests/test_model.py#L51
    PATCH_METHOD = "pynamodb.connection.Connection.dispatch"
    # PATCH_METHOD = "pynamodb.connection.Connection._make_api_call"
    fake_db = mocker.MagicMock()
    mocker.patch(PATCH_METHOD, fake_db)

    assert admin_app
    assert admin_client

    # Test the index route (greeting)
    response = admin_client.get("/admin/")
    assert response.status_code == 200

    # Test getting the url object collection (empty for now)
    fake_db.return_value = {"Items": [], "Count": 0, "ScannedCount": 0}
    response = admin_client.get("/admin/urls")
    assert response.status_code == 200
    assert response.json == []

    # Test getting a single url object (404 for now)
    fake_db.return_value = {"Items": [], "Count": 0, "ScannedCount": 0}
    response = admin_client.get("/admin/urls/AABBCC")
    assert response.status_code == 404
    assert response.json
    assert response.json["error_code"] == "url_object_not_found"

    # Test creating an url object from a long url
    fake_db.return_value = {
        "Items": [
            {
                "short_url": {"S": "AABBCC"},
                "long_url": {"S": "https://www.jpchavat.com"},
                "created_at": {"S": "2024-04-01T00:00:00.259475+0000"},
                "deleted": {"BOOL": False},
                "user_id": {"S": "admin_127001"},
            }
        ],
        "Count": 1,
        "ScannedCount": 1,
    }
    body = {"long_url": "https://www.jpchavat.com"}
    response = admin_client.post("/admin/urls", json=body)
    assert response.status_code == 201
    assert response.json
    url_short_key = response.json["short_url"]

    # Test getting the just created url object
    fake_db.return_value = {
        "Items": [
            {
                "short_url": {"S": url_short_key},
                "long_url": {"S": "https://www.jpchavat.com"},
                "created_at": {"S": "2024-04-01T00:00:00.259475+0000"},
                "deleted": {"BOOL": False},
                "user_id": {"S": "admin_127001"},
            }
        ],
        "Count": 1,
        "ScannedCount": 1,
    }
    response = admin_client.get(f"/admin/urls/{url_short_key}")
    assert response.status_code == 200
    assert response.json
    assert response.json["short_url"] == url_short_key
    assert response.json["long_url"] == "https://www.jpchavat.com"

    # Test deleting the just created url object
    fake_db.return_value = {
        "Items": [
            {
                "short_url": {"S": url_short_key},
                "long_url": {"S": "https://www.jpchavat.com"},
                "created_at": {"S": "2024-04-01T00:00:00.259475+0000"},
                "deleted": {"BOOL": False},
                "user_id": {"S": "admin_127001"},
            }
        ],
        "Count": 1,
        "ScannedCount": 1,
    }
    response = admin_client.delete(f"/admin/urls/{url_short_key}")
    assert response.status_code == 200
    assert response.json
    assert response.json["short_url"] == url_short_key

    # Test getting the deleted url object
    fake_db.return_value = {"Items": [], "Count": 0, "ScannedCount": 0}
    response = admin_client.get(f"/admin/urls/{url_short_key}")
    assert response.status_code == 404
    assert response.json
    assert response.json["error_code"] == "url_object_not_found"

    # Test getting the url object collection (empty again)
    fake_db.return_value = {"Items": [], "Count": 0, "ScannedCount": 0}
    response = admin_client.get("/admin/urls")
    assert response.status_code == 200
    assert response.json == []

    # Validate that the url object was virtually deleted
    fake_db.return_value = {
        "Items": [
            {
                "short_url": {"S": url_short_key},
                "long_url": {"S": "https://www.jpchavat.com"},
                "created_at": {"S": "2024-04-01T00:00:00.259475+0000"},
                "deleted": {"BOOL": True},
                "user_id": {"S": "admin_127001"},
            }
        ],
        "Count": 1,
        "ScannedCount": 1,
    }
    from common.services.urlobject import URLObjectServices

    url_obj = URLObjectServices.get_urlobject(url_short_key, incl_deleted=True)
    assert url_obj.deleted == True

    # Test when trying to delete an already deleted url object
    fake_db.return_value = {"Items": [], "Count": 0, "ScannedCount": 0}
    response = admin_client.delete(f"/admin/urls/{url_short_key}")
    assert response.status_code == 404
    assert response.json
    assert response.json["error_code"] == "url_object_not_found"


# Example output from the "pynamodb.connection.Connection.dispatch" (the patched method in the above test case)
# {'Items': [{'created_at': {'S': '2024-04-10T16:25:51.259475+0000'}, 'deleted': {'BOOL': False}, 'long_url': {'S': 'https://www.jpchavat.com'}, 'user_id': {'S': 'admin_127001'}, 'short_url': {'S': 'AABBCC'}}], 'Count': 1, 'ScannedCount': 1, 'ConsumedCapacity': {'TableName': 'urls', 'CapacityUnits': 0.5}, 'ResponseMetadata': {'RequestId': 'b3313288-e578-4efd-ab3c-6c6355f7ef89', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Jetty(12.0.2)', 'date': 'Wed, 10 Apr 2024 16:29:02 GMT', 'x-amzn-requestid': 'b3313288-e578-4efd-ab3c-6c6355f7ef89', 'content-type': 'application/x-amz-json-1.0', 'x-amz-crc32': '3194121034', 'content-length': '280'}, 'RetryAttempts': 0}}
# {'Items': [{'created_at': {'S': '2024-04-10T16:25:51.259475+0000'}, 'deleted': {'BOOL': False}, 'long_url': {'S': 'https://www.jpchavat.com'}, 'user_id': {'S': 'admin_127001'}, 'short_url': {'S': 'AABBCC'}}], 'Count': 1, 'ScannedCount': 1, 'ConsumedCapacity': {'TableName': 'urls', 'CapacityUnits': 0.5}, 'ResponseMetadata': {'RequestId': 'd55e4a10-c150-463c-b110-92f9ccfe23cb', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Jetty(12.0.2)', 'date': 'Wed, 10 Apr 2024 16:33:27 GMT', 'x-amzn-requestid': 'd55e4a10-c150-463c-b110-92f9ccfe23cb', 'content-type': 'application/x-amz-json-1.0', 'x-amz-crc32': '3194121034', 'content-length': '280'}, 'RetryAttempts': 0}}


def test_crud_exceptions(mocker, admin_app, admin_client):

    # mock the DB connection, inspired in https://github.com/pynamodb/PynamoDB/blob/master/tests/test_model.py#L51
    PATCH_METHOD = "pynamodb.connection.Connection.dispatch"
    fake_db = mocker.MagicMock()

    mocker.patch(PATCH_METHOD, fake_db)

    # Test an invalid Admin-app URL
    response = admin_client.get("/admin/notfound")
    assert response.status_code == 404
    assert response.json
    assert response.json["error_code"] == "not_found"

    # Test an invalid URL object key (>6 characters)
    response = admin_client.get("/admin/urls/MORETHAN6CHARACTERS")
    assert response.status_code == 400
    assert response.json
    assert response.json["error_code"] == "invalid_short_url"
    assert response.json["params"]["short_url"] == "MORETHAN6CHARACTERS"

    # Test an invalid URL object key (non-alphanumeric)
    response = admin_client.get("/admin/urls/!!!---")
    assert response.status_code == 400
    assert response.json
    assert response.json["error_code"] == "invalid_short_url"
    assert response.json["params"]["short_url"] == "!!!---"

    # Test an invalid URL object key (<6 characters)
    response = admin_client.get("/admin/urls/ABC")
    assert response.status_code == 400
    assert response.json
    assert response.json["error_code"] == "invalid_short_url"
    assert response.json["params"]["short_url"] == "ABC"

    # Test a missing URL object key
    response = admin_client.get("/admin/urls/")
    assert response.status_code == 404
    assert response.json
    assert response.json["error_code"] == "not_found"

    # Same tests, but using the delete method
    #
    response = admin_client.delete("/admin/urls/MORETHAN6CHARACTERS")
    assert response.status_code == 400
    assert response.json
    assert response.json["error_code"] == "invalid_short_url"
    assert response.json["params"]["short_url"] == "MORETHAN6CHARACTERS"
    #
    response = admin_client.delete("/admin/urls/!!!---")
    assert response.status_code == 400
    assert response.json
    assert response.json["error_code"] == "invalid_short_url"
    assert response.json["params"]["short_url"] == "!!!---"
    #
    response = admin_client.delete("/admin/urls/ABC")
    assert response.status_code == 400
    assert response.json
    assert response.json["error_code"] == "invalid_short_url"
    assert response.json["params"]["short_url"] == "ABC"
    #
    response = admin_client.delete("/admin/urls/")
    assert response.status_code == 404
    assert response.json
    assert response.json["error_code"] == "not_found"
