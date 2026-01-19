import pytest
from datetime import datetime, timedelta
import time
from game.entity.character.effect.poison import Poison
from network.modules import PoisonTypes

def test_poison_initialization():
    start_time = datetime.now() - timedelta(seconds=10)
    poison = Poison(PoisonTypes.Venom, start=start_time)
    
    assert poison.name == "Venom"
    assert poison.damage == 5
    assert poison.duration == timedelta(seconds=30)
    assert poison.rate == timedelta(seconds=2)
    assert poison.start == start_time

def test_poison_expired():
    # Not expired
    poison = Poison(PoisonTypes.Venom)
    assert not poison.expired()
    
    # Expired
    start_time = datetime.now() - timedelta(seconds=31)
    poison = Poison(PoisonTypes.Venom, start=start_time)
    assert poison.expired()

def test_persistent_poison_never_expires():
    poison = Poison(PoisonTypes.Persistent)
    assert not poison.expired()
    
    start_time = datetime.now() - timedelta(days=100)
    poison = Poison(PoisonTypes.Persistent, start=start_time)
    assert not poison.expired()

def test_get_remaining_time():
    duration_seconds = 30
    start_time = datetime.now() - timedelta(seconds=10)
    poison = Poison(PoisonTypes.Venom, start=start_time)
    
    remaining = poison.get_remaining_time()
    # Should be around 20000ms
    assert 19000 <= remaining <= 21000
    
    # Persistent should return -1.0 or something indicating infinite
    poison_persistent = Poison(PoisonTypes.Persistent)
    assert poison_persistent.get_remaining_time() == -1.0

def test_get_remaining_time_expired():
    start_time = datetime.now() - timedelta(seconds=40)
    poison = Poison(PoisonTypes.Venom, start=start_time)
    
    assert poison.get_remaining_time() == 0.0
