from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_API = "https://akiru-jwt-10.vercel.app/token"

CREDITS = {
    "api_source_credit": "@NR_CODRX",
    "api_credit": "@NILAY_VII",
    "telegram_channel": "@nr_codex"
}

@app.route('/token', methods=['GET'])
def get_token():
    uid = request.args.get('uid')
    password = request.args.get('password')
    
    if not uid or not password:
        logger.error("Missing uid or password in request")
        return jsonify({"error": "Missing uid or password"}), 400
    
    try:
        target_url = f"{TARGET_API}?uid={uid}&password={password}"
        logger.info(f"Requesting target API: {target_url}")
        
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        
        target_response = response.json()
        
        response_with_credits = {
            **target_response,
            "credits": CREDITS
        }
        
        logger.info("Successfully fetched response from target API")
        return jsonify(response_with_credits), 200
        
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return jsonify({
            "error": "Failed to fetch token from target API",
            "status_code": response.status_code,
            "details": str(http_err)
        }), response.status_code
        
    except requests.exceptions.Timeout:
        logger.error("Request to target API timed out")
        return jsonify({
            "error": "Request to target API timed out",
            "details": "The target API took too long to respond"
        }), 504
        
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to target API")
        return jsonify({
            "error": "Failed to connect to target API",
            "details": "Could not establish a connection to the target API"
        }), 502
        
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")
        return jsonify({
            "error": "An error occurred while fetching the token",
            "details": str(req_err)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Server is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)