#!/bin/bash

# Couleurs pour le output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Fichier de log
OUTPUT_FILE="tests/test_api/api_tests_$(date +%Y%m%d_%H%M%S).log"

# Fonction pour logger
log_test() {
    echo -e "${YELLOW}Testing: $1${NC}"
    echo "=== Testing: $1 ===" >> "$OUTPUT_FILE"
    echo "$2" >> "$OUTPUT_FILE"
    echo -e "\n" >> "$OUTPUT_FILE"
}

# URL de base
BASE_URL="http://localhost:5000/api/v1"

echo "Starting API tests..." | tee -a "$OUTPUT_FILE"
echo "$(date)" | tee -a "$OUTPUT_FILE"
echo "----------------------------------------" | tee -a "$OUTPUT_FILE"

# 1. Routes Publiques
echo -e "\n${GREEN}Testing Public Routes:${NC}" | tee -a "$OUTPUT_FILE"

# Documentation
log_test "GET / (Documentation)" "$(curl -s $BASE_URL/)"

# Login (avec mauvais credentials)
log_test "POST /auth/login (Bad Credentials)" "$(curl -s -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "wrong@email.com",
        "password": "wrongpass"
    }')"

# Login (avec bons credentials)
RESPONSE=$(curl -s -X POST $BASE_URL/auth/login \
    -H "Content-Type: application/json" \
    -d '{
        "email": "admin@hbnb.io",
        "password": "admin1234"
    }')
log_test "POST /auth/login (Good Credentials)" "$RESPONSE"

# Extraire le token
TOKEN=$(echo $RESPONSE | jq -r '.token')

# 2. Routes Protégées (sans auth)
echo -e "\n${GREEN}Testing Protected Routes without Auth:${NC}" | tee -a "$OUTPUT_FILE"

# Users
log_test "GET /users (No Auth)" "$(curl -s $BASE_URL/users)"

# Places
log_test "GET /places (No Auth)" "$(curl -s $BASE_URL/places)"

# 3. Routes Protégées (avec auth)
echo -e "\n${GREEN}Testing Protected Routes with Auth:${NC}" | tee -a "$OUTPUT_FILE"

# Users
log_test "GET /users (With Auth)" "$(curl -s -H "Authorization: Bearer $TOKEN" $BASE_URL/users)"

# Places
log_test "GET /places (With Auth)" "$(curl -s -H "Authorization: Bearer $TOKEN" $BASE_URL/places)"

# 4. Routes Admin Only
echo -e "\n${GREEN}Testing Admin Only Routes:${NC}" | tee -a "$OUTPUT_FILE"

# Delete user
log_test "DELETE /users/some-id (Admin)" "$(curl -s -X DELETE -H "Authorization: Bearer $TOKEN" $BASE_URL/users/some-id)"

echo -e "\n${GREEN}Tests completed! Check $OUTPUT_FILE for details${NC}"