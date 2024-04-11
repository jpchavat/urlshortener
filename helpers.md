## DynamoDB-Local 💾
### List Tables
```bash
aws dynamodb list-tables --endpoint-url http://localhost:9000 --region elasticmq
```

### Scan Table Items
```bash
aws dynamodb scan --endpoint-url http://localhost:9000 --region elasticmq --table-name urls
```

### Delete an Item
```bash
aws dynamodb delete-item --endpoint-url http://localhost:9000 --region elasticmq --table-name urls --key '{"id": {"S": "1"}}'
```

### Delete Tables
```bash
aws dynamodb delete-table --endpoint-url http://localhost:9000 --region elasticmq --table-name urls
```

### Create Tables
```python
from admin.app import create_app; app = create_app(); app.app_context().push()
from common.models.urlobject import URLObject
from common.models.analytic import AnalyticRecord
URLObject.exists() or URLObject.create_table()
AnalyticRecord.exists() or AnalyticRecord.create_table()
```

### Describe Table
```bash
aws dynamodb describe-table --endpoint-url http://localhost:9000 --region elasticmq --table-name urls
```

## Dynamo-viewer 🔍
```bash
# npm install -g dynamodb-admin
DYNAMO_ENDPOINT=http://localhost:9000 dynamodb-admin --port 8888
```
Then, access http://localhost:8888

## PynamoDB Docs 📚
https://pynamodb.readthedocs.io/en/latest/index.html

## Ngrok 🌐
```bash
ngrok http 80
```

## Redis Explorer 🔍
```bash
# Install
npm install -g redis-commander
# Run
redis-commander --port 9999
```
Then, access http://localhost:9999

More info at http://joeferner.github.io/redis-commander/

## Docker-Compose 🐳
View Logs in a Terminal
```bash
cd infra
docker-compose logs -f
```

## ElasticMQ (Simulating AWS SQS) 🤖
Once the Docker container is running, you can access a web interface at http://localhost:9325 to monitor its usage.