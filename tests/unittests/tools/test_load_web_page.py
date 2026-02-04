# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from google.adk.tools.load_web_page import load_web_page


class TestLoadWebPage(unittest.TestCase):

  @patch('requests.get')
  def test_load_web_page_blocks_private_ip(self, mock_get):
    """Verifies that load_web_page blocks fetches to internal URLs."""
    # The internal URL that should be blocked
    url = 'http://localhost:8080/admin'

    # Call the function
    result = load_web_page(url)

    # Verify requests.get was NOT called
    mock_get.assert_not_called()
    self.assertIn('The url is restricted', result)

  @patch('requests.get')
  def test_load_web_page_blocks_private_ip_address(self, mock_get):
    """Verifies that load_web_page blocks fetches to private IP addresses."""
    # The internal IP that should be blocked
    url = 'http://192.168.1.1/admin'

    # Call the function
    result = load_web_page(url)

    # Verify requests.get was NOT called
    mock_get.assert_not_called()
    self.assertIn('The url is restricted', result)

  @patch('requests.get')
  @patch('socket.getaddrinfo')
  def test_load_web_page_allows_public_url(self, mock_getaddrinfo, mock_get):
    """Verifies that load_web_page allows fetches to public URLs."""
    # Mock socket resolution to a public IP
    # (family, type, proto, canonname, sockaddr)
    mock_getaddrinfo.return_value = [(2, 1, 6, '', ('8.8.8.8', 80))]

    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = (
        b'<html><body>Some Public Content For Testing</body></html>'
    )
    mock_get.return_value = mock_response

    url = 'http://example.com'

    # Call the function
    result = load_web_page(url)

    # Verify requests.get was called
    mock_get.assert_called_with(url, allow_redirects=False, timeout=10)
    self.assertIn('Some Public Content', result)


if __name__ == '__main__':
  unittest.main()
