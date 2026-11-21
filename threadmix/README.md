# ThreadMix Auto DJ

> **This is the copy of the website in the [sideblabs.com](https://github.com/logge/sideblabs.com) repository, published at https://sideblabs.com/threadmix/.** It was copied from the `threadmix` repository, which is still published at https://logge.github.io/threadmix and still holds the installers (its Releases): the download buttons point there. Change the site here, and there too for as long as both are up. This copy also has the video (https://www.youtube.com/watch?v=RaKkexU7fUg): the picture at the top is its play button, and it plays in a window on the page (the link's `data-film`, and the end of the page's script).

A DJ that runs itself. Point it at your music and it plays one continuous,
beatmatched mix.

**Website and downloads: https://logge.github.io/threadmix**

This repository holds the website (GitHub Pages, from `main`) and the
installers ([Releases](https://github.com/logge/threadmix/releases)). The
source code of each version is attached to its release as
`ThreadMix-source.zip`.

The release assets keep the same names from version to version, so the site's
download links (`releases/latest/download/<name>`) never need editing:

| Asset | What |
|---|---|
| `ThreadMix-Windows-Setup.exe` | Windows installer |
| `ThreadMix-Linux-Vulkan-x86_64.AppImage` | Linux AppImage (x86-64), AI on the GPU through Vulkan |
| `ThreadMix-Linux-x86_64.AppImage` | Linux AppImage (x86-64), AI on the processor only |
| `ThreadMix-macOS.zip` | Mac app, zipped (Apple Silicon) |
| `ThreadMix-source.zip` | Complete source of that version |
| `ThreadMix-macOS-source.zip` | Source of the Mac app, when it was built from a different commit |
| `ThreadMix-Linux-source.zip` | Source of the Linux AppImages, when they were built from a different commit |

`scripts/make-appimage.sh` names its images with the version
(`ThreadMix-0.1.1-x86_64.AppImage`, `ThreadMix-0.1.1-vulkan-x86_64.AppImage`);
rename them to the names above when uploading.
