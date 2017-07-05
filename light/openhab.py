from homeassistant.components.light import (
    ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, Light)
import requests
import logging

REQUIREMENTS = ['requests>=2.12.4']
_LOGGER = logging.getLogger(__name__)

DEFAULT_BRIGHTNESS = "255"
DEFAULT_NAME = "Openhab Insteon Dimmer"


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup Openhab Insteon Dimmer platform."""
    
    devices = []
    resource = requests.get('{host}/rest/items?type=json'.format(
        host=config.get('host')))

    for item in resource.json()['item']:
        if item['type'] in ['DimmerItem', ]:
            devices.append(OpenhabLight(
                hass,
                item,
                config.get('brightness', DEFAULT_BRIGHTNESS)))

    add_devices(devices)


class OpenhabLight(Light):
    """Provide an Openhab light."""

    # pylint: disable=too-many-arguments
    def __init__(self, hass, item,  brightness):
        """Initialize the light."""
        self._state = None
        self._hass = hass
        self._name = item['name'] 
        self._resource = item['link'] 
        self._brightness = brightness

    @property
    def should_poll(self):
        """Polling for a light."""
        return True

    @property
    def name(self):
        """Return the name of the light if any."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        request = requests.get(self._resource+"/state", timeout=10)
        
        try:
            if int(float(request.text)) > 0:
                self._state = True
            else:
                self._state = False
        
        except:
            self._state = None
        
        return self._state

    def turn_on(self, **kwargs):
        """Turn the light on."""
        onValue = str((kwargs.get(ATTR_BRIGHTNESS, int(self._brightness))/255)*100)
        request = requests.post(self._resource,
                                data=onValue,
                                timeout=10)
        if (request.status_code == 200) or (request.status_code == 201):
            self._state = True
        else:
            _LOGGER.info("HTTP Status Code: %s", request.status_code)
            _LOGGER.error("Can't turn on %s. Is resource/endpoint offline?", self._resource)

        self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the light off."""
        request = requests.post(self._resource, data="0", timeout=10)
        if (request.status_code == 200) or (request.status_code == 201):
            self._state = False
        else:
            _LOGGER.error("Can't turn off %s. Is resource/endpoint offline?",
                          self._resource)

        self.schedule_update_ha_state()
    
    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS
