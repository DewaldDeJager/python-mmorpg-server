from network.modules import Hits, AttackStyle
from network.shared_types import HitData


class Hit:
    def __init__(
        self,
        hit_type: Hits,
        damage: int = 0,
        ranged: bool = False,
        aoe: int = 0,
        magic: bool = False,
        archery: bool = False,
        attack_style: AttackStyle | None = None
    ):
        self.type = hit_type
        self.damage = damage
        self.ranged = ranged
        self.aoe = aoe
        self.magic = magic
        self.archery = archery
        self.attack_style = attack_style

    def get_damage(self) -> int:
        """
        @returns The damage integer of the hit.
        """
        return self.damage

    def is_aoe(self) -> bool:
        """
        @returns Whether the hit is an aoe.
        """
        return self.aoe > 0

    def get_skill(self) -> list[str]:
        """
        @returns Whether the hit is ranged.
        """
        if self.magic:
            return ["magic"]

        if self.archery:
            return ["archery"]

        if self.attack_style is not None and self.attack_style != AttackStyle.None_:
            match self.attack_style:
                case AttackStyle.Stab:
                    return ["accuracy"]

                case AttackStyle.Slash:
                    return ["strength"]

                case AttackStyle.Defensive:
                    return ["defense"]

                case AttackStyle.Crush:
                    return ["accuracy", "strength"]

                case AttackStyle.Shared:
                    return ["accuracy", "strength", "defense"]

                case AttackStyle.Hack:
                    return ["strength", "defense"]

                case AttackStyle.Chop:
                    return ["accuracy", "defense"]

        if self.type == Hits.Normal or self.type == Hits.Critical:
            return ["accuracy"]

        return []

    def serialize(self) -> HitData:
        """
        Serializes the Hit object and converts
        it into a JSON object.
        """
        return HitData(
            type=self.type,
            damage=self.damage,
            ranged=self.ranged,
            aoe=self.aoe,
            skills=self.get_skill()
        )
