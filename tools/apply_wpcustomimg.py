#!/usr/bin/env python3
"""Last patch layer: while the video wallpaper is on, the still-picture layer behind it shows a fixed custom image
(app-assets/public/wallpaper-placeholder.jpg) instead of whichever picture is saved in config.wallpaper - no more painting/
landscape flash before the video's first frame arrives. The !important CSS rule overrides whatever setWallpaper() set inline,
and only applies while config.videoWallpaper is on - config.wallpaper itself is untouched, so turning video off restores your
own picture choice exactly as before."""
import os
ROOT = os.path.expanduser('~/Developer/webos-launcher-tvos')
SRC = os.path.join(ROOT, 'app/src')
def P(p): return os.path.join(SRC, p)
def edit(path, pairs):
    s = open(path).read()
    for a, b in pairs:
        assert a in s, (os.path.basename(path), a[:90])
        s = s.replace(a, b, 1)
    open(path, 'w').write(s)

edit(P('app.tsx'), [
 ("useEffect(() => setVideoWallpaper(config.videoWallpaper), [config.videoWallpaper]);",
  "useEffect(() => setVideoWallpaper(config.videoWallpaper), [config.videoWallpaper]);\n"
  "\tuseEffect(() => { document.documentElement.classList.toggle('wp-customimg', config.videoWallpaper); }, [config.videoWallpaper]);"),
])

css = open(P('theme/global.css')).read()
css += "\n/* ---------- custom placeholder image while the video wallpaper loads ---------- */\n"
css += "html.wp-customimg #wpimage { background-image: url(\"/wallpaper-placeholder.png\") !important; }\n"
open(P('theme/global.css'), 'w').write(css)
print('wallpaper custom placeholder image applied')
