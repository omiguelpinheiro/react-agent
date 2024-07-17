# Testing request
curl -X POST http://0.0.0.0:8000/generate \
-H "Content-Type: application/json" \
-d '{"user_query": "Which assets Client_1 have a target allocation smaller than 40%?", "session_id": "123"}'

# Testing memory
curl -X POST http://0.0.0.0:8000/generate \
-H "Content-Type: application/json" \
-d '{"user_query": "What about smaller or equal to 15% for Client_1?", "session_id": "123"}'

# Testing querying advisors_clients
curl -X POST http://0.0.0.0:8000/generate \
-H "Content-Type: application/json" \
-d '{"user_query": "Which of my clients have tesla stocks?", "session_id": "123"}'

# Testing filling up null values
curl -X POST http://0.0.0.0:8000/generate \
-H "Content-Type: application/json" \
-d '{"user_query": "In what asset Client 35 have 5% target allocation? Also give me his Profile", "session_id": "123"}'
