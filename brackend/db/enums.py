import enum


class MatchProgress(enum.Enum):
    not_started = enum.auto()
    in_progress = enum.auto()
    completed = enum.auto()


class UserRole(enum.Enum):
    player = enum.auto()
    spectator = enum.auto()
    organizer = enum.auto()