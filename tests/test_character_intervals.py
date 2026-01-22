import pytest
import asyncio
from unittest.mock import MagicMock
from game.entity.character.character import Character
from network.modules import Effects

class MockCharacter(Character):
    def serialize(self):
        return super().serialize()

@pytest.fixture
def mock_world():
    return MagicMock()

@pytest.mark.anyio
async def test_character_intervals_start_and_stop(mock_world):
    # Mock Constants to have very short intervals for testing
    from network.modules import Constants
    original_heal_rate = Constants.HEAL_RATE
    original_effect_rate = Constants.EFFECT_RATE
    Constants.HEAL_RATE = 10  # 10ms
    Constants.EFFECT_RATE = 10 # 10ms
    
    char = MockCharacter("0-instance_1", mock_world, "char_1", 10, 10)
    
    # Give it some time to run
    await asyncio.sleep(0.05)
    
    # We can't easily spy on methods that were already captured in create_task
    # unless we replace them before __init__ or use a different approach.
    # Since we already ran, let's just check that tasks are running.
    assert char.healing_task is not None
    assert not char.healing_task.done()
    assert char.effect_task is not None
    assert not char.effect_task.done()
    
    # Stop intervals
    char.stop()
    
    assert char.healing_task is None
    assert char.effect_task is None
    
    # Restore Constants
    Constants.HEAL_RATE = original_heal_rate
    Constants.EFFECT_RATE = original_effect_rate

@pytest.mark.anyio
async def test_character_poison_interval(mock_world):
    from network.modules import Constants, PoisonTypes
    char = MockCharacter("0-instance_1", mock_world, "char_1", 10, 10)
    
    # Set poison
    char.set_poison(PoisonTypes.Venom)
    
    assert char.poison_task is not None
    assert not char.poison_task.done()
    
    # Remove poison
    char.set_poison(None)
    assert char.poison_task is None
    
    char.stop()
