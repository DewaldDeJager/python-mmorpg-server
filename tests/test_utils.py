import pytest
from common.utils import Utils
from network.modules import EntityType

class TestUtils:
    def test_create_instance_format(self):
        """Test that create_instance returns a string in the correct format."""
        instance_id = Utils.create_instance(EntityType.Player)
        # Format: {type_val}-{random_int}{counter}
        # EntityType.Player value is 0
        assert instance_id.startswith("0-")
        
        parts = instance_id.split("-")
        assert len(parts) == 2
        assert parts[0] == str(EntityType.Player.value)
        assert parts[1].isdigit()

    def test_create_instance_uniqueness(self):
        """Test that create_instance generates unique IDs due to the counter."""
        ids = set()
        num_instances = 100
        for _ in range(num_instances):
            instance_id = Utils.create_instance(EntityType.Mob)
            assert instance_id not in ids
            ids.add(instance_id)
        
        assert len(ids) == num_instances

    def test_create_instance_different_types(self):
        """Test create_instance with different EntityTypes."""
        player_id = Utils.create_instance(EntityType.Player)
        mob_id = Utils.create_instance(EntityType.Mob)
        item_id = Utils.create_instance(EntityType.Item)
        
        assert player_id.startswith(f"{EntityType.Player.value}-")
        assert mob_id.startswith(f"{EntityType.Mob.value}-")
        assert item_id.startswith(f"{EntityType.Item.value}-")
