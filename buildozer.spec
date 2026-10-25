[app]

# (str) Title of your application
title = Attendance Tracker

# (str) Package name
package.name = attendancetracker

# (str) Package domain (needed for android packaging)
package.domain = org.attendance

# (list) Source files to include (let it find python files)
source.include_exts = py,png,jpg,kv,atlas,txt,csv

# (list) Application requirements
# Add hostpython3, kivy, and python/datetime/csv are built-in libraries
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# No special permissions needed unless exporting files to shared storage later
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (str) Supported API levels
android.api = 33
android.minapi = 21

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2
