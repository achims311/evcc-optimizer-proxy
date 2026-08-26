#!/usr/bin/env python3
"""
EVCC Optimizer Proxy - Home Assistant Add-on
Modifies EVCC Optimizer requests to ensure charge_from_grid and export_to_grid are true.
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from proxy import EvccProxy
from config_handler import ConfigHandler

# Configure logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Initialize configuration and proxy
config = ConfigHandler()
proxy = EvccProxy(config)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Home Assistant."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/proxy', methods=['GET', 'POST'])
def handle_proxy():
    """
    Main proxy endpoint that receives and forwards requests to EVCC Optimizer.
    Modifies the request to ensure charge_from_grid and export_to_grid are true.
    """
    try:
        # Parse incoming request data
        if request.method == 'POST':
            data = request.get_json()
        else:
            # For GET requests, try to get JSON from args or body
            data = request.get_json(force=True, silent=True)
            if not data:
                return jsonify({'error': 'Invalid JSON data'}), 400
        
        logger.debug(f"Received request: {json.dumps(data, indent=2)}")
        
        # Modify the request
        modified_data = proxy.modify_request(data)
        logger.debug(f"Modified request: {json.dumps(modified_data, indent=2)}")
        
        # Forward to EVCC Optimizer
        response_status, response_data = proxy.forward_request(modified_data)
        
        logger.debug(f"Response status: {response_status}")
        
        if response_status == 200:
            return jsonify(response_data), response_status
        else:
            return jsonify(response_data), response_status
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/config', methods=['GET', 'POST'])
def handle_config():
    """Endpoint to view/update configuration."""
    if request.method == 'GET':
        return jsonify(config.get_config()), 200
    elif request.method == 'POST':
        try:
            new_config = request.get_json()
            config.update_config(new_config)
            return jsonify({'status': 'Configuration updated'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@app.route('/', methods=['GET'])
def index():
    """Root endpoint."""
    return jsonify({
        'name': 'EVCC Optimizer Proxy',
        'version': '1.0.0',
        'endpoints': {
            '/health': 'Health check',
            '/proxy': 'Proxy endpoint for EVCC Optimizer requests',
            '/config': 'Configuration management'
        }
    }), 200


if __name__ == '__main__':
    from waitress import serve
    logger.info("Starting EVCC Optimizer Proxy...")
    logger.info(f"Target URL: {config.get('target_url')}")
    serve(app, host='0.0.0.0', port=8080)
