#!/usr/bin/env python3
"""
Simple HTTP client for testing the EVCC Optimizer Proxy.
Usage: python test_client.py [target_url] [proxy_url]
"""

import json
import sys
import requests
from pathlib import Path


def load_sample_request():
    """Load the sample request from EvccOptimizerRequest.json."""
    json_file = Path(__file__).parent / 'EvccOptimizerRequest.json'
    if json_file.exists():
        with open(json_file, 'r') as f:
            return json.load(f)
    else:
        # Return a minimal sample
        return {
            "batteries": [
                {
                    "c_max": 5000,
                    "c_min": 0,
                    "charge_from_grid": False,
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


def run_proxy_test(proxy_url='http://localhost:8080'):
    """Test the proxy with a sample request."""
    print("=" * 60)
    print("EVCC Optimizer Proxy Test Client")
    print("=" * 60)
    print(f"\nTarget Proxy: {proxy_url}")
    
    # Load sample request
    print("\nLoading sample request...")
    sample_data = load_sample_request()
    
    # Show original battery data
    print("\nOriginal Battery Data:")
    print(json.dumps(sample_data['batteries'][0], indent=2))
    
    # Send request to proxy
    print(f"\nSending request to {proxy_url}/proxy...")
    try:
        response = requests.post(
            f'{proxy_url}/proxy',
            json=sample_data,
            timeout=10
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print("\nResponse Body:")
        try:
            response_data = response.json()
            print(json.dumps(response_data, indent=2))
        except:
            print(response.text)
        
        if response.status_code == 200:
            print("\n✓ Test successful!")
        else:
            print(f"\n✗ Test failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"\n✗ Could not connect to {proxy_url}")
        print("Make sure the proxy is running!")
        return False
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Request error: {e}")
        return False
    
    return True


def run_health_test(proxy_url='http://localhost:8080'):
    """Test the health endpoint."""
    print("\n" + "=" * 60)
    print("Testing Health Endpoint")
    print("=" * 60)
    
    try:
        response = requests.get(f'{proxy_url}/health', timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✓ Health check passed!")
            return True
        else:
            print("✗ Health check failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Could not connect to {proxy_url}")
        return False


def run_config_test(proxy_url='http://localhost:8080'):
    """Test the config endpoint."""
    print("\n" + "=" * 60)
    print("Testing Configuration Endpoint")
    print("=" * 60)
    
    try:
        response = requests.get(f'{proxy_url}/config', timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            config = response.json()
            print("\nCurrent Configuration:")
            print(json.dumps(config, indent=2))
            print("✓ Config endpoint working!")
            return True
        else:
            print("✗ Config endpoint failed!")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"✗ Could not connect to {proxy_url}")
        return False


if __name__ == '__main__':
    proxy_url = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8080'
    
    results = []
    results.append(('Health Check', run_health_test(proxy_url)))
    results.append(('Config Endpoint', run_config_test(proxy_url)))
    results.append(('Proxy Request', run_proxy_test(proxy_url)))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(r for _, r in results)
    print("\n" + ("All tests passed! ✓" if all_passed else "Some tests failed! ✗"))
    sys.exit(0 if all_passed else 1)
