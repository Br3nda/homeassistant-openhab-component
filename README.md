# Homeassistant component to control Openhab
Enable while you port your config over to homeassistant

## Installation

```
git clone https://github.com/Br3nda/homeassistant-openhab-component
cp sensor/openhab.py .homeassistant/custom_components/sensor/
cp switch/openhab.py .homeassistant/custom_components/switch/
```

## Example configuration:

Control openhab switches (on/off) from homeassistant
```
switch openhab:
  platform: openhab
  host: http://127.0.0.1:8080
```


Read everything else
```
sensor openhab:
  platform: openhab
  host: http://127.0.0.1:8080
```
