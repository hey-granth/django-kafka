# Django Kafka Clone

A lightweight, Django-based implementation of a Kafka-like messaging system. This project provides a simple yet scalable message broker with support for producers, consumers, topics, partitions, and consumer groups.

---

## 🚀 Features
- **Topics and Partitions**: Create topics with multiple partitions for parallel message processing.
- **Producers**: Send messages to specific topics with optional keys for partitioning.
- **Consumers**: Read messages in a consumer group with offset tracking.
- **Scalable**: Designed to handle multiple producers and consumers.
- **Persistence**: Messages are stored in a database (Django ORM) for durability.
- **HTTP API**: Easy integration with RESTful endpoints for producing and consuming messages.

---

## 🛠️ Getting Started

### 📋 Prerequisites
- Python 3.8+
- Django 4.0+
- PostgreSQL (or any Django-supported database)

---

### 📥 Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/hey-granth/django-kafka.git
    cd django-kafka
    ```

2. **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    - Update `settings.py` with your database configuration.
    - Run migrations:
    ```bash
    python manage.py migrate
    ```

5. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

---

## 🚀 Usage

### 1. **Create a Topic**
Use the API to create a topic with a specified number of partitions:

```bash
curl -X POST http://localhost:8000/api/topics/ \
  -H "Content-Type: application/json" \
  -d '{"name": "orders", "partitions": 3}'
```
### 2. **Produce Messages**
Send messages to a topic using the producer CLI:

**Single Message:**
    
```bash
python manage.py produce orders --key "user123" --value "Order placed for 2 items"
```
**Bulk Messages from a File:**
```bash
python manage.py produce orders --file orders.csv
```
**Example** `orders.csv`:
```csv
user123,Order placed for 2 items
user456,Order placed for 1 item
user123,Payment received
```
### 3. **Consume Messages**
Start a consumer to read messages from a topic:
```bash
python manage.py consume [GROUP_ID] orders
```
Replace `[GROUP_ID]` with a unique identifier for your consumer group.

Messages will be printed to the console as they are consumed.

---

## 🏗️ Architecture
### Components
- **Broker**: Manages topics, partitions, and message storage.
- **Producer**: Sends messages to topics.
- **Consumer**: Reads messages from topics in a consumer group.
- **Database**: Stores messages and consumer offsets.
### Workflow
1. Producers send messages to topics.
2. Messages are partitioned based on their key.
3. Consumers in a group read messages from partitions, tracking their offsets.
4. Offsets are stored to ensure messages are not reprocessed.
---
## 💡 Example Use Cases
- **Order Processing**: Stream orders from producers to multiple consumers for processing.
- **Log Aggregation**: Collect logs from multiple services into a central topic.
- **Event Sourcing**: Track changes to application state as a sequence of events.
---
## 🤝 Contributing
Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.
---
## 🙏 Acknowledgments
- Inspired by Apache Kafka.
- Built with Django and Django REST framework.
- Made with love by [Granth Agarwal](https://github.com/hey-granth).