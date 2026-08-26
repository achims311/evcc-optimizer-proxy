#!/usr/bin/env python3
"""
Test script for EVCC Optimizer Proxy.
"""

import sys
import json
import requests
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / 'rootfs' / 'app'))

from proxy import EvccProxy
from config_handler import ConfigHandler


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
    assert modified_data['batteries'][0]['export_to_grid'] == True, "export_to_grid should be True"
    
    print("\n✓ Request modification test passed!")
    return True


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
    return True


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
