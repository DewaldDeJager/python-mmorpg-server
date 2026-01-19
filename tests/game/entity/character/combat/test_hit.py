from game.entity.character.combat.hit import Hit
from network.modules import Hits, AttackStyle


def test_hit_initialization():
    hit = Hit(Hits.Normal, damage=10)
    assert hit.type == Hits.Normal
    assert hit.get_damage() == 10
    assert not hit.is_aoe()
    assert hit.get_skill() == ["accuracy"]


def test_hit_aoe():
    hit = Hit(Hits.Normal, aoe=2)
    assert hit.is_aoe()


def test_hit_magic_skill():
    hit = Hit(Hits.Normal, magic=True)
    assert hit.get_skill() == ["magic"]


def test_hit_archery_skill():
    hit = Hit(Hits.Normal, archery=True)
    assert hit.get_skill() == ["archery"]


def test_hit_attack_style_skills():
    styles = {
        AttackStyle.Stab: ["accuracy"],
        AttackStyle.Slash: ["strength"],
        AttackStyle.Defensive: ["defense"],
        AttackStyle.Crush: ["accuracy", "strength"],
        AttackStyle.Shared: ["accuracy", "strength", "defense"],
        AttackStyle.Hack: ["strength", "defense"],
        AttackStyle.Chop: ["accuracy", "defense"],
    }
    for style, expected_skills in styles.items():
        hit = Hit(Hits.Normal, attack_style=style)
        assert hit.get_skill() == expected_skills


def test_hit_serialize():
    hit = Hit(Hits.Critical, damage=25, ranged=True, aoe=1)
    serialized = hit.serialize()
    assert serialized.type == Hits.Critical
    assert serialized.damage == 25
    assert serialized.ranged is True
    assert serialized.aoe == 1
    assert serialized.skills == ["accuracy"]
