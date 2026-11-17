"""Validate webhook endpoint URLs before they are stored."""

import ipaddress
from urllib.parse import urlsplit

from hooksvc.errors import InvalidEndpointError


def validate_endpoint(url: str) -> str:
    """Return the URL when it is an allowed HTTPS target, otherwise raise."""
    parts = urlsplit(url)
    if parts.scheme != "https":
        raise InvalidEndpointError("endpoint must use https")
    if not parts.hostname:
        raise InvalidEndpointError("endpoint must name a host")
    try:
        address = ipaddress.ip_address(parts.hostname)
    except ValueError:
        return url
    if address.is_private or address.is_loopback or address.is_link_local:
        raise InvalidEndpointError("endpoint must not target a private address")
    return url
