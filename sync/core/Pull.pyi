from pathlib import Path
from typing import Optional, Tuple

from ..error import Result
from ..model import (
    TrackJson,
    ConfigJson,
    OnlineModule
)
from ..utils import Log


class Pull:
    _log: Log

    _local_folder: Path
    _modules_folder: Path
    _config: ConfigJson

    _max_size: float

    def __init__(self, root_folder: Path, config: ConfigJson): ...
    @staticmethod
    def _copy_file(old: Path, new: Path, delete_old: bool): ...
    @staticmethod
    @Result.catching()
    def _download(url: str, out: Path) -> Result: ...
    def _check_changelog(self, module_id: str, file: Path) -> bool: ...
    def _check_version_code(self, module_id: str, version_code: int) -> bool: ...
    def _get_file_url(self, module_id: str, file: Path) -> str: ...
    def _get_changelog_common(self, module_id: str, changelog: Optional[str]) -> Optional[Path]: ...
    def _from_zip_common(
        self,
        track: TrackJson,
        zip_file: Path,
        changelog_file: Optional[Path],
        *,
        delete_tmp: bool
    ) -> Optional[OnlineModule]: ...
    def from_json(self, track: TrackJson, *, local: bool) -> Tuple[Optional[OnlineModule], float]: ...
    def from_url(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
    def from_git(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
    def from_zip(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
    def from_track(self, track: TrackJson) -> Tuple[Optional[OnlineModule], float]: ...
    @classmethod
    def set_max_size(cls, value: float): ...
