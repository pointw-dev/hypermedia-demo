from hypermea.core.settings_manager import SettingsManager

PREFIX = 'API'
SETTINGS = SettingsManager.instance()
SETTINGS.set_prefix_description(PREFIX, 'Settings for accounts-service')
SETTINGS.create(PREFIX, {
    # add settings here
})
