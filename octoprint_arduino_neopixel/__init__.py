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

    def setArduino(self, color):
        if self.is_connected:
            try:
                try:
                    self.board.write("<" + str(color) + ">")
                except SerialException:
                    self.is_connected = False
                    self._logger.info("Could not connect to Arduino")
                    self.board.close()
            except Exception as e:
                self._logger.info("Error: " + str(e))

    ##~~ StartupPlugin
    def on_after_startup(self):
        Port = self._settings.get(["Port"])
        BaudRate = self._settings.get(["BaudRate"])
        try:
            self.board = Serial(Port, BaudRate, timeout=2)
            if self.board.isOpen():
                self.is_connected = True
                self._logger.info("Connected to Arduino")
            else:
                raise SerialException
        except SerialException:
            self.is_connected = False
            self._logger.info("Disconnecting from Arduino failed")
        except OSError:
            self.is_connected = False
            self._logger.info("Disconnecting from Arduino failed")

    ##~~ ShutdownPlugin
    def on_shutdown(self):
        if self.is_connected:
            self.setArduino("#000000")
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

    def on_settings_save(self, data):
        oldPort = self._settings.get(["Port"])
        oldBaudRate = self._settings.get(["BaudRate"])

        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)

        newPort = self._settings.get(["Port"])
        newBaudRate = self._settings.get(["BaudRate"])

        if (oldPort != newPort) or (oldBaudRate != newBaudRate):
            if self.is_connected:
                try:
                    self.board.close()
                    self._logger.info("Disconnected from Arduino")
                    self.is_connected = False
                except SerialException:
                    self.is_connected = False
                    self._logger.info("Disconnecting from Arduino failed")
                except OSError:
                    self.is_connected = False
                    self._logger.info("Disconnecting from Arduino failed")
            try:
                self.board = Serial(newPort, newBaudRate, timeout=2)
                if self.board.isOpen():
                    self.is_connected = True
                    self._logger.info("Connected to Arduino")
                else:
                    raise SerialException
            except SerialException:
                self.is_connected = False
                self._logger.info("Disconnecting from Arduino failed")
            except OSError:
                self.is_connected = False
                self._logger.info("Disconnecting from Arduino failed")

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False),
            dict(type="tab", custom_bindings=False),
        ]

    ##~~ EventHandlerPlugin
    def on_event(self, event, payload):
        command = self._settings.get([event])
        if command is not None:
            self.setArduino(command)

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
    def set_color(self, color):
        self.setArduino("#" + color)
        return("")

    ##~~ BlueprintPlugin
    @octoprint.plugin.BlueprintPlugin.route("/status/", methods=["GET"])
    def status(self):
        return(str(self.is_connected))

    ##~~ BlueprintPlugin
    @octoprint.plugin.BlueprintPlugin.route("/reconnect/", methods=["GET"])
    def reconnect(self):
        if self.is_connected == False:
            try:
                Port = self._settings.get(["Port"])
                BaudRate = self._settings.get(["BaudRate"])
                self.board = Serial(Port, BaudRate, timeout=2)
                if self.board.isOpen():
                    self.is_connected = True
                    self._logger.info("Connected to Arduino")
                    return("True")
                else:
                    raise SerialException
            except SerialException:
                self.is_connected = False
                self._logger.info("Disconnecting from Arduino failed")
                return("False")
            except OSError:
                self.is_connected = False
                self._logger.info("Disconnecting from Arduino failed")
                return("False")
        else:
            return("True")

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
