[app]

title = Attendance Tracker
icon.filename = %(source.dir)s/icon.png
package.name = attendancetracker
package.domain = org.attendance

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,csv

version = 1.0

requirements = python3,kivy

orientation = all

android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21

android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
