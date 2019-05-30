# Service REST API specification

Authentication:

    HTTP_X_TOKEN: 32-bit service auth token in request header

API Throttling settings:

    anon: 10 requests per day
    user: 1000 requests per hour

<hr>Retrieving text check results.

    /api/result/<message_id>/

Allowed requests: GET.<br/><br>
Request parameters:
- message_id: 32-length hex integer, unique text identifier.

Response:<br/>
```json
{
    "message_id": "str, message_id from request",
    "check_result": "bool, service text checking result"
}
```
<hr>Initiating text checking process.

    /api/check/

Allowed requests: POST.<br/>

Request:
```json
{
    "message_id": "str, 32-length hex integer, unique text identifier",
    "language": "str, 2-length, language code",
    "headline": "str, news article headline",
    "cleared_text": "str, news article text, prepared for analysis (stemmed, cleared, checked for correctness, stopwords deleted)"
}
```

Response:
```json
{
    "message_id": "str, message_id from request",
    "check_result": "bool, service text checking result"
}
```