# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.13.0] - 2025-11-17

### Added

- Experimental action `add_mqtt_device` for adding device (currently only LK4) as device in MQTT integration.

## [0.12.1] - 2025-03-28

### Added

- Readings PM for LK4.

## [0.12.0] - 2025-01-30

### Added

- Support devices using HTTPS (port 443 only, no port forwarding).
- Ability to edit authentication data and the entire device configuration from the Home Assistant interface. In the event of authentication problems, an appropriate alert will appear in the Devices & Services section, allowing you to change the authentication data. Reconfiguration of the device is available within the menu of the given device (next to actions: reload, rename, disable, delete).

### Fixed

- Deprecations warnings from homeassistant - by using replacements of deprecated features.

## [0.11.2] - 2024-06-11

### Changed

- Upgrade requirements.

## [0.11.1] - 2024-03-26

### Changed

- Title of config entry from *MAC* to combination of `{MODEL} ({MAC}, {HOST}:{PORT})` so it's easier to differentiate devices.

## [0.11.0] - 2024-03-20

This version uses new domain `tinycontrol` instead of `lk3`, so it should be treated as a new integration.

### Added

- Support for more tinycontrol devices. It supports LK 2.0, LK 2.5, LK 3.0, LK 3.5, LK 4.0, tcPDU, IP Power Strip (based on LK 2.X and LK 3.5).

### Changed

- Domain of integration changed to `tinycontrol` to better reflect its functionality (supports various devices not just one).
- Config flow is now fully asyncio.
- API library is replaced and now pulled from PyPI.
- Better handling of entities - if device does not provide data for them they simply won't be initialized. It should seamlessly add new entities after software upgrade (integration reload required).

### Fixed

- Deprecations warnings from homeassistant - by using replacements of deprecated features.

## [0.9.1] - 2022-12-14

### Changed

- Internal configuration of sensor entities to allow selecting unit of measurement.

## [0.8.3] - 2022-10-13

### Fixed

- On/off action for outputs and PWM. It properly set output on or off instead of always toggling it (change mostly affects HA scripts).

## [0.8.2] - 2022-10-13

### Fixed

- Showing state of *EVENT* variables for **HW 3.5+ SW 1.22b - 1.49d** (for newer it still works fine). The values are not available in earlier firmwares and also in **HW 3.0**.

## [0.8.1] - 2022-03-25

### Fixed

- Bug with handling **SW 1.49**, that was introduced in 0.8.0.

## [0.8.0] - 2022-03-25

### Added

- Support for **HW 3.5+ SW 1.50** (modified *m1-m30* readings).
- Support for reading and controlling *Event* variables.

## [0.7.1] - 2022-01-27

### Added

- Support for **HW 3.5+ SW 1.49** (additional *POWER*, *ENERGY*, *DIFF* readings, different *INPD* parsing).

### Fixed

- Displaying values of *DIFF* which has another *DIFF* as input.

## [0.6.2] - 2021-06-30

### Fixed

- Add version property inside `manifest.json` so custom integration can be loaded by **Home Assistant 2021.6+**.

## [0.6.1] - 2021-02-15

### Fixed

- Fix parsing modbus readings for SW 1.35+.

## [0.6.0] - 2021-02-03

### Added

- Support for SW 1.34.
- Support for handling LK3 using non standard http port (selectable in config flow).

### Changed

- Rename sdm1-29 to m1-29 and add m30 (variables for modbus readings).
- Use negation flag for outputs and digital inputs on LK to show states in the same manner (only SW 1.34+).

### Fixed

- Fix divisor for pressure reading.

## [0.5.2] - 2021-01-04

### Changed

- Improve installation instructions in `README.md`.

## [0.5.1] - 2021-01-04

### Fixed

- Fix configuring device with Basic Authentication enabled.

## [0.5.0] - 2020-11-19

### Added

- Parse sdm with divisors depending on HW, SW and modbus sensor.

## [0.4.1] - 2020-08-24

### Changed

- Use name for entity's name instead of host.

## [0.4.0] - 2020-08-24

### Added

- Add name to configuration form.

### Fixed

- Moved translations to directory without `.`.
- Fix displaying error messages during configuration.

## [0.3.0] - 2020-03-02

### Added

- Update interval value to config_flow.

### Fixed

- Fix adding multiple devices (invalid mac query).

## [0.2.0] - 2020-02-13

### Added

- Reading states of digital inputs (inpd).
- Reading and controlling pwm outputs.

### Changed

- Use `/json/all.json` instead of multi file query (requires web version 1.16.x+ on LK3).

    Query times [s] | old version | new version | New/Old Avg [%] | Increase [times]
    ---|---|---|---|---
    LK3.0 | 0.389 (0.361, 0.611) | 0.094 (0.071, 0.272) | 24.2 | 4.13
    LK3.5 | 0.260 (0.249, 0.327) | 0.022 (0.017, 0.065) | 8.5 | 11.82

## [0.1.0] - 2020-01-17

- Basic homeassistant integration for LK3.
