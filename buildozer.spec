[app]

# (str) Title of your application
title = Attendance Tracker

# (str) App icon
icon.filename = %(source.dir)s/icon.png

# (str) Package name
package.name = attendancetracker

# (str) Package domain (needed for android packaging)
package.domain = org.attendance

# (str) Source files to include (let it include json files for local storage)
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Note: 'json' and 'datetime' are built-in Python modules, so only python3 and kivy are needed here.
requirements = python3,kivy

# (str) Supported orientations
orientation = all

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use (pinned to 25b for stable cloud build compatibility)
android.ndk = 25b

# (list) Supported architectures
android.archs = arm64-v8a, armeabi-v7a

# Automatically accept Android SDK licenses on cloud builders
android.accept_sdk_license = True

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = DANGER)
warn_on_root = 1
