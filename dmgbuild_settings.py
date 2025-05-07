"""
QR2Key - DMG build settings
"""

import os.path

format = 'UDBZ'

size = None

files = ['dist/QR2Key.app']

symlinks = {'Applications': '/Applications'}

background = 'resources/dmg_background.png'

window_rect = ((100, 100), (640, 480))
icon_size = 128
text_size = 16

icon_locations = {
    'QR2Key.app': (120, 180),
    'Applications': (500, 180)
}

background_color = (0.3, 0.3, 0.9)
