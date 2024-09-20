from enum import Enum

from .AttrDict import AttrDict
from .JsonIO import JsonIO

from .ModuleNote import ModuleNote

class TrackJson(AttrDict, JsonIO):
    id: str
    enable: bool
    verified: bool
    update_to: str
    changelog: str
    license: str
    homepage: str
    source: str
    support: str
    donate: str
    max_num: int
    # author: str
    # contributors: list[str]
    cover: str
    icon:str
    screenshots: list[str]
    require: list[str]
    category: str
    categories: list[str]
    readme: str
    require: list[str]
    antifeatures: list[str]
    note: ModuleNote

    # noinspection PyAttributeOutsideInit
    @property
    def type(self):
        if self._type is not None:
            return self._type

        if self.update_to.startswith("http"):
            if self.update_to.endswith(".json"):
                self._type = TrackType.ONLINE_JSON
            elif self.update_to.endswith(".zip"):
                self._type = TrackType.ONLINE_ZIP
            elif self.update_to.endswith(".git"):
                self._type = TrackType.GIT

        elif self.update_to.startswith("git@"):
            if self.update_to.endswith(".git"):
                self._type = TrackType.GIT

        else:
            if self.update_to.endswith(".json"):
                self._type = TrackType.LOCAL_JSON
            elif self.update_to.endswith(".zip"):
                self._type = TrackType.LOCAL_ZIP

        if self._type is None:
            self._type = TrackType.UNKNOWN

        return self._type

    def json(self):
        return AttrDict(
            type=self.type.name,
            added=self.added,
            source=self.source or None
        )

    def write(self, file):
        new = AttrDict()
        keys = list(self.expected_fields().keys())

        # fields without manually
        keys.extend(["added", "last_update", "versions"])

        for key in keys:
            value = self.get(key, "")
            if value is None:
                continue

            if isinstance(value, str):
                if value == "" or value.isspace():
                    continue

            new[key] = value

        JsonIO.write(new, file)

    @classmethod
    def load(cls, file):
        obj = JsonIO.load(file)
        return TrackJson(obj)

    @classmethod
    def filename(cls):
        return "track.json"

    @classmethod
    def expected_fields(cls, __type=True):
        if __type:
            return cls.__annotations__

        return {k: v.__name__ for k, v in cls.__annotations__.items() if v is not None and v is not False}


class TrackType(Enum):
    UNKNOWN = 0
    ONLINE_JSON = 1
    ONLINE_ZIP = 2
    GIT = 3
    LOCAL_JSON = 4
    LOCAL_ZIP = 5
