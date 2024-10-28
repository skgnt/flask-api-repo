# Flask RESTful API with SQLite

This project is a simple RESTful API built with Flask and SQLite. The API allows you to log and retrieve server monitoring data.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/githubnext/hello-world.git
   cd hello-world
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask application:
   ```bash
   flask run
   ```

## API Endpoints

### POST /log

Add a new log entry to the database.

#### Request Body

When status is success:
```json
{
  "cpu_usage": cpu_usage,
  "gpu_usage": gpu_usage,
  "gpu_memory_usage": gpu_memory_usage,
  "memory_usage": memory_usage,
  "status": "success",
  "server": server_name
}
```

When status is failed:
```json
{
  "server": server_name,
  "status": "failed",
  "error": error_msg
}
```

#### Response

```json
{
  "message": "Log added successfully"
}
```

### GET /log

Retrieve the latest log entries for each server recorded within the past day.

#### Response

When status is success:
```json
[
  {
    "cpu_usage": cpu_usage,
    "gpu_usage": gpu_usage,
    "gpu_memory_usage": gpu_memory_usage,
    "memory_usage": memory_usage,
    "status": "success",
    "server": server_name
  }
]
```

When status is failed:
```json
[
  {
    "server": server_name,
    "status": "failed",
    "error": error_msg
  }
]
```
