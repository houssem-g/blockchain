curl -X 'POST' \
  'http://127.0.0.1:8000/v1/users/signup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "username": "string",
  "password": "string"
}'
echo
