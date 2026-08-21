"""Tests for ClickHouse MCP integration."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.integrations.clickhouse_mcp import (
    ClickHouseMCPClient,
    ClickHouseConfig,
    get_clickhouse_client
)


def test_config_creation():
    """Test ClickHouse config creation."""
    config = ClickHouseConfig()
    assert config.host == "localhost"
    assert config.port == 8123
    assert config.database == "cinepilot"
    print("✅ Config creation test passed")


def test_client_creation():
    """Test ClickHouse client creation."""
    client = get_clickhouse_client()
    assert client is not None
    assert isinstance(client, ClickHouseMCPClient)
    print("✅ Client creation test passed")


def test_connection():
    """Test ClickHouse connection."""
    client = ClickHouseMCPClient()
    result = client.connect()
    assert result == True
    print("✅ Connection test passed")


if __name__ == "__main__":
    test_config_creation()
    test_client_creation()
    test_connection()
    print("\n🎉 All ClickHouse tests passed!")
