#!/usr/bin/env python3
"""
EVCC Optimizer Proxy - Home Assistant Add-on
Modifies EVCC Optimizer requests to ensure charge_from_grid and export_to_grid are true.
"""

import json
import logging
from flask import Flask, request, jsonify
from config_handler import ConfigHandler
from proxy import EvccProxy

# Initialize Flask app
app = Flask(__name__)

# Initialize configuration and proxy
config = ConfigHandler()


def configure_logging():
    """Configure application logging from the active add-on configuration."""
    log_level = str(config.get('log_level') or 'INFO').upper()
    level = getattr(logging, log_level, logging.INFO)
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True
    )
    logging.getLogger('urllib3').setLevel(logging.DEBUG if level == logging.DEBUG else logging.WARNING)


configure_logging()
logger = logging.getLogger(__name__)
proxy = EvccProxy(config)

HOP_BY_HOP_HEADERS = {
    'connection',
    'content-encoding',
    'content-length',
    'host',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailer',
    'transfer-encoding',
    'upgrade',
}


def get_forward_headers():
    """Return request headers that are valid for a new upstream request."""
    connection_headers = {
        name.strip().lower()
        for value in request.headers.getlist('Connection')
        for name in value.split(',')
        if name.strip()
    }
    excluded_headers = HOP_BY_HOP_HEADERS | connection_headers
    return {
        name: value
        for name, value in request.headers.items()
        if name.lower() not in excluded_headers
    }


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Home Assistant."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/proxy', defaults={'target_path': ''}, methods=['GET', 'POST'])
@app.route('/proxy/<path:target_path>', methods=['GET', 'POST'])
def handle_proxy(target_path):
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
        response_status, response_data = proxy.forward_request(
            modified_data,
            target_path,
            get_forward_headers()
        )
        
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
            configure_logging()
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
    logger.info(f"Log level: {str(config.get('log_level') or 'INFO').upper()}")
    serve(app, host='0.0.0.0', port=8080)
