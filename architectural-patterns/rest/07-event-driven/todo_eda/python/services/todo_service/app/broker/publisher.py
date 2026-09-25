"""
Event Publisher Module

This module provides functionality to publish events to a Redis Pub/Sub channel.
It's used by the Todo Service to notify other services of todo-related events
in an asynchronous, decoupled manner.
"""

from shared.events import BaseEvent
import redis.asyncio as aioredis

# Redis connection configuration
REDIS_URL = "redis://localhost:6379"
# Channel name for todo-related events
CHANNEL_NAME = "todo_events"


class EventPublisher:
    """
    Static class for publishing events to Redis Pub/Sub.
    
    Provides methods to publish domain events to a Redis channel,
    enabling asynchronous communication between services.
    """
    
    @staticmethod
    async def publish(event: BaseEvent) -> None:
        """
        Publish an event to the Redis Pub/Sub channel.
        
        Serializes the event to JSON and publishes it to the configured
        Redis channel. Creates a new Redis connection for each publish
        operation and closes it afterward.
        
        Args:
            event: BaseEvent instance (or subclass) to publish
        
        Side Effects:
            - Publishes the event to the Redis channel
            - Logs errors to stdout if publishing fails
        
        Error Handling:
            Catches all exceptions during publishing to prevent service
            disruption. In production, this should use proper logging
            and potentially implement retry logic or dead-letter queues.
        
        Note:
            This implementation creates a new connection per publish.
            For high-throughput scenarios, consider using a connection pool.
        """
        try:
            # Create async Redis client
            client = await aioredis.from_url(REDIS_URL)
            # Publish event as JSON to the channel
            await client.publish(CHANNEL_NAME, event.model_dump_json())
            # Close the connection
            await client.aclose()
        except Exception as e:
            # Log the error or handle it as needed
            # In production, consider using proper logging and retry mechanisms
            print(f"Failed to publish event: {e}")
