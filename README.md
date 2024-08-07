# Magisk Modules Repo Util

This util is to build module repository for [MMRL](https://github.com/DerGoogler/MMRL)

- `sync` is a python package
- `cli.py` is a cli tool

## Getting Started

### Install dependencies

```shell
pip3 install -r util/requirements.txt
```

### New config.json

You can write it to `your-repo/json/config.json` by yourself, or

```shell
cli.py config --stdin << EOF
{
  "name": "Your Magisk Repo",
  "base_url": "https://you.github.io/magisk-modules-repo/",
  "max_num": 3,
  "enable_log": true,
  "log_dir": "log"
}
EOF
```

or

```shell
cli.py config --write name="Your Magisk Repo" base_url="https://you.github.io/magisk-modules-repo/" max_num=3 enable_log=true log_dir="log"
```

### New track.json

You can write it to `your-repo/modules/{id}/track.json` by yourself, or

```shell
cli.py track --stdin << EOF
{
  "id": "zygisk_lsposed",
  "update_to": "https://lsposed.github.io/LSPosed/release/zygisk.json",
  "license": "GPL-3.0"
}
EOF
```

or

```shell
cli.py track --add id="zygisk_lsposed" update_to="https://lsposed.github.io/LSPosed/release/zygisk.json" license="GPL-3.0"
```

If you want to generate `track.json`s from repositories on github

```shell
cli.py github --token <github-token> -u <user-name> -r <repo-name ...>
```

> [!TIP]
> Click [here](https://github.com/settings/personal-access-tokens/new) to create a new api token.

### Sync

```shell
cli.py sync
```

### Generate a sitemap

```shell
cli.py sitemap --base-url "https://mmrl.dergoogler.com/?module="
```

## How to update by GitHub Actions?

- You can refer to [GMR](https://github.com/Googlers-Repo/gmr).

## cli.py

```
cli.py --help
usage: cli.py [-h] [-v] [-V] command ...

Magisk Modules Repo Util

positional arguments:
  command
    config            Modify config of repository.
    track             Module tracks utility.
    github            Generate tracks from GitHub.
    sync              Sync modules in repository.
    index             Generate modules.json from local.
    check             Content check and migrate.
    sitemap           Sitemap generator.

options:
  -h, --help          Show this help message and exit.
  -v, --version       Show util version and exit.
  -V, --version-code  Show util version code and exit.
```

## config.json

```json
{
  "name": "Googlers Magisk Repo",
  "website": "https://mmrl.dergoogler.com",
  "support": "https://github.com/Googlers-Repo/repo/issues",
  "donate": "https://github.com/sponsors/DerGoogler",
  "submission": null,
  "base_url": "https://gr.dergoogler.com/repo/",
  "max_num": 3,
  "enable_log": true,
  "log_dir": "log"
}
```

| Key        | Attribute | Description                                     |
| ---------- | --------- | ----------------------------------------------- |
| name       | required  | Name of your module repository                  |
| base_url   | required  | Need to end with `/`                            |
| website    | optional  | Name of your website                            |
| donate     | optional  | Name of your donation url                       |
| submission | optional  | Link to your submission requests                |
| support    | optional  | Link to your support chat                       |
| max_num    | optional  | Max num of versions for modules, default is `3` |
| enable_log | optional  | default is `true`                               |
| log_dir    | optional  | default is `null`                               |

## track.json

```json
{
  "id": "str",
  "enable": "bool",
  "verified": "bool",
  "update_to": "str",
  "source": "str",
  "readme": "str",
  "max_num": "int",
  "antifeatures": ["array"]
}
```

| Key          | Attribute | Description                             |
| ------------ | --------- | --------------------------------------- |
| id           | required  | Id of Module (_in `module.prop`_)       |
| enable       | required  | Whether to enable                       |
| update_to    | required  | Follow examples below                   |
| changelog    | optional  | Markdown or Simple Text (**_no HTML_**) |
| antifeatures | optional  | Str[]                                   |
| verified     | optional  | Bool                                    |
| source       | optional  | Url                                     |
| max_num      | optional  | Overload `MAX_NUM` in config.json       |
| readme       | optional  | Str                                     |

## `common/repo.json`

> [!IMPORTANT]
> This file can be placed in the modules root directory. If a repo owner has added your module to his repo he can override those fields with the `track.json` file

```jsonc
{
  "support": "str",
  "donate": "str",
  "cover": "str",
  "icon": "str",
  "license": "str",
  "homepage": "str",
  "readme": "str",
  "screenshots": ["array"],
  "category": "str",
  "categories": ["array"],
  "require": ["array"],
  "note": {
    "title": "str" // optional
    "color": "red,blue,yellow,green", // optional
    "message": "str" // required
  }
}
```

| Key          | Attribute | Description |
| ------------ | --------- | ----------- |
| license      | optional  | SPDX ID     |
| cover        | optional  | Url         |
| icon         | optional  | Url         |
| readme       | optional  | Str         |
| screenshots  | optional  | Url[]       |
| antifeatures | optional  | Str[]       |
| category     | optional  | Str         |
| categories   | optional  | Str[]       |
| homepage     | optional  | Url         |
| support      | optional  | Url         |
| donate       | optional  | Url         |
| note         | optional  | Note        |

### Update from updateJson

> For those modules that provide [updateJson](https://topjohnwu.github.io/Magisk/guides.html#moduleprop).

```json
{
  "id": "zygisk_lsposed",
  "update_to": "https://lsposed.github.io/LSPosed/release/zygisk.json",
  "license": "GPL-3.0"
}
```

### Update from local updateJson

> _update_to_ requires a relative directory of _local_.

```json
{
  "id": "zygisk_lsposed",
  "update_to": "zygisk.json",
  "license": "GPL-3.0"
}
```

### Update from url

> For those have a same url to release new modules.

```json
{
  "id": "zygisk_lsposed",
  "update_to": "https://github.com/LSPosed/LSPosed/releases/download/v1.8.6/LSPosed-v1.8.6-6712-zygisk-release.zip",
  "license": "GPL-3.0",
  "changelog": "https://lsposed.github.io/LSPosed/release/changelog.md"
}
```

### Update from git

> For those we can get module by packaging all files in the repository, such as [Magisk-Modules-Repo](https://github.com/Magisk-Modules-Repo) and [Magisk-Modules-Alt-Repo](https://github.com/Magisk-Modules-Alt-Repo).

```json
{
  "id": "busybox-ndk",
  "update_to": "https://github.com/Magisk-Modules-Repo/busybox-ndk.git"
}
```

### Update from local zip

> _update_to_ and _changelog_ requires a relative directory of _local_.

```json
{
  "id": "zygisk_lsposed",
  "update_to": "LSPosed-v1.8.6-6712-zygisk-release.zip",
  "license": "GPL-3.0",
  "changelog": "changelog.md"
}
```

## For developer

```
your-repo
├── json
│   ├── config.json
│   └── modules.json
│
├── local
│   ├── ...
│   └── ...
│
├── log
│   ├── sync_2023-03-18.log
│   ├── ...
│   └── ...
│
├── modules
│   ├── zygisk_lsposed
│   │   ├── track.json
│   │   ├── update.json
│   │   ├── v1.8.6_6712.md
│   │   ├── v1.8.6_6712.zip
│   │   ├── ...
│   │   └── ...
│   │
│   ├── another_module
│   │   ├── ...
│   │   └── ...
│   └── .
│
└── util
```

### update.json

```json
{
  "id": "zygisk_lsposed",
  "timestamp": 1673882223.0,
  "versions": [
    {
      "timestamp": 1673882223.0,
      "version": "v1.8.6 (6712)",
      "versionCode": 6712,
      "zipUrl": "{base_url}modules/zygisk_lsposed/v1.8.6_(6712)_6712.zip",
      "changelog": "{base_url}modules/zygisk_lsposed/v1.8.6_(6712)_6712.md"
    }
  ]
}
```

### track.json

```json
{
  "id": "zygisk_lsposed",
  "update_to": "https://lsposed.github.io/LSPosed/release/zygisk.json",
  "license": "GPL-3.0",
  "homepage": "https://lsposed.org/",
  "source": "https://github.com/LSPosed/LSPosed.git",
  "support": "https://github.com/LSPosed/LSPosed/issues",
  "added": 1679025505.129431,
  "last_update": 1673882223.0,
  "versions": 1
}
```

## modules.json

### version 1

```json
{
  "name": "{name}",
  "metadata": {
    "version": 1,
    "timestamp": 1692439764.10608
  },
  "modules": [
    {
      "id": "zygisk_lsposed",
      "name": "Zygisk - LSPosed",
      "version": "v1.8.6 (6712)",
      "versionCode": 6712,
      "author": "LSPosed Developers",
      "description": "Another enhanced implementation of Xposed Framework. Supports Android 8.1 ~ 13. Requires Magisk 24.0+ and Zygisk enabled.",
      "track": {
        "type": "ONLINE_JSON",
        "added": 1679025505.129431,
        "license": "GPL-3.0",
        "homepage": "https://lsposed.org/",
        "source": "https://github.com/LSPosed/LSPosed.git",
        "support": "https://github.com/LSPosed/LSPosed/issues",
        "donate": ""
      },
      "versions": [
        {
          "timestamp": 1673882223.0,
          "version": "v1.8.6 (6712)",
          "versionCode": 6712,
          "zipUrl": "{base_url}modules/zygisk_lsposed/v1.8.6_(6712)_6712.zip",
          "changelog": "{base_url}modules/zygisk_lsposed/v1.8.6_(6712)_6712.md"
        }
      ]
    }
  ]
}
```

### version 0

```json
{
  "name": "{name}",
  "timestamp": 1692439602.46997,
  "modules": [
    {
      "id": "zygisk_lsposed",
      "name": "Zygisk - LSPosed",
      "version": "v1.8.6 (6712)",
      "versionCode": 6712,
      "author": "LSPosed Developers",
      "description": "Another enhanced implementation of Xposed Framework. Supports Android 8.1 ~ 13. Requires Magisk 24.0+ and Zygisk enabled.",
      "license": "GPL-3.0",
      "states": {
        "zipUrl": "{base_url}modules/zygisk_lsposed/v1.8.6_(6712)_6712.zip",
        "changelog": "{base_url}modules/zygisk_lsposed/v1.8.6_(6712)_6712.md"
      }
    }
  ]
}
```
