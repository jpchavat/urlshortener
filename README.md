# URL Shortener 🔗
## Project Description 📝
This project implements a URL shortening system with the following functional and non-functional requirements:

### Functional Requirements 🛠️
- The system must allow shortening a long URL into a short URL.
- The system must allow redirecting a short URL to the original long URL.
- The system stores information about short URL traffic.
- The system must allow deleting a short URL.

### Non-Functional Requirements 🔍
- The system must be highly available.
- Creating a short URL must be fast, in less than 1 second.
- Redirecting a short URL must be fast, in less than 10 milliseconds in 90% of cases.
- The system must support a redirection traffic of 50,000 requests per second.

## How to Run the Project 🚀
### Requirements
- Docker
- Docker Compose

### Steps
1. Clone the repository.
2. Run the `docker-compose up` command in the `infra` directory.
3. Use Postman to load the request collection located in the project's `api-collection` folder.

### What Does the `docker-compose up` Command Lift Up? 🐳
- Three containers with the URL Management application (admin-app-{1,2,3}) served by Gunicorn on port 8000.
- Three containers with the URL Redirection application (redirector-app-{1,2,3}) served by Gunicorn on port 8080.
- A container with Redis on port 6379.
- A container with DynamoDB on port 9000 (:warning: not 8000).
- A container with ElasticMQ on port 9324.
- A container with Zookeeper on port 2181.
- A container with Nginx on port 80, with configuration located in the `infra/nginx.lb.conf` file.
Note: Docker volumes are used for cases requiring data persistence.

## Architecture 🏗️
### Architecture Diagram
![Component Diagram](diagrama_arqui_EN.png)

## Technology Stack 🛠️
- Python 3.9 as programming language
- Flask 3.x as web framework
- Redis as Cache
- DynamoDB as NoSQL database
- ElasticMQ as SQS simulator
- AWS SDK (Boto3)
- Zookeeper to ensure service high availability and uniqueness when generating short URL keys
- Nginx as web server and load balancer
- Gunicorn as WSGI application server
- Docker
- Docker Compose

## Design Decisions 🧠
### Database
DynamoDB was chosen as the NoSQL database for its scalability and high availability.

### Cache
Redis was chosen as the cache to store short URLs and their respective long URLs.

### Message Queue
ElasticMQ was chosen as an SQS simulator to store short URL redirection events. This ensures the system's high availability and prevents event loss.

Additionally, ElasticMQ is a tool that allows simulating AWS SQS service locally, using the same AWS SDK (Boto3).

### Architecture
A microservices architecture was chosen, where each service has a specific responsibility. This ensures the system's scalability and high availability.
