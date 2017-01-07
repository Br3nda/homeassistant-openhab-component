from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.entity import Entity
import requests

REQUIREMENTS = ['requests>=2.12.4']


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    devices = []
    response = requests.get('{host}/rest/items?type=json'.format(
        host=config.get('host')))
    for item in response.json()['item']:
        if item['type'] in ['NumberItem', 'StringItem']:
            devices.append(OpenhabSensor(item))
    add_devices(devices)


class OpenhabSensor(Entity):
    def __init__(self, item):
        self._item = item

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._item['name']

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.data['state']

    def update(self):
        self._item = requests.get(self._item['link'] + '?type=json').json()
        return self._item['state']

    # @property
    # def unit_of_measurement(self):
    #     """Return the unit of measurement."""
    #     return TEMP_CELSIUS

    @property
    def should_poll(self):
        """Polling is needed."""
        return True
