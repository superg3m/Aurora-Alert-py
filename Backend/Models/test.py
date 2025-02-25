from Backend.Models._ModelBase import ModelBase


class GuildModel(ModelBase):
    def __init__(self):
        self.id: int = 1  # Assume ID is always required for updates
        self.name: str = "Test Guild"
        self.start_time: int = 14
        self.end_time: int = 21
        self.channel_name: str = "aurora-alert"
        self.kp_index_threshold: float = 4.67
        self.cloud_coverage_threshold: int = 35
        self.time_zone = "EST"  # Not used in DB
        self.moon_phase_blacklist: str = "Full Moon, Waxing Gibbous, Waning Gibbous"  # Not used in DB


guild = GuildModel()
guild.create()
