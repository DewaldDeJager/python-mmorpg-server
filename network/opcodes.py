from enum import IntEnum

class Login(IntEnum):
    Login = 0
    Register = 1
    Guest = 2

class List(IntEnum):
    Spawns = 0
    Positions = 1

class Equipment(IntEnum):
    Batch = 0
    Equip = 1
    Unequip = 2
    Style = 3

class Movement(IntEnum):
    Request = 0
    Started = 1
    Step = 2
    Stop = 3
    Move = 4
    Follow = 5
    Entity = 6
    Speed = 7

class Target(IntEnum):
    Talk = 0
    Attack = 1
    None_ = 2
    Object = 3

class Combat(IntEnum):
    Initiate = 0
    Hit = 1
    Finish = 2
    Sync = 3

class Projectile(IntEnum):
    Static = 0
    Dynamic = 1
    Create = 2
    Update = 3
    Impact = 4

class Network(IntEnum):
    Ping = 0
    Pong = 1
    Sync = 2

class Container(IntEnum):
    Batch = 0
    Add = 1
    Remove = 2
    Select = 3
    Swap = 4

class Ability(IntEnum):
    Batch = 0
    Add = 1
    Update = 2
    Use = 3
    QuickSlot = 4
    Toggle = 5

class Quest(IntEnum):
    Batch = 0
    Progress = 1
    Finish = 2
    Start = 3

class Achievement(IntEnum):
    Batch = 0
    Progress = 1

class Notification(IntEnum):
    Ok = 0
    YesNo = 1
    Text = 2
    Popup = 3

class Experience(IntEnum):
    Sync = 0
    Skill = 1

class NPC(IntEnum):
    Talk = 0
    Store = 1
    Bank = 2
    Enchant = 3
    Countdown = 4

class Trade(IntEnum):
    Request = 0
    Add = 1
    Remove = 2
    Accept = 3
    Close = 4
    Open = 5

class Enchant(IntEnum):
    Select = 0
    Confirm = 1

class Guild(IntEnum):
    Create = 0
    Login = 1
    Logout = 2
    Join = 3
    Leave = 4
    Rank = 5
    Update = 6
    Experience = 7
    Banner = 8
    List = 9
    Error = 10
    Chat = 11
    Promote = 12
    Demote = 13
    Kick = 14

class Pointer(IntEnum):
    Location = 0
    Entity = 1
    Relative = 2
    Remove = 3

class Store(IntEnum):
    Open = 0
    Close = 1
    Buy = 2
    Sell = 3
    Update = 4
    Select = 5

class Overlay(IntEnum):
    Set = 0
    Remove = 1
    Lamp = 2
    RemoveLamps = 3
    Darkness = 4

class Camera(IntEnum):
    LockX = 0
    LockY = 1
    FreeFlow = 2
    Player = 3

class Command(IntEnum):
    CtrlClick = 0

class Skill(IntEnum):
    Batch = 0
    Update = 1

class Minigame(IntEnum):
    TeamWar = 0
    Coursing = 1

class MinigameState(IntEnum):
    Lobby = 0
    End = 1
    Exit = 2

class MinigameActions(IntEnum):
    Score = 0
    End = 1
    Lobby = 2
    Exit = 3

class Bubble(IntEnum):
    Entity = 0
    Position = 1

class Effect(IntEnum):
    Add = 0
    Remove = 1

class Friends(IntEnum):
    List = 0
    Add = 1
    Remove = 2
    Status = 3
    Sync = 4

class Player(IntEnum):
    Login = 0
    Logout = 1

class Crafting(IntEnum):
    Open = 0
    Select = 1
    Craft = 2

class LootBag(IntEnum):
    Open = 0
    Take = 1
    Close = 2

class Pet(IntEnum):
    Pickup = 0

class Interface(IntEnum):
    Open = 0
    Close = 1
