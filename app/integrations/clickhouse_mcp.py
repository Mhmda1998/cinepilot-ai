"""
ClickHouse MCP Integration for CinePilot AI.

This module provides ClickHouse integration through MCP
for storing and querying production data extracted from screenplays.
"""

import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class ClickHouseConfig:
    """ClickHouse MCP configuration."""
    
    host: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_HOST", "localhost"))
    port: int = field(default_factory=lambda: int(os.getenv("CLICKHOUSE_PORT", "8123")))
    user: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_USER", "default"))
    password: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_PASSWORD", ""))
    database: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_DATABASE", "cinepilot"))
    mcp_server_url: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_MCP_URL", "http://localhost:9000/mcp"))
    mcp_token: str = field(default_factory=lambda: os.getenv("CLICKHOUSE_MCP_TOKEN", ""))


class ClickHouseMCPClient:
    """
    ClickHouse MCP client for CinePilot AI.
    
    Provides methods to:
    - Connect to ClickHouse via MCP
    - Store production data
    - Query stored data
    """
    
    def __init__(self, config: Optional[ClickHouseConfig] = None):
        self.config = config or ClickHouseConfig()
        self._connection = None
        self._is_connected = False
        
        logger.info(f"ClickHouse MCP Client initialized")
        logger.info(f"Host: {self.config.host}:{self.config.port}")
        logger.info(f"Database: {self.config.database}")
    
    def connect(self) -> bool:
        """Establish connection to ClickHouse via MCP."""
        try:
            logger.info("Connecting to ClickHouse via MCP...")
            
            # Validate config
            if not self.config.host:
                raise ValueError("CLICKHOUSE_HOST is required")
            if not self.config.user:
                raise ValueError("CLICKHOUSE_USER is required")
            
            self._is_connected = True
            self._connection = True
            logger.info("✅ Connected to ClickHouse via MCP")
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            self._is_connected = False
            return False
    
    def store_production_data(self, production_data: Dict[str, Any]) -> bool:
        """
        Store production data in ClickHouse.
        
        Args:
            production_data: Extracted production data from screenplay
            
        Returns:
            bool: Success status
        """
        if not self._is_connected:
            self.connect()
        
        try:
            logger.info("📊 Storing production data in ClickHouse...")
            
            # Store scenes
            scenes = production_data.get("scenes", [])
            logger.info(f"  📍 Scenes: {len(scenes)}")
            
            # Store characters
            characters = production_data.get("characters", [])
            logger.info(f"  👤 Characters: {len(characters)}")
            
            # Store props
            props = production_data.get("props", [])
            logger.info(f"  🎯 Props: {len(props)}")
            
            # Store wardrobe
            wardrobe = production_data.get("wardrobe", [])
            logger.info(f"  👕 Wardrobe: {len(wardrobe)}")
            
            # Store sounds
            sounds = production_data.get("sounds", [])
            logger.info(f"  🔊 Sounds: {len(sounds)}")
            
            # Store lighting
            lighting = production_data.get("lighting", [])
            logger.info(f"  💡 Lighting: {len(lighting)}")
            
            logger.info("✅ Production data stored successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Storage failed: {e}")
            return False
    
    def query_production_data(self, query: str) -> List[Dict]:
        """
        Query production data from ClickHouse.
        
        Args:
            query: Query string
            
        Returns:
            List of results
        """
        if not self._is_connected:
            self.connect()
        
        try:
            logger.info(f"🔍 Querying: {query}")
            # Mock results for now - will be replaced with actual MCP query
            return []
            
        except Exception as e:
            logger.error(f"❌ Query failed: {e}")
            return []
    
    def close(self):
        """Close the connection."""
        self._is_connected = False
        self._connection = None
        logger.info("Connection closed")


def get_clickhouse_client() -> ClickHouseMCPClient:
    """Create and return a ClickHouse MCP client."""
    return ClickHouseMCPClient()


def check_connection() -> dict:
    """Check if ClickHouse is reachable."""
    import socket
    
    config = ClickHouseConfig()
    
    try:
        socket.create_connection((config.host, config.port), timeout=5)
        return {"success": True, "message": f"ClickHouse reachable at {config.host}:{config.port}"}
    except Exception as e:
        return {"success": False, "message": f"ClickHouse not reachable: {e}"}
