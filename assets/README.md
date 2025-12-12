# Assets Folder

This folder contains assets for the application builds.

## Required Files

### Windows
- `icon.ico` - Application icon (for Windows executable)
  - Recommended size: 256x256 pixels
  - Format: .ico file

### Linux
- `icon.png` - Application icon (for Linux packages)
  - Recommended size: 256x256 pixels or 512x512 pixels
  - Format: .png file

## Creating Icons

### For Windows (.ico)
You can create an icon from any image using:

1. **Online converter**: https://convertio.co/png-ico/
2. **GIMP**: Export as .ico format
3. **Icon editors**: IcoFX, Greenfish Icon Editor Pro

### For Linux (.png)
You can use any PNG image. For best results:
- Use square dimensions (256x256, 512x512, etc.)
- Keep it simple for small sizes
- Use transparent background if appropriate

### Creating Both from One Image
If you have a PNG image:
1. Save it as `icon.png` for Linux
2. Convert it to `icon.ico` for Windows using an online tool or GIMP

## Placeholder

If you don't have an icon yet, the build scripts will work without it (packages will use a default system icon).

