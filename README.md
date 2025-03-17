# TELERAG-LLM-proxy

This repository represents a prototype of a broker service with LLM API gateaway. It uses FastAPI to provide an HTTP API and asyncio queues to simulate topics and partitions

## Features

- **Topics and Partitions:**
  Create topics with multiple partitions. Each partition is represented as a separate queue.
- **Producer API:**
  Send messages to a specified topic with an optional partition selection (if not specified, a random partition is chosen).
- **Consumer API:**
  Retrieve messages from a specific partition of a topic

## Requirments 

- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [uvicorn](https://www.uvicorn.org/)
- [httpx](https://www.python-httpx.org/)

```bash
git clone https://github.com/PP-TELERAG/TELERAG-LLM-proxy.git
cd TELERAG-LLM-proxy
python3 -m venv venv
source venv/bin/activate
pip -r requirments.txt
```

To run the project start server using uvicorn
```bash
uvicorn main:app --reload
```

## API Endpoints

1) `POST /topics`. Query parameters: `topic`(string) – topic nam, `partitions`(int) – Number of partitions (default: 1).
2) `POST /topics/{topic_name}/produce`. URL Parameters: `topic_name`(string) – Topic name. Query parameters: `partition`(int, optional) – Target partition. If omitted, a rangom partition is selected.
3) `GET /topics/{topic_name}/consume/{partition}`. URL Parameters: `topic_name`(string) – Topic name, `partition`(int) – Target partition.

## Additional notes
- This is a simplified implementation for prototyping purposes.
- Features such as offset tracking, consumer groups, and persistent storage are yet to be included.

## License

This project is licensed under MIT License. See LICENSE file for more details.
