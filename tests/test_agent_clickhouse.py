"""Test agent integration with ClickHouse."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.integrations.clickhouse_mcp import ClickHouseMCPClient
from app.tools.screenplay_tools import production_breakdown


def test_production_breakdown_with_clickhouse():
    """Test production breakdown with ClickHouse storage."""
    
    screenplay = """
INT. COFFEE SHOP - DAY
John enters carrying a black backpack.
A phone rings.

JOHN
Sarah? I didn't expect to see you here.

SARAH
Neither did I.
"""
    
    # Get production data
    data = production_breakdown(screenplay)
    assert data["success"] == True
    
    # Store in ClickHouse
    client = ClickHouseMCPClient()
    client.connect()
    result = client.store_production_data(data)
    assert result == True
    
    print("✅ Production breakdown with ClickHouse test passed")


if __name__ == "__main__":
    test_production_breakdown_with_clickhouse()
    print("\n🎉 Agent-ClickHouse integration test passed!")
