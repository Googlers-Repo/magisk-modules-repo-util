from .Config import Config
from .Index import Index
from .Pull import Pull
from ..model import TrackJson, UpdateJson, VersionItem
from ..track import LocalTracks
from ..utils import Log


class Migrate:
    def __init__(self, root_folder, config):
        self._log = Log("Migrate", config.log_dir, config.show_log)

        self._modules_folder = Config.get_modules_folder(root_folder)
        self._tracks = LocalTracks(self._modules_folder, config)
        self._config = config

    def _get_file_url(self, module_id, file):
        func = getattr(Pull, "_get_file_url")
        return func(self, module_id, file)

    def _check_folder(self, track, target_id):
        if track.id == target_id:
            return True

        msg = f"id is not same as in module.prop[{target_id}]"
        self._log.d(f"_check_ids: [{track.id}] -> {msg}")

        old_module_folder = self._modules_folder.joinpath(track.id)
        new_module_folder = self._modules_folder.joinpath(target_id)

        if new_module_folder.exists():
            msg = f"{target_id} already exists, remove the old directly"
            self._log.d(f"_check_ids: [{track.id}] -> {msg}")
            return True

        old_module_folder.rename(new_module_folder)
        track.update(id=target_id)

        return False

    def _check_update_json(self, track, update_json):
        module_folder = self._modules_folder.joinpath(track.id)
        new_update_json = UpdateJson(
            id=track.id,
            timestamp=update_json.timestamp,
            versions=list()
        )

        for item in update_json.versions:
            now_id, zipfile_name = item.zipUrl.split("/")[-2:]
            if now_id == track.id:
                continue

            zipfile = module_folder.joinpath(zipfile_name)
            if not zipfile.exists():
                msg = f"{zipfile_name} does not exist, it will be removed from {UpdateJson.filename()}"
                self._log.w(f"_check_update_json: [{track.id}] -> {msg}")
                continue

            new_zip_url = self._get_file_url(track.id, zipfile)

            changelog_name = item.changelog.split("/")[-1]
            changelog = module_folder.joinpath(changelog_name)
            new_changelog_url = ""
            if changelog.exists() and changelog.is_file():
                new_changelog_url = self._get_file_url(track.id, changelog)

            new_item = VersionItem(
                timestamp=item.timestamp,
                version=item.version,
                versionCode=item.versionCode,
                zipUrl=new_zip_url,
                changelog=new_changelog_url
            )

            new_update_json.versions.append(new_item)

        if len(new_update_json.versions) != 0:
            update_json.clear()
            update_json.update(new_update_json)
            return False

        return True

    def get_online_module(self, module_id, zip_file):
        func = getattr(Index, "get_online_module")
        return func(self, module_id, zip_file)

    def check_ids(self, module_ids=None):
        for track in self._tracks.get_tracks(module_ids):
            old_id = track.id
            module_folder = self._modules_folder.joinpath(track.id)
            latest_zip = sorted(
                module_folder.glob("*.zip"),
                key=lambda f: f.stat().st_mtime,
                reverse=True
            )[0]

            online_module = self.get_online_module(track.id, latest_zip)
            if online_module is None:
                continue

            if not self._check_folder(track, online_module.id):
                self._log.i(f"check_ids: [{old_id}] -> track has been migrated to {track.id}")
                module_folder = self._modules_folder.joinpath(track.id)
                track_json_file = module_folder.joinpath(TrackJson.filename())
                track.write(track_json_file)

            update_json_file = module_folder.joinpath(UpdateJson.filename())
            update_json = UpdateJson.load(update_json_file)
            if not self._check_update_json(track, update_json):
                self._log.i(f"check_ids: [{track.id}] -> {UpdateJson.filename()} has been updated")
                update_json.write(update_json_file)

    def clear_null_values(self, module_ids=None):
        for track in self._tracks.get_tracks(module_ids):
            module_folder = self._modules_folder.joinpath(track.id)
            track_json_file = module_folder.joinpath(TrackJson.filename())
            track.write(track_json_file)
