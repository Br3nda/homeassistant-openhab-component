from homeassistant.const import TEMP_CELSIUS
from homeassistant.components.switch import SwitchDevice
import requests
import logging

REQUIREMENTS = ['requests>=2.12.4']
_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the openhab switch platform."""
    devices = []
    response = requests.get('{host}/rest/items?type=json'.format(
        host=config.get('host')))
    # Add all SwitchItem entries to homeassistant
    for item in response.json()['item']:
        if item['type'] in ['SwitchItem', ]:
            devices.append(OpenhabSwitch(item))
    add_devices(devices)


class OpenhabSwitch(SwitchDevice):
    # hidden = True

    def __init__(self, item):
        self._item = item

    @property
    def name(self):
        """Return the name of the openhab item."""
        return self._item['name']

    @property
    def is_on(self):
        _LOGGER.info("Reading cached item state: {}".format(self._item))
        """Return true if switch is on."""
        return self._item['state'] == 'ON'

    def turn_on(self, **kwargs):
        _LOGGER.info("Turning on item: {}".format(self._item))
        requests.post(self._item['link'], 'ON')

    def turn_off(self, **kwargs):
        _LOGGER.info("Turning off item: {}".format(self._item))
        requests.post(self._item['link'], 'OFF')

    def update(self):
        self._item = requests.get(self._item['link'] + '?type=json').json()
        _LOGGER.info("Fetched item state {}".format(self._item))
        return self._item['state'] == 'ON'

    @property
    def available(self):
        return True

    @property
    def should_poll(self):
        """Polling is needed."""
        return True
