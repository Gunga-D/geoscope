from dataclasses import dataclass

@dataclass
class Service:
    name: str
    has_supported_scrap: bool
    has_supported_dist: bool