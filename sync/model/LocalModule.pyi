from pathlib import Path
from typing import Dict, Type

from .AttrDict import AttrDict
from .TrackJson import TrackJson

from ..core.Config import Config

class LocalModule(AttrDict):
    id: str
    name: str
    version: str
    versionCode: int
    author: str
    description: str
    
    added: float
    timestamp: float
    size: float
    
    # FoxMMM supported props
    maxApi: int
    minApi: int
    
    # MMRL supported props
    category: str
    categories: list[str]
    icon: str
    homepage: str
    donate: str
    support: str
    cover: str
    screenshots: list[str]
    license: str
    screenshots: list[str]
    readme: str
    require: list[str]
    verified: bool

    @classmethod
    def load(cls, file: Path, track: TrackJson, config: Config) -> LocalModule: ...
    @classmethod
    def expected_fields(cls, __type: bool = ...) -> Dict[str, Type]: ...
