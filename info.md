# ListenBrainz Integration

_Integration for [ListenBrainz][listenbrainz]._

{% if prerelease %}
### This is a pre-release version
It may contain bugs or break functionality in addition to adding new features and fixes. Please review open issues and submit new issues to the [issue tracker][issues].

{% endif %}

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

{% if not installed %}

## Installation

1. Click install.
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "ListenBrainz".

{% endif %}

## Configuration is done in the UI

There is nothing to configure in YAML.

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
