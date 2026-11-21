# brand/ — assets shared by every video in this project

Put anything more than one video needs here, once. `hf new <product>/<video>` copies the
contents of this folder into the new video as `assets/brand/...`, so the composition always
loads it with a relative path (`assets/brand/logo.svg`) — required by the renderer.

```
brand/
  logo.svg
  fonts/<Family>.ttf        # non-bundled font: declare @font-face to assets/brand/fonts/...
  screens/                  # real product screenshots — show the product, don't draw it
  music/                    # a track reused across videos
  palette.md                # optional: the hex values from BRIEF.md
```

Rules:

- Files here are **copied**, never symlinked — a render must not depend on this folder.
- Replace a brand asset: change it here, then re-copy into each video that uses it
  (`cp -a brand/. ../<video>/assets/brand/`) and re-render. Earlier renders stay as history.
- Keep it small. Per-video media belongs in that video's own `assets/`.
