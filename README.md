# Tinycontrol integration for home-assistant

## Requirements

- Installed homeassistant (for details see <https://www.home-assistant.io/>).
- Access to config directory of homeassistant (to place custom integration files there)

## Installation

1. If you are using Home Assistant OS or Docker container then you need to find `config` directory (in case of docker it was selected in command running container). If you are using virtualenv installation it will be `.homeassistant` directory in home directory of user with whom you run the `hass` command, eg. `/home/homeassistant/.homeassistant`.
2. Create new directory `custom_components` inside directory mentioned in step 1.
3. Create new directory `tinycontrol` inside `custom_components`.
4. Copy project's files to directory `tinycontrol` (from step 3.).
5. In result you should have a following directory layout:

    ```
    .
    ├─ config/                          # or .homeassistant
    │  └─ ...                           # other homeassistant directories and files
    │  └─ custom_components/            # directory for storing custom integrations
    │     └─ tinycontrol/               # tinycontrol integration directory
    │        ├─ translations/
    │        │  ├─ en.json
    │        │  └─ en.json
    │        ├─ __init__.py
    │        ├─ __version__.py
    │        ├─ binary_sensor.py
    │        ├─ CHANGELOG.md            # List of changes in integration
    │        ├─ config_flow.py
    │        ├─ const.py
    │        ├─ coordinator.py
    │        ├─ entity.py
    │        ├─ manifest.json
    │        ├─ README.md               # This file with instructions
    │        ├─ sensor.py
    │        ├─ strings.json
    │        └─ switch.py
    └─ ...
    ```

6. Restart homeassistant server.
7. After restart the integration `tinycontrol` should be available in Configuration > Integrations > Add integration.

## Configuration

After adding device only few entities (status values like boardTemp, boardVoltage, etc.) will be active right away.

Other entities can be activated in Configuration > Devices > Entities, where you can select interesting ones and enable them.
