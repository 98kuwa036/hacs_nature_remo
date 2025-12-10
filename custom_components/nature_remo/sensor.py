"""Support for Nature Remo sensors."""
import logging
from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    LIGHT_LUX,
    PERCENTAGE,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Nature Remo sensor from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    sensors = []

    # Add device sensors (temperature, humidity, illuminance, motion)
    for device in coordinator.data.get("devices", []):
        device_id = device["id"]
        device_name = device["name"]

        # Temperature sensor
        if "newest_events" in device and "te" in device["newest_events"]:
            sensors.append(
                NatureRemoTemperatureSensor(coordinator, device_id, device_name)
            )

        # Humidity sensor
        if "newest_events" in device and "hu" in device["newest_events"]:
            sensors.append(
                NatureRemoHumiditySensor(coordinator, device_id, device_name)
            )

        # Illuminance sensor
        if "newest_events" in device and "il" in device["newest_events"]:
            sensors.append(
                NatureRemoIlluminanceSensor(coordinator, device_id, device_name)
            )

        # Motion sensor
        if "newest_events" in device and "mo" in device["newest_events"]:
            sensors.append(
                NatureRemoMotionSensor(coordinator, device_id, device_name)
            )

    # Add smart meter sensors
    for appliance in coordinator.data.get("appliances", []):
        if appliance.get("type") == "EL_SMART_METER":
            appliance_id = appliance["id"]
            appliance_name = appliance["nickname"]

            # Instantaneous power sensor
            if "smart_meter" in appliance:
                sensors.append(
                    NatureRemoPowerSensor(coordinator, appliance_id, appliance_name)
                )
                sensors.append(
                    NatureRemoEnergySensor(coordinator, appliance_id, appliance_name)
                )

    async_add_entities(sensors)


class NatureRemoSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for Nature Remo sensors."""

    def __init__(self, coordinator, device_id, device_name):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device_id = device_id
        self._device_name = device_name

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._device_name,
            "manufacturer": "Nature",
            "model": "Nature Remo",
        }


class NatureRemoTemperatureSensor(NatureRemoSensorBase):
    """Representation of a Nature Remo temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, device_id, device_name):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name)
        self._attr_name = f"{device_name} Temperature"
        self._attr_unique_id = f"{device_id}_temperature"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for device in self.coordinator.data.get("devices", []):
            if device["id"] == self._device_id:
                if "newest_events" in device and "te" in device["newest_events"]:
                    return device["newest_events"]["te"]["val"]
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes for dashboard display."""
        attributes = {}
        temp = self.native_value

        if temp is not None:
            # Comfort level assessment
            if temp < 18:
                attributes["comfort_level"] = "寒い"
                attributes["comfort_icon"] = "mdi:snowflake-alert"
                attributes["comfort_color"] = "#3498db"
            elif temp < 20:
                attributes["comfort_level"] = "少し寒い"
                attributes["comfort_icon"] = "mdi:snowflake"
                attributes["comfort_color"] = "#5dade2"
            elif temp < 24:
                attributes["comfort_level"] = "快適"
                attributes["comfort_icon"] = "mdi:emoticon-happy"
                attributes["comfort_color"] = "#2ecc71"
            elif temp < 26:
                attributes["comfort_level"] = "やや暑い"
                attributes["comfort_icon"] = "mdi:weather-sunny"
                attributes["comfort_color"] = "#f39c12"
            else:
                attributes["comfort_level"] = "暑い"
                attributes["comfort_icon"] = "mdi:fire"
                attributes["comfort_color"] = "#e74c3c"

            # Add timestamp
            for device in self.coordinator.data.get("devices", []):
                if device["id"] == self._device_id:
                    if "newest_events" in device and "te" in device["newest_events"]:
                        attributes["last_updated"] = device["newest_events"]["te"].get("created_at")
                        attributes["device_serial"] = device.get("serial_number", "Unknown")
                        attributes["firmware_version"] = device.get("firmware_version", "Unknown")

        return attributes


class NatureRemoHumiditySensor(NatureRemoSensorBase):
    """Representation of a Nature Remo humidity sensor."""

    _attr_device_class = SensorDeviceClass.HUMIDITY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = PERCENTAGE

    def __init__(self, coordinator, device_id, device_name):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name)
        self._attr_name = f"{device_name} Humidity"
        self._attr_unique_id = f"{device_id}_humidity"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for device in self.coordinator.data.get("devices", []):
            if device["id"] == self._device_id:
                if "newest_events" in device and "hu" in device["newest_events"]:
                    return device["newest_events"]["hu"]["val"]
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes for dashboard display."""
        attributes = {}
        humidity = self.native_value

        if humidity is not None:
            # Comfort level assessment
            if humidity < 30:
                attributes["comfort_level"] = "乾燥"
                attributes["comfort_icon"] = "mdi:water-alert"
                attributes["comfort_color"] = "#e67e22"
                attributes["recommendation"] = "加湿器の使用を推奨"
            elif humidity < 40:
                attributes["comfort_level"] = "やや乾燥"
                attributes["comfort_icon"] = "mdi:water-minus"
                attributes["comfort_color"] = "#f39c12"
                attributes["recommendation"] = "適度な加湿を推奨"
            elif humidity < 60:
                attributes["comfort_level"] = "快適"
                attributes["comfort_icon"] = "mdi:emoticon-happy"
                attributes["comfort_color"] = "#2ecc71"
                attributes["recommendation"] = "最適な湿度です"
            elif humidity < 70:
                attributes["comfort_level"] = "やや湿気"
                attributes["comfort_icon"] = "mdi:water-plus"
                attributes["comfort_color"] = "#3498db"
                attributes["recommendation"] = "除湿を検討"
            else:
                attributes["comfort_level"] = "多湿"
                attributes["comfort_icon"] = "mdi:water-alert-outline"
                attributes["comfort_color"] = "#9b59b6"
                attributes["recommendation"] = "除湿器の使用を推奨"

            # Add timestamp
            for device in self.coordinator.data.get("devices", []):
                if device["id"] == self._device_id:
                    if "newest_events" in device and "hu" in device["newest_events"]:
                        attributes["last_updated"] = device["newest_events"]["hu"].get("created_at")

        return attributes


class NatureRemoIlluminanceSensor(NatureRemoSensorBase):
    """Representation of a Nature Remo illuminance sensor."""

    _attr_device_class = SensorDeviceClass.ILLUMINANCE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = LIGHT_LUX

    def __init__(self, coordinator, device_id, device_name):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name)
        self._attr_name = f"{device_name} Illuminance"
        self._attr_unique_id = f"{device_id}_illuminance"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for device in self.coordinator.data.get("devices", []):
            if device["id"] == self._device_id:
                if "newest_events" in device and "il" in device["newest_events"]:
                    return device["newest_events"]["il"]["val"]
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes for dashboard display."""
        attributes = {}
        illuminance = self.native_value

        if illuminance is not None:
            # Brightness level assessment
            if illuminance < 10:
                attributes["brightness_level"] = "真っ暗"
                attributes["brightness_icon"] = "mdi:weather-night"
                attributes["brightness_color"] = "#34495e"
                attributes["recommendation"] = "照明を点灯"
            elif illuminance < 50:
                attributes["brightness_level"] = "暗い"
                attributes["brightness_icon"] = "mdi:brightness-4"
                attributes["brightness_color"] = "#7f8c8d"
                attributes["recommendation"] = "作業には照明が必要"
            elif illuminance < 200:
                attributes["brightness_level"] = "薄暗い"
                attributes["brightness_icon"] = "mdi:brightness-5"
                attributes["brightness_color"] = "#95a5a6"
                attributes["recommendation"] = "読書には不十分"
            elif illuminance < 500:
                attributes["brightness_level"] = "普通"
                attributes["brightness_icon"] = "mdi:brightness-6"
                attributes["brightness_color"] = "#f39c12"
                attributes["recommendation"] = "日常活動に適切"
            elif illuminance < 1000:
                attributes["brightness_level"] = "明るい"
                attributes["brightness_icon"] = "mdi:white-balance-sunny"
                attributes["brightness_color"] = "#f1c40f"
                attributes["recommendation"] = "十分な明るさ"
            else:
                attributes["brightness_level"] = "非常に明るい"
                attributes["brightness_icon"] = "mdi:weather-sunny"
                attributes["brightness_color"] = "#e67e22"
                attributes["recommendation"] = "直射日光レベル"

            # Add timestamp
            for device in self.coordinator.data.get("devices", []):
                if device["id"] == self._device_id:
                    if "newest_events" in device and "il" in device["newest_events"]:
                        attributes["last_updated"] = device["newest_events"]["il"].get("created_at")

        return attributes


class NatureRemoMotionSensor(NatureRemoSensorBase):
    """Representation of a Nature Remo motion sensor."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(self, coordinator, device_id, device_name):
        """Initialize the sensor."""
        super().__init__(coordinator, device_id, device_name)
        self._attr_name = f"{device_name} Motion"
        self._attr_unique_id = f"{device_id}_motion"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for device in self.coordinator.data.get("devices", []):
            if device["id"] == self._device_id:
                if "newest_events" in device and "mo" in device["newest_events"]:
                    return device["newest_events"]["mo"]["created_at"]
        return None


class NatureRemoPowerSensor(NatureRemoSensorBase):
    """Representation of a Nature Remo smart meter power sensor."""

    _attr_device_class = SensorDeviceClass.POWER
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfPower.WATT

    def __init__(self, coordinator, appliance_id, appliance_name):
        """Initialize the sensor."""
        super().__init__(coordinator, appliance_id, appliance_name)
        self._attr_name = f"{appliance_name} Power"
        self._attr_unique_id = f"{appliance_id}_power"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for appliance in self.coordinator.data.get("appliances", []):
            if appliance["id"] == self._device_id:
                if "smart_meter" in appliance:
                    smart_meter = appliance["smart_meter"]
                    if "echonetlite_properties" in smart_meter:
                        for prop in smart_meter["echonetlite_properties"]:
                            if prop["epc"] == 231:  # Instantaneous power
                                return prop.get("val")
        return None

    @property
    def extra_state_attributes(self):
        """Return additional attributes for dashboard display."""
        attributes = {}
        power = self.native_value

        if power is not None:
            # Usage level assessment
            if power < 500:
                attributes["usage_level"] = "低"
                attributes["usage_icon"] = "mdi:battery-charging-low"
                attributes["usage_color"] = "#2ecc71"
                attributes["status"] = "省エネ運転中"
            elif power < 1500:
                attributes["usage_level"] = "通常"
                attributes["usage_icon"] = "mdi:battery-charging-medium"
                attributes["usage_color"] = "#f39c12"
                attributes["status"] = "標準的な使用量"
            elif power < 3000:
                attributes["usage_level"] = "高"
                attributes["usage_icon"] = "mdi:battery-charging-high"
                attributes["usage_color"] = "#e67e22"
                attributes["status"] = "多くの電力を使用中"
            else:
                attributes["usage_level"] = "非常に高"
                attributes["usage_icon"] = "mdi:battery-alert"
                attributes["usage_color"] = "#e74c3c"
                attributes["status"] = "高負荷使用中"

            # Estimated daily cost (assuming 27 yen/kWh - adjust as needed)
            daily_kwh = (power / 1000) * 24
            attributes["estimated_daily_cost"] = round(daily_kwh * 27, 2)
            attributes["estimated_daily_kwh"] = round(daily_kwh, 2)

        return attributes


class NatureRemoEnergySensor(NatureRemoSensorBase):
    """Representation of a Nature Remo smart meter energy sensor."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR

    def __init__(self, coordinator, appliance_id, appliance_name):
        """Initialize the sensor."""
        super().__init__(coordinator, appliance_id, appliance_name)
        self._attr_name = f"{appliance_name} Energy"
        self._attr_unique_id = f"{appliance_id}_energy"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        for appliance in self.coordinator.data.get("appliances", []):
            if appliance["id"] == self._device_id:
                if "smart_meter" in appliance:
                    smart_meter = appliance["smart_meter"]
                    if "echonetlite_properties" in smart_meter:
                        for prop in smart_meter["echonetlite_properties"]:
                            if prop["epc"] == 224:  # Cumulative energy
                                val = prop.get("val")
                                coefficient = smart_meter.get("coefficient", 1)
                                if val is not None:
                                    return val * coefficient
        return None
