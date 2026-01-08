
# ═══════════════════════════════════════════════════════════════════════════
# STROM CRUD - First-Class Calibration Streams (5 Endpoints)
# ═══════════════════════════════════════════════════════════════════════════

print_header "🌊 STROM CRUD - First-Class Calibration Streams (5 Endpoints)"

test_endpoint "GET" "/strom" "List All Streams - Complete Stream Registry"
test_endpoint "GET" "/strom/example_morning_strom" "Get Single Stream - Morning Calibration Flow"
test_endpoint "POST" "/strom" "Create New Stream - Test Stream Creation" '{"name":"API Test Stream","zeitplan":"0 9 * * *","modell":"gpt-4o","felder_topics":{"test":0.7},"styles":["technisch"],"sprachen":["de"]}'
test_endpoint "PUT" "/strom/api_test_stream" "Update Stream - Modify Test Stream" '{"zeitplan":"0 10 * * *","felder_topics":{"test":0.9}}'
test_endpoint "DELETE" "/strom/api_test_stream" "Delete Stream - Remove Test Stream"

