from typing import Literal
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

# Used for multiple database support
DatabaseTypes = Literal["mongo", "mongodb"]


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # === Connectivity/Hosting ===
    name: str = "Kaetram"
    host: str = "localhost"
    port: int = 9001
    ssl: bool = False

    server_id: int = 1
    access_token: str = ""
    api_enabled: bool = False
    api_port: int = 9002

    hub_enabled: bool = False
    hub_host: str = ""
    hub_ws_host: str = ""
    hub_port: int = 9526
    hub_ws_port: int = 9527
    hub_access_token: str = ""
    admin_host: str = ""
    admin_port: int = 9528
    remote_server_host: str = ""
    remote_api_host: str = ""

    # === Database ===
    database: DatabaseTypes = "mongodb"
    skip_database: bool = True

    mongodb_host: str = "mongodb"
    mongodb_port: int = 27017
    mongodb_user: str = ""
    mongodb_password: str = ""
    mongodb_database: str = "game"
    mongodb_srv: bool = False
    mongodb_tls: bool = False
    mongodb_auth_source: str = ""
    aggregate_threshold: int = 60000

    # === World Configurations ===
    tutorial_enabled: bool = True
    override_auth: bool = Field(False, validation_alias=AliasChoices("OVERWRITE_AUTH", "OVERRIDE_AUTH"))
    disable_register: bool = False
    max_players: int = 200
    update_time: int = 300
    gver: str = "0.0.1-alpha"
    minor: str = ""
    region_cache: bool = True
    save_interval: int = 60000
    message_limit: int = 300

    # === Discord ===
    discord_enabled: bool = False
    discord_channel_id: str = ""
    discord_bot_token: str = ""

    # === LICENSING ===
    accept_license: bool = True

    # === Debugging ===
    debugging: bool = False
    debug_level: str = "all"
    fs_debugging: bool = False

    def __init__(self, **values):
        super().__init__(**values)
        # Defaults to `HOST` if empty
        if not self.hub_host:
            self.hub_host = self.host
        if not self.hub_ws_host:
            self.hub_ws_host = self.hub_host
        if not self.admin_host:
            self.admin_host = self.hub_host
        if not self.remote_server_host:
            self.remote_server_host = self.host


config = Config()
