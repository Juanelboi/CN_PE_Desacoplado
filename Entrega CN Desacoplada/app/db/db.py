from abc import ABC, abstractmethod
from typing import List, Optional
from app.model.athlete import Athlete

class Database(ABC):
    
    @abstractmethod
    def initialize(self):
        pass
    
    @abstractmethod
    def create_athlete(self, athlete: Athlete) -> Athlete:
        pass
    
    @abstractmethod
    def get_athlete(self, athlete_number: int) -> Optional[Athlete]:
        pass
    
    @abstractmethod
    def get_all_athletes(self) -> List[Athlete]:
        pass
    
    @abstractmethod
    def update_athlete(self, athlete_number: int, athlete: Athlete) -> Optional[Athlete]:
        pass
    
    @abstractmethod
    def delete_athlete(self, athlete_number: int) -> bool:
        pass