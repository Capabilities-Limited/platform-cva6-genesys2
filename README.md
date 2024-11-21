# CVA6: development platform for [PlatformIO](https://platformio.org)

This repository is based on the Shakti PlatformIO repository (https://github.com/platformio/platform-shakti)

# Usage

1. [Install PlatformIO](https://platformio.org)
2. Create PlatformIO project and configure a platform option in [platformio.ini](https://docs.platformio.org/page/projectconf.html) file:

```ini
[env:stable]
platform = cva6
board = ...
...
```

Until released to the PlatformIO repository, copy (or symlink) this repository into your PlatformIO install, e.g. "~/.platformio/platforms/".
