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

    def test_get_empty_stats(self):
        """Test that get_empty_stats returns a Stats object with all zeros."""
        stats = Utils.get_empty_stats()
        assert stats.crush == 0
        assert stats.slash == 0
        assert stats.stab == 0
        assert stats.archery == 0
        assert stats.magic == 0

    def test_get_empty_bonuses(self):
        """Test that get_empty_bonuses returns a Bonuses object with all zeros."""
        bonuses = Utils.get_empty_bonuses()
        assert bonuses.accuracy == 0
        assert bonuses.strength == 0
        assert bonuses.archery == 0
        assert bonuses.magic == 0

    def test_random_weighted_int_bounds(self):
        """Test that random_weighted_int always returns a value within [min, max]."""
        min_val, max_val = 5, 15
        for weight in [0.1, 1.0, 2.0, 10.0]:
            for _ in range(100):
                result = Utils.random_weighted_int(min_val, max_val, weight)
                assert min_val <= result <= max_val

    def test_random_weighted_int_distribution(self):
        """Test that weight affects the distribution of random_weighted_int."""
        min_val, max_val = 0, 10
        samples = 10000
        
        # Low weight (e.g., 0.1) should bias towards max_val
        low_weight_results = [Utils.random_weighted_int(min_val, max_val, 0.1) for _ in range(samples)]
        low_weight_avg = sum(low_weight_results) / samples
        
        # High weight (e.g., 10.0) should bias towards min_val
        high_weight_results = [Utils.random_weighted_int(min_val, max_val, 10.0) for _ in range(samples)]
        high_weight_avg = sum(high_weight_results) / samples
        
        # With low weight (0.1), distribution is x^0.1, which is heavily skewed towards 1.0 (max)
        # With high weight (10.0), distribution is x^10, which is heavily skewed towards 0.0 (min)
        assert low_weight_avg > 7  # Should be high
        assert high_weight_avg < 3  # Should be low
