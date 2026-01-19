import pytest
import asyncio
import time
from game.entity.character.effect.status import Status
from network.modules import Effects
from database.models.player import SerializedDuration

@pytest.fixture
def status_system():
    return Status()

@pytest.mark.anyio
async def test_add_remove_effect(status_system):
    status_system.add(Effects.Stun)
    assert status_system.has(Effects.Stun)
    
    status_system.remove(Effects.Stun)
    assert not status_system.has(Effects.Stun)

@pytest.mark.anyio
async def test_add_with_timeout(status_system):
    callback_called = False
    def callback():
        nonlocal callback_called
        callback_called = True

    # 100ms timeout
    status_system.add_with_timeout(Effects.Stun, 100, callback)
    assert status_system.has(Effects.Stun)
    assert status_system.has_timeout(Effects.Stun)

    await asyncio.sleep(0.15)
    
    assert not status_system.has(Effects.Stun)
    assert callback_called

@pytest.mark.anyio
async def test_clear_effects(status_system):
    status_system.add(Effects.Stun)
    status_system.add_with_timeout(Effects.Freezing, 1000)
    
    status_system.clear()
    
    assert not status_system.has(Effects.Stun)
    assert not status_system.has(Effects.Freezing)
    assert not status_system.has_timeout(Effects.Freezing)

@pytest.mark.anyio
async def test_permanent_freezing(status_system):
    # Permanent freezing (no timeout)
    status_system.add(Effects.Freezing)
    assert status_system.has_permanent_freezing()
    
    # Try adding temporary freezing while permanent is active
    status_system.add_with_timeout(Effects.Freezing, 100)
    assert not status_system.has_timeout(Effects.Freezing)

@pytest.mark.anyio
async def test_serialize_load(status_system):
    # Use a longer duration for serialization to avoid race conditions
    status_system.add_with_timeout(Effects.Stun, 5000)
    
    serialized = status_system.serialize()
    assert int(Effects.Stun) in serialized
    assert serialized[int(Effects.Stun)].remaining_time > 3000

    new_status_system = Status()
    new_status_system.load(serialized)
    
    assert new_status_system.has(Effects.Stun)
    assert new_status_system.has_timeout(Effects.Stun)

@pytest.mark.anyio
async def test_callbacks(status_system):
    added = []
    removed = []
    
    status_system.on_add(lambda s: added.append(s))
    status_system.on_remove(lambda s: removed.append(s))
    
    status_system.add(Effects.Stun)
    assert Effects.Stun in added
    
    status_system.remove(Effects.Stun)
    assert Effects.Stun in removed
