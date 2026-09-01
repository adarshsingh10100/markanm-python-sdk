from typing import Dict, Any, Optional

class Event:
    """
    MarkanM Platform Event Model
    """
    def __init__(self, data: Dict[str, Any]):
        self.raw_data = data or {}
        self.id = data.get("event_id") or data.get("id", "")
        self.type = data.get("event_type") or data.get("event", "")
        self.timestamp = data.get("timestamp") or data.get("created_at", "")

        # payload can be nested under "payload" key, or the event itself IS the payload
        self.payload = data.get("payload") if "payload" in data else data

        # Convenience: store bot reference for reply()
        self._bot = None

    def _attach_bot(self, bot):
        """Internal: attach bot instance so reply() works"""
        self._bot = bot

    @property
    def event_id(self) -> str:
        return self.id

    @property
    def event_type(self) -> str:
        return self.type

    @property
    def created_at(self) -> str:
        return str(self.timestamp)

    @property
    def room_id(self) -> Optional[str]:
        """Extract room_id from payload"""
        if isinstance(self.payload, dict):
            return (
                self.payload.get("room_id") or
                self.payload.get("conversation_id") or
                (self.payload.get("room") or {}).get("id")
            )
        return None

    async def reply(self, content: str):
        """
        Reply to the room this event came from.
        Works in @bot.on("command.received") handlers.
        """
        if not self._bot:
            raise RuntimeError("Bot not attached to event. Use @bot.on() decorator.")
        rid = self.room_id
        if not rid:
            raise ValueError("Cannot reply: missing room_id in event payload")
        return await self._bot.send_message(rid, content)

    def __repr__(self) -> str:
        return f"<MarkanM Event type='{self.type}' id='{self.id}' room_id='{self.room_id}'>"
