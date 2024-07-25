# https://pypi.org/project/qrcode/
# pip install qrcode

import qrcode
img = qrcode.make('https://wfi-dwp-metabase.richemont.com/')
type(img)  # qrcode.image.pil.PilImage
dir = r'C:\Aphonso_C'
img.save(dir+"\metabase_prd.png")