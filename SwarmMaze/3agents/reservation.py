class ReservationTable:
    """Class to manage time-based reservations for collision avoidance."""
    def __init__(self):
        self.reservations = {}

    def add_reservation(self, position, time, agent_id):
        """Add a reservation for a specific position and time."""
        self.reservations[(position, time)] = agent_id

    def is_reserved(self, position, time):
        """Check if a position is reserved at a specific time."""
        return (position, time) in self.reservations

    def get_reservation(self, position, time):
        """Get the agent ID that reserved a position at a specific time."""
        return self.reservations.get((position, time), None)

    def items(self):
        """Return all reservations as an iterable of ((position, time), agent_id)."""
        return self.reservations.items()

    def __iter__(self):
        """Allow iteration over reservations."""
        return iter(self.reservations)

    def __str__(self):
        """String representation of the reservation table for debugging."""
        return "\n".join(
            f"Time {time}: Position {pos} reserved by Agent {agent_id}"
            for (pos, time), agent_id in sorted(self.reservations.items())
        )
