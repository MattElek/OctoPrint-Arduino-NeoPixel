# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
from serial import Serial, SerialException

class Arduino_neopixelPlugin(octoprint.plugin.StartupPlugin,
                             octoprint.plugin.ShutdownPlugin,
                             octoprint.plugin.SettingsPlugin,
                             octoprint.plugin.TemplatePlugin,
                             octoprint.plugin.EventHandlerPlugin,
                             octoprint.plugin.BlueprintPlugin):

        def __init__(self):
            self.is_connected = False

	##~~ StartupPlugin
	def on_after_startup(self):
		port = self._settings.get(["Port"])
		baudrate = self._settings.get(["BaudRate"])
		try:
			self.board = Serial(port, baudrate, timeout=2)
			if self.board.isOpen():
				self._logger.info("Connected to Arduino")
				self.is_connected = True
			else:
				 raise SerialException
		except SerialException:
			self._logger.exception("Could not connect to Arduino")

	##~~ ShutdownPlugin
	def on_shutdown(self):
		if self.is_connected == True:
			self.board.write("<#000000>")
			self.board.close()
			self._logger.info("Disconnected from Arduino")

	##~~ SettingsPlugin
	def get_settings_defaults(self):
		return dict(
			Connected="#000000",
			Disconnected="#000000",
			PrintStarted="#FFFFFF",
			PrintFailed="#FF0000",
			PrintDone="#0000FF",
			PrintCancelled="#FFA500",
			PrintPaused="#FFFF00",
			PrintResumed="#FFFFFF",
			Home="#00FF00",
			Port="/dev/ttyACM1",
			BaudRate="9600",
		)

	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False),
			dict(type="tab", custom_bindings=False),
		]

	##~~ EventHandlerPlugin
	def on_event(self, event, payload):
		if self.is_connected == True:
                    command = self._settings.get([event])
		    if command is not None:
                        self.board.write("<" + command  + ">")

	##~~ Softwareupdate hook
	def get_update_information(self):
		return dict(
			arduino_neopixel=dict(
				displayName="Arduino_neopixel Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="mhar9000",
				repo="OctoPrint-Arduino-NeoPixel",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/mhar9000/OctoPrint-Arduino-NeoPixel/archive/{target_version}.zip"
			)
		)
	##~~ BlueprintPlugin
	@octoprint.plugin.BlueprintPlugin.route("/<color>/", methods=["GET"])
	def red(self, color):
		self.board.write("<#" + str(color) + ">")
		return("")

	def is_blueprint_protected(self):
		return False


##~~ Load Plugin
__plugin_name__ = "NeoPixel"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = Arduino_neopixelPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
