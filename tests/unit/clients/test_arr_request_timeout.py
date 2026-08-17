"""Tests for the request_timeout setting in ArrClient API calls."""

from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from rangarr.clients.arr import ArrClient
from rangarr.clients.arr import RadarrClient
from tests.builders import ClientBuilder

_request_timeout_cases = {
    'default_timeout': {
        'timeout': None,
        'expected_timeout': 30,
    },
    'custom_timeout': {
        'timeout': 120,
        'expected_timeout': 120,
    },
}


def _build_client(timeout: int | None) -> ArrClient:
    """Build a Radarr client with or without an explicit request_timeout."""
    builder = ClientBuilder(RadarrClient)
    if timeout is not None:
        builder = builder.with_settings(request_timeout=timeout)
    return builder.build()


@pytest.mark.parametrize(
    'timeout, expected_timeout',
    [(case['timeout'], case['expected_timeout']) for case in _request_timeout_cases.values()],
    ids=list(_request_timeout_cases.keys()),
)
def test_fetch_unlimited_request_timeout(timeout: int | None, expected_timeout: int) -> None:
    """Test that _fetch_unlimited passes the configured or default request_timeout.

    Args:
        timeout: request_timeout to set in client settings; None to use the default.
        expected_timeout: Expected timeout kwarg in the API request.
    """
    client = _build_client(timeout)
    mock_resp = MagicMock()
    mock_resp.json.return_value = {'records': []}
    mock_resp.raise_for_status.return_value = None

    with patch.object(client.session, 'get', return_value=mock_resp) as mock_get:
        client._fetch_unlimited('/api/v3/wanted/missing')

    assert mock_get.call_args_list[0].kwargs['timeout'] == expected_timeout


@pytest.mark.parametrize(
    'timeout, expected_timeout',
    [(case['timeout'], case['expected_timeout']) for case in _request_timeout_cases.values()],
    ids=list(_request_timeout_cases.keys()),
)
def test_trigger_single_request_timeout(timeout: int | None, expected_timeout: int) -> None:
    """Test that _trigger_single passes the configured or default request_timeout.

    Args:
        timeout: request_timeout to set in client settings; None to use the default.
        expected_timeout: Expected timeout kwarg in the API request.
    """
    client = _build_client(timeout)
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None

    with patch.object(client.session, 'post', return_value=mock_resp) as mock_post:
        client._trigger_single(1, 'missing', 'Example Movie', 1, 1)

    assert mock_post.call_args_list[0].kwargs['timeout'] == expected_timeout
