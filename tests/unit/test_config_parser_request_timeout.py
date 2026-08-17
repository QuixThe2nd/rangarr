"""Tests for the request_timeout setting in config_parser.py."""

import re
from typing import Any

import pytest

from rangarr.config_parser import parse_config
from tests.helpers import assert_config_result

_BASE_INSTANCE = {
    'type': 'radarr',
    'host': 'http://test',
    'api_key': 'testkey',
    'enabled': True,
}

_parse_config_request_timeout_cases = {
    'request_timeout_default': {
        'config_data': {
            'instances': {'test-instance': _BASE_INSTANCE},
            'global': {},
        },
        'expected_result': {
            'global_settings': {
                'request_timeout': 30,
            },
        },
    },
    'request_timeout_custom': {
        'config_data': {
            'instances': {'test-instance': _BASE_INSTANCE},
            'global': {
                'request_timeout': 120,
            },
        },
        'expected_result': {
            'global_settings': {
                'request_timeout': 120,
            },
        },
    },
    'request_timeout_minimum_valid': {
        'config_data': {
            'instances': {'test-instance': _BASE_INSTANCE},
            'global': {
                'request_timeout': 1,
            },
        },
        'expected_result': {
            'global_settings': {
                'request_timeout': 1,
            },
        },
    },
    'request_timeout_rejects_zero': {
        'config_data': {
            'instances': {'test-instance': _BASE_INSTANCE},
            'global': {
                'request_timeout': 0,
            },
        },
        'expected_error': "'global.request_timeout' must be at least 1.",
    },
    'request_timeout_rejects_negative': {
        'config_data': {
            'instances': {'test-instance': _BASE_INSTANCE},
            'global': {
                'request_timeout': -1,
            },
        },
        'expected_error': "'global.request_timeout' must be at least 1.",
    },
    'request_timeout_rejects_wrong_type': {
        'config_data': {
            'instances': {'test-instance': _BASE_INSTANCE},
            'global': {
                'request_timeout': '120',
            },
        },
        'expected_error': "'global.request_timeout' must be of type int.",
    },
}


@pytest.mark.parametrize(
    'config_data, expected_error, expected_result',
    [
        (
            case['config_data'],
            case.get('expected_error'),
            case.get('expected_result'),
        )
        for case in _parse_config_request_timeout_cases.values()
    ],
    ids=list(_parse_config_request_timeout_cases.keys()),
)
def test_parse_config_request_timeout(config_data: Any, expected_error: Any, expected_result: Any) -> None:
    """Test parse_config validates the request_timeout setting.

    Args:
        config_data: The raw configuration dictionary to validate.
        expected_error: Expected validation error message, if any.
        expected_result: Expected values in the parsed configuration, if valid.
    """
    if expected_error:
        with pytest.raises(ValueError, match=re.escape(expected_error)):
            parse_config(config_data)
    else:
        assert_config_result(parse_config(config_data), expected_result)
