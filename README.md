# Integration Voltalis

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

_Integration to integrate with [Voltalis][voltalis]._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`climate` | Provides functionality to interact with climate devices.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `voltalis`.
1. Download _all_ the files from the `custom_components/voltalis/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Voltalis"

## Configuration is done in the UI

Provide your [Voltalis account][voltalis_account] credential

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[integration_voltalis]: https://github.com/jdelahayes/ha-voltalis
[buymecoffee]: https://www.buymeacoffee.com/jdelahayes
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/jdelahayes/ha-voltalis.svg?style=for-the-badge
[commits]: https://github.com/jdelahayes/ha-voltalis/commits/main
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/jdelahayes/ha-voltalis.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Johann%20Delahayes%20%40jdelahayes-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/jdelahayes/ha-voltalis.svg?style=for-the-badge
[releases]: https://github.com/jdelahayes/ha-voltalis/releases
[voltalis]: https://www.voltalis.com/
[voltalis_account]: https://myvoltalis.com/