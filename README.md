# ListenBrainz Integration

_Integration for [ListenBrainz][listenbrainz]._

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![Ko-Fi][kofibadge]][kofi]

[![Community Forum][forum-shield]][forum]

**This integration will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Various info about a user's listening history
`media_player` | User's _currently playing_

## Installation

Installation via [HACS][hacs] is recommended.

Manual:

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `listenbrainz`.
1. Download _all_ the files from the `custom_components/listenbrainz/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "ListenBrainz"

## Configuration is done in the UI

There is nothing to configure in YAML.

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[listenbrainz]: https://listenbrainz.org/
[hass-listenbrainz]: https://github.com/Weissnix4711/hass-listenbrainz
[issues]: https://github.com/Weissnix4711/hass-listenbrainz/issues
[kofi]: https://ko-fi.com/thomasaldrian
[kofibadge]: https://img.shields.io/badge/KO--FI-SUPPORT%20MY%20WORK-FF5E5B?style=for-the-badge&logo=kofi&color=13C3FF
[commits-shield]: https://img.shields.io/github/commit-activity/y/Weissnix4711/hass-listenbrainz.svg?style=for-the-badge
[commits]: https://github.com/Weissnix4711/hass-listenbrainz/commits/main
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/Weissnix4711/hass-listenbrainz.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Thomas%20Aldrian%20%40Weissnix4711-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/Weissnix4711/hass-listenbrainz.svg?style=for-the-badge
[releases]: https://github.com/Weissnix4711/hass-listenbrainz/releases
[hacs]: https://hacs.xyz/
