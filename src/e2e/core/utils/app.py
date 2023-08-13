import plistlib
import typing as t

from e2e._typing import Path, StrPath


class AppUtils:
    @staticmethod
    def get_app_id(app_path: StrPath) -> t.Optional[str]:
        app_path = Path(app_path)

        def read_from_app_bundle() -> str:
            with open(app_path / 'Info.plist', 'rb') as f:
                data = plistlib.load(f)
                return data.get('CFBundleIdentifier')

        if app_path.suffix == '.app':
            return read_from_app_bundle()
        # TODO: Handle .ipa, .apk
