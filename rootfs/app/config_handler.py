"""
Configuration handler for EVCC Optimizer Proxy.
Reads configuration from Home Assistant options or environment variables.
"""

import os
import json
import logging

logger = logging.getLogger(__name__)


class ConfigHandler:
    """Handle application configuration."""
    
    # Default configuration
    DEFAULTS = {
        'target_url': 'https://optimizer.evcc.io',
        'proxy_url': None,
        'proxy_username': None,
        'proxy_password': None,
        'use_system_proxy': True,
        'log_level': 'INFO'
    }
    
    def __init__(self):
        """Initialize configuration from Home Assistant or environment."""
        self.config = self.DEFAULTS.copy()
        self._load_config()
    
    def _load_config(self):
        """Load configuration from various sources."""
        # Try to load from Home Assistant options file
        options_file = '/data/options.json'
        if os.path.exists(options_file):
            try:
                with open(options_file, 'r') as f:
                    ha_options = json.load(f)
                    self.config.update(ha_options)
                    logger.info("Configuration loaded from Home Assistant options")
                    return
            except Exception as e:
                logger.warning(f"Could not read Home Assistant options file: {e}")
        
        # Fall back to environment variables
        logger.info("Loading configuration from environment variables")
        env_mappings = {
            'TARGET_URL': 'target_url',
            'PROXY_URL': 'proxy_url',
            'PROXY_USERNAME': 'proxy_username',
            'PROXY_PASSWORD': 'proxy_password',
            'USE_SYSTEM_PROXY': 'use_system_proxy',
            'LOG_LEVEL': 'log_level'
        }
        
        for env_var, config_key in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                
                # Convert string boolean to actual boolean
                if config_key == 'use_system_proxy' and isinstance(value, str):
                    value = value.lower() in ('true', '1', 'yes')
                
                self.config[config_key] = value
                logger.debug(f"Set {config_key} from environment")
    
    def get(self, key, default=None):
        """Get a configuration value."""
        return self.config.get(key, default)
    
    def get_config(self):
        """Get all configuration (excluding sensitive data)."""
        safe_config = self.config.copy()
        # Remove password from output
        if 'proxy_password' in safe_config:
            safe_config['proxy_password'] = '***REDACTED***'
        return safe_config
    
    def update_config(self, new_config):
        """Update configuration (for runtime updates)."""
        try:
            for key, value in new_config.items():
                if key in self.DEFAULTS:
                    self.config[key] = value
                    logger.info(f"Updated configuration: {key}")
            return True
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            raise
