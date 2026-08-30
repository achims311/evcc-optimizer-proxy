#!/usr/bin/env python3
"""
Test script for EVCC Optimizer Proxy.
"""

import sys
import json
import requests
from pathlib import Path
from unittest.mock import patch

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / 'rootfs' / 'app'))

from proxy import EvccProxy
from config_handler import ConfigHandler


class ProxyConfig(dict):
    """Minimal configuration object for proxy unit tests."""

    def get(self, key, default=None):
        return super().get(key, default)


def test_request_modification():
    """Test the request modification logic."""
    print("=" * 50)
    print("Testing Request Modification")
    print("=" * 50)
    
    config = ConfigHandler()
    proxy = EvccProxy(config)
    
    # Sample request data
    sample_data = {
        "batteries": [
            {
                "c_max": 5000,
                "c_min": 0,
                "charge_from_grid": False,  # Should be modified to True
                "d_max": 5000,
                "p_a": 0.00018822195,
                "s_capacity": 9600,
                "s_initial": 8885.106,
                "s_max": 9600,
                "s_min": 1440
            }
        ],
        "eta_c": 0.9,
        "eta_d": 0.9,
        "grid": {},
        "strategy": {
            "charging_strategy": "attenuate_grid_peaks",
            "discharging_strategy": "discharge_before_import"
        }
    }
    
    print("\nOriginal Request:")
    print(json.dumps(sample_data['batteries'][0], indent=2))
    
    modified_data = proxy.modify_request(sample_data)
    
    print("\nModified Request:")
    print(json.dumps(modified_data['batteries'][0], indent=2))
    
    # Verify modifications
    assert modified_data['batteries'][0]['charge_from_grid'] == True, "charge_from_grid should be True"
    assert modified_data['batteries'][0]['discharge_to_grid'] == True, "discharge_to_grid should be True"
    
    print("\n✓ Request modification test passed!")


def test_efficiency_overrides():
    """Test optional eta_c and eta_d request overrides."""
    data = {'eta_c': 0.9, 'eta_d': 0.8}

    unchanged = EvccProxy(ProxyConfig()).modify_request(data)
    assert unchanged['eta_c'] == 0.9
    assert unchanged['eta_d'] == 0.8

    modified = EvccProxy(ProxyConfig(eta_c=0.95, eta_d=0.85)).modify_request(data)
    assert modified['eta_c'] == 0.95
    assert modified['eta_d'] == 0.85

    boundary_values = EvccProxy(ProxyConfig(eta_c=0, eta_d=1)).modify_request(data)
    assert boundary_values['eta_c'] == 0.9
    assert boundary_values['eta_d'] == 0.8


def test_config_loading():
    """Test configuration loading."""
    print("\n" + "=" * 50)
    print("Testing Configuration Loading")
    print("=" * 50)
    
    config = ConfigHandler()
    
    print("\nConfiguration loaded:")
    print(json.dumps(config.get_config(), indent=2))
    
    # Check required keys
    required_keys = ['target_url', 'proxy_url', 'use_system_proxy', 'log_level']
    for key in required_keys:
        assert key in config.get_config(), f"Missing config key: {key}"
    
    print("\n✓ Configuration loading test passed!")


def test_proxy_forwards_path_headers_and_modified_body():
    """Test forwarding optimizer paths, end-to-end headers, and modified data."""
    from main import app

    request_data = {
        'batteries': [{
            'charge_from_grid': False,
            'discharge_to_grid': False,
        }]
    }
    with patch('main.proxy.forward_request', return_value=(200, {'optimized': True})) as forward_request:
        response = app.test_client().post(
            '/proxy/optimize/charge-schedule',
            json=request_data,
            headers={
                'Authorization': 'Bearer test-token',
                'Connection': 'keep-alive',
                'X-Request-ID': 'request-123',
            }
        )

    assert response.status_code == 200
    assert response.get_json() == {'optimized': True}
    forwarded_data, target_path, forwarded_headers = forward_request.call_args.args
    assert target_path == 'optimize/charge-schedule'
    assert forwarded_data['batteries'][0]['charge_from_grid'] is True
    assert forwarded_data['batteries'][0]['discharge_to_grid'] is True
    assert forwarded_headers['Authorization'] == 'Bearer test-token'
    assert forwarded_headers['X-Request-Id'] == 'request-123'
    assert 'Host' not in forwarded_headers
    assert 'Connection' not in forwarded_headers
    assert 'Content-Length' not in forwarded_headers


if __name__ == '__main__':
    try:
        test_config_loading()
        test_request_modification()
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
