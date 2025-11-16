import redis
import json
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
from src.infrastructure.config.settings import settings


class InMemoryCache:
    """Fallback cache using Python dictionary"""
    def __init__(self):
        self._cache: Dict[str, tuple[Any, datetime]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            value, expiry = self._cache[key]
            if datetime.utcnow() < expiry:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, expiration: int = 300):
        expiry_time = datetime.utcnow() + timedelta(seconds=expiration)
        self._cache[key] = (value, expiry_time)
    
    def delete(self, key: str):
        if key in self._cache:
            del self._cache[key]


class CacheClient:
    """Redis cache client with in-memory fallback"""
    
    def __init__(self):
        self.use_redis = False
        self.memory_cache = InMemoryCache()
        
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=2
            )
            # Test connection
            self.redis_client.ping()
            self.use_redis = True
            print("✓ Redis cache connected successfully!")
        except Exception as e:
            print(f"⚠ Redis not available. Using in-memory cache. Error: {e}")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if self.use_redis:
            try:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            except Exception as e:
                print(f"Redis get error: {e}, falling back to memory cache")
        
        return self.memory_cache.get(key)
    
    def set(self, key: str, value: Any, expiration: int = 300) -> bool:
        """Set value in cache with expiration"""
        if self.use_redis:
            try:
                serialized = json.dumps(value)
                self.redis_client.setex(key, expiration, serialized)
                return True
            except Exception as e:
                print(f"Redis set error: {e}, using memory cache")
        
        self.memory_cache.set(key, value, expiration)
        return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if self.use_redis:
            try:
                self.redis_client.delete(key)
            except Exception:
                pass
        
        self.memory_cache.delete(key)
        return True
    
    def clear_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern"""
        if self.use_redis:
            try:
                keys = self.redis_client.keys(pattern)
                if keys:
                    return self.redis_client.delete(*keys)
            except Exception:
                pass
        return 0
    
    def ping(self) -> bool:
        """Check if Redis is available"""
        return self.use_redis


# Singleton instance
cache_client = CacheClient()