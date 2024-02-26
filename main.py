#!/usr/bin/env python
import argostranslate.package
import argostranslate.translate
import pyperclip
import dbus
import time

from_code = "fr"
to_code = "en"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

# D-Bus setup
item = "org.freedesktop.Notifications"

notfy_intf = dbus.Interface(
    dbus.SessionBus().get_object(item, "/"+item.replace(".", "/")), item)

# Main loop
last_text = ""
while True:
    time.sleep(0.1)
    text = pyperclip.paste()
    if text == last_text:
        continue

    last_text = text

    translated_text = argostranslate.translate.translate(text, from_code, to_code)
    notfy_intf.Notify("", 0, "", f"{from_code} to {to_code}", translated_text, [], {"urgency": 1}, 3000)
