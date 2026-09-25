"""
Event Subscriber Module

This module provides functionality to subscribe to and consume events from a Redis Pub/Sub channel.
It runs as a background task in the Audit Service, listening for todo-related events
and creating audit log entries for each event.
"""

import json
import asyncio
import redis.asyncio as aioredis
from services.audit_service.app.database import SessionLocal
from services.audit_service.app.service import AuditService

# Redis connection configuration
REDIS_URL = "redis://localhost:6379"
# Channel name to subscribe to for todo-related events
CHANNEL_NAME = "todo_events"


async def start_event_subscriber():
    """
    Start the continuous background event subscriber.
    
    This function creates a persistent connection to Redis Pub/Sub and
    listens for events published to the configured channel. When an event
    is received, it processes the event and creates an audit log entry.
    
    The subscriber runs indefinitely until cancelled (typically on application shutdown).
    Each consumed event is processed in its own database transaction for isolation.
    
    Event Processing Flow:
        1. Subscribe to the Redis Pub/Sub channel
        2. Listen for incoming messages
        3. Parse the JSON event payload
        4. Determine the event type
        5. Create an appropriate audit log entry
        6. Commit the transaction
    
    Supported Event Types:
        - TODO_CREATED: Logged when a new todo is created
        - TODO_DELETED: Logged when a todo is deleted
    
    Error Handling:
        - Database sessions are properly closed even if processing fails
        - Handles CancelledError for graceful shutdown
        - Each event is processed in isolation to prevent cascade failures
    
    Side Effects:
        - Creates audit log entries in the database
        - Prints processing status to stdout
    
    Raises:
        asyncio.CancelledError: When the task is cancelled during shutdown
    
    Note:
        This function is designed to run as a long-lived background task.
        In production, consider adding:
        - Exponential backoff for connection failures
        - Dead letter queue for failed event processing
        - Structured logging instead of print statements
        - Metrics/monitoring for event processing
    """
    # Create Redis client and Pub/Sub connection
    client = aioredis.from_url(REDIS_URL)
    pubsub = client.pubsub()
    await pubsub.subscribe(CHANNEL_NAME)

    print(f"[*] Audit Service worker subscribed to '{CHANNEL_NAME}'...")

    try:
        # Infinite loop listening for messages
        async for message in pubsub.listen():
            # Skip non-message events (e.g., subscription confirmations)
            if message["type"] != "message":
                continue

            # Decode and parse the event payload
            raw_data = message["data"].decode("utf-8")
            event_payload = json.loads(raw_data)
            event_type = event_payload.get("event_type")

            # Open a fresh isolated DB session per consumed event
            # This ensures each event is processed in its own transaction
            db = SessionLocal()
            audit_service = AuditService(db)

            try:
                # Handle TODO_CREATED event
                if event_type == "TODO_CREATED":
                    audit_service.record_event_log(
                        event_type=event_type,
                        resource_id=str(event_payload["todo_id"]),
                        message=f"New Todo created: '{event_payload['title']}'",
                    )
                    print(
                        f"[EVENT CONSUMED] Created Audit record for Todo ID {event_payload['todo_id']}"
                    )

                # Handle TODO_DELETED event
                elif event_type == "TODO_DELETED":
                    audit_service.record_event_log(
                        event_type=event_type,
                        resource_id=str(event_payload["todo_id"]),
                        message=f"Todo item deleted: ID {event_payload['todo_id']}",
                    )
                    print(
                        f"[EVENT CONSUMED] Created Audit record for deleted Todo ID {event_payload['todo_id']}"
                    )

            finally:
                # Always close the database session to prevent connection leaks
                db.close()

    except asyncio.CancelledError:
        # Graceful shutdown: unsubscribe and close connections
        await pubsub.unsubscribe(CHANNEL_NAME)
        await client.aclose()
