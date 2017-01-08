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

    """ The openhab item"""
    _item = {}

    def __init__(self, item):
        self._item = item

    @property
    def name(self):
        """Return the name of the openhab item."""
        # Note Openhab doesn't return the friendly name
        return self._item['name']

    @property
    def is_on(self):
        """Return true if switch is on."""
        _LOGGER.debug("Reading cached item state: {}".format(self._item))
        return self._item['state'] == 'ON'

    def turn_on(self, **kwargs):
        self._send_command('ON')

    def turn_off(self, **kwargs):
        self._send_command('OFF')

    def _send_command(self, command):
        _LOGGER.debug("Sending command: {} to item: {}".format(
            command, self._item))
        try:
            requests.post(self._item['link'], command, timeout=10)
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Request to openhab failed")
            _LOGGER.exception(e)

    def update(self):
        try:
            self._item = requests.get(self._item['link'] + '?type=json',
                                      timeout=10).json()
            _LOGGER.info("Fetched item state from openhab {}".format(
                self._item))
            return self._item['state'] == 'ON'
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Request to openhab failed")
            _LOGGER.exception(e)

    @property
    def available(self):
        return True

    @property
    def should_poll(self):
        """Polling is needed."""
        return True
