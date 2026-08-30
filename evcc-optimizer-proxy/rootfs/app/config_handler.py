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
        'proxy_url': '',
        'proxy_username': '',
        'proxy_password': None,
        'use_system_proxy': True,
        'log_level': 'INFO',
        'eta_c': None,
        'eta_d': None
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
                    self._normalize_config()
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
            'LOG_LEVEL': 'log_level',
            'ETA_C': 'eta_c',
            'ETA_D': 'eta_d'
        }
        
        for env_var, config_key in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                
                # Convert string boolean to actual boolean
                if config_key == 'use_system_proxy' and isinstance(value, str):
                    value = value.lower() in ('true', '1', 'yes')
                
                self.config[config_key] = value
                logger.debug(f"Set {config_key} from environment")

        self._normalize_config()

    def _normalize_config(self):
        """Normalize optional string values from Home Assistant."""
        for key in ('proxy_url', 'proxy_username'):
            if self.config.get(key) is None:
                self.config[key] = ''

        for key in ('eta_c', 'eta_d'):
            value = self.config.get(key)
            if value in (None, ''):
                self.config[key] = None
                continue

            try:
                value = float(value)
            except (TypeError, ValueError):
                value = None

            if value is None or not 0 < value < 1:
                logger.warning("Ignoring invalid %s value; it must be between 0 and 1", key)
                self.config[key] = None
            else:
                self.config[key] = value
    
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
            self._normalize_config()
            self._save_config()
            return True
        except Exception as e:
            logger.error(f"Error updating configuration: {e}")
            raise

    def _save_config(self):
        """Persist configuration changes for subsequent application starts."""
        options_file = '/data/options.json'
        saved_config = {}

        if os.path.exists(options_file):
            with open(options_file, 'r') as f:
                saved_config = json.load(f)

        saved_config.update({
            key: self.config[key]
            for key in self.DEFAULTS
            if key != 'proxy_password' and key in self.config
        })

        temporary_file = f'{options_file}.tmp'
        with open(temporary_file, 'w') as f:
            json.dump(saved_config, f)
        os.replace(temporary_file, options_file)
