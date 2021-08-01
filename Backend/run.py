from App import app
from waitress import serve

serve(app, host="0.0.0.0", port=5000, max_request_body_size=20 * 1000 * 1000 * 1000)
