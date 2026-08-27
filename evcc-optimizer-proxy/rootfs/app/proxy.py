"""
Proxy module for forwarding and modifying EVCC Optimizer requests.
Handles NTLM proxy support and request modification.
"""

import json
import logging
import requests
from requests_ntlm import HttpNtlmAuth
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class EvccProxy:
    """Proxy class for EVCC Optimizer requests."""
    
    def __init__(self, config):
        """Initialize proxy with configuration."""
        self.config = config
        self.session = self._create_session()
    
    def _create_session(self):
        """Create a requests session with proxy configuration."""
        session = requests.Session()
        
        proxy_url = self.config.get('proxy_url')
        use_system_proxy = self.config.get('use_system_proxy', True)
        
        if proxy_url:
            logger.info(f"Configuring proxy: {proxy_url}")
            
            proxy_username = self.config.get('proxy_username')
            proxy_password = self.config.get('proxy_password', '')
            
            # Configure NTLM authentication if credentials provided
            if proxy_username:
                logger.debug(f"Using NTLM authentication for proxy with user: {proxy_username}")
                session.auth = HttpNtlmAuth(proxy_username, proxy_password)
            
            # Set proxy for both http and https
            session.proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
        elif use_system_proxy:
            logger.info("Using system proxy settings")
            # requests library automatically uses system proxy settings
            # On Windows: HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Internet Settings
            # On Linux/Mac: HTTP_PROXY, HTTPS_PROXY environment variables
        
        return session
    
    def modify_request(self, data):
        """
        Modify the request to ensure charge_from_grid and discharge_to_grid are true.
        
        Args:
            data (dict): The original request data
            
        Returns:
            dict: Modified request data
        """
        modified_data = json.loads(json.dumps(data))  # Deep copy
        
        # Ensure batteries array exists
        if 'batteries' not in modified_data:
            modified_data['batteries'] = []
        
        # Modify each battery in the array
        for battery in modified_data['batteries']:
            logger.debug(f"Battery before modification: {battery}")
            
            battery['charge_from_grid'] = True
            battery['discharge_to_grid'] = True
            
            logger.debug(f"Battery after modification: {battery}")
        
        # Also check if there's a single battery object (not in array)
        if 'battery' in modified_data and isinstance(modified_data['battery'], dict):
            modified_data['battery']['charge_from_grid'] = True
            modified_data['battery']['discharge_to_grid'] = True
        
        logger.info("Request modification completed")
        return modified_data
    
    def forward_request(self, data, target_path='', headers=None):
        """
        Forward the modified request to the EVCC Optimizer server.
        
        Args:
            data (dict): The modified request data
            
        Returns:
            tuple: (status_code, response_data)
        """
        target_url = self.config.get('target_url')
        
        try:
            destination_url = target_url.rstrip('/')
            if target_path:
                destination_url = f"{destination_url}/{target_path.lstrip('/')}"

            logger.info(f"Forwarding request to {destination_url}")
            logger.debug(
                "Request transport settings: trust_env=%s, configured_proxies=%s, "
                "proxy_auth=%s",
                self.session.trust_env,
                bool(self.session.proxies),
                bool(self.session.auth)
            )
            
            # Send POST request with JSON data
            response = self.session.post(
                destination_url,
                json=data,
                headers=headers,
                timeout=30,
                verify=True  # Verify SSL certificates
            )
            
            logger.info(f"Response status: {response.status_code}")
            
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text
            
            return response.status_code, response_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error forwarding request: {str(e)}")
            logger.debug("Request failure details", exc_info=True)
            error_response = {
                'error': 'Failed to forward request to EVCC Optimizer',
                'details': str(e)
            }
            return 502, error_response
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return 500, {'error': str(e)}
