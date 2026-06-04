# API Documentation

## Running the Server
Ensure you have installed the dependencies:
```bash
pip install -r api/requirements.txt
```
Start the server:
```bash
python -m api.app
```
*Note: Make sure to run it from the `codebase` root directory.*

## Endpoints

### 1. Process Query
**URL:** `/api/query`
**Method:** `POST`
**Payload:**
```json
{
  "query": "Giao nhanh",
  "location": "Ocean Park 1"
}
```
**Response:**
Returns a JSON object with `suggestions`, `action_trace`, and `execution_time_ms`.

### 2. Submit Feedback
**URL:** `/api/feedback`
**Method:** `POST`
**Payload:**
```json
{
  "query": "Giao nhanh",
  "suggestion_id": 1,
  "rating": 5,
  "text": "Great suggestion!"
}
```
**Response:**
```json
{"status": "success"}
```