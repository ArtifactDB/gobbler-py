# Changelog

## Version 0.1.3

- Enable setting/getting of asset-level permissions in `set_permissions()` and `fetch_permissions()`.
- Added the `force=` option to forcibly remove directories in `remove_asset()`, `remove_version()` and `reject_probation()`.
- Bugfix for handling relative links in `upload_directory()`.

## Version 0.1.2

- Added the `reindex_version()` function.

## Version 0.1.1

- Added `fetch_file()` utility to fetch individual files from the registry.
- Added the `global_write=` option to `set_permissions()` to enable global writes.
- Preserve relative links in the upload directory in `upload_directory()`. 
- Added an `unpack_path()` utility to return project/asset/version information from a path to a Gobbler resource.

## Version 0.1.0

- New release of the Gobbler.
