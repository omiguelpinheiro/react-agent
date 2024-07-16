curl -X POST http://0.0.0.0:8000/generate \
-H "Content-Type: application/json" \
-d '{"user_query": "Which assets Client_1 have a target allocation smaller than 40%?", "session_id": "123"}'

curl -X POST http://0.0.0.0:8000/generate \
-H "Content-Type: application/json" \
-d '{"user_query": "What about smaller or equal to 15% for Client_1?", "session_id": "123"}'