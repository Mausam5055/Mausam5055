# Repository Blueprint & Recovery Guide

This file serves as a blueprint of the `README.md` structure and a recovery guide for AI agents to understand exactly how the profile is designed and what to do if the layout breaks.

## ⚠️ Recovery Instructions (If the README Breaks)

1. **Sync Issue**: If the README mysteriously reverts to an old state overnight (icons vanish, sections break), the user likely had a local Git sync issue (e.g. VS Code auto-sync pushed a stale local copy). 
2. **Action Overwrites**: If the 3D Contribution graph loses its container styling and turns back to AMOLED, check `.github/workflows/profile-3d.yml`. The Python script injecting the `rx="15"`, `stroke`, and `fill` styles into the generated SVGs must be present!
3. **Cache Busting**: If an SVG is modified but GitHub serves the old version, increment the `?v=X` cache buster parameter in the `README.md` image URL (e.g., `?v=7`).
4. **Restoration**: If the README is completely destroyed, copy the contents of the `backup/` folder (which was isolated on July 13) back to the root directory.

## 🏗️ Layout & Structure Blueprint

### 1. Header Animation
- **Format**: `<img>` inside `<div align="center">`
- **Content**: `footer.gif` animation.

### 2. Profile ASCII Header (light/dark mode aware)
- **Format**: `<picture>` inside `<a href="...">`
- **Content**: SVGs `dark_mode_v5.svg` and `light_mode_v5.svg`.

### 3. Skills & Stacks Matrix
- **Format**: An explicit HTML `<table align="center">` with `<td>` widths set to `80px`. 
- **Important Hack**: The first row contains `<sub>&nbsp;&nbsp;&nbsp;...</sub>` padding to force a rigid desktop width and horizontally scroll on mobile without shrinking the icons.
- **Content**: `skillicons.dev` badges in a 12-column grid.

### 4. Top Projects
- **Format**: An HTML `<table align="center" style="border: none;">`
- **Structure**: 
  - Left column (`300px`): Profile picture with `border-radius: 10px`.
  - Right column (`800px`): The custom Top Projects SVG (`projects_dark_v1.svg`).
- **Total Width**: `1100px`.

### 5. Hackatime Stats
- **Format**: `<picture>` inside `<div align="center">`
- **Content**: Custom ASCII terminal SVGs (`hackatime_dark_v1.svg`).
- **Container Size**: Explicitly modified to be `1100px` wide so its left and right edges sit perfectly flush with the Top Projects table above it.

### 6. 3D Contribution Graph
- **Format**: `<picture>` inside `<div align="center">`
- **Content**: Generated nightly by `.github/workflows/profile-3d.yml` (`profile-night-rainbow.svg`).
- **Styling**: It is `1280px` wide, but scales down gracefully. A Python script inside the GitHub Action automatically injects `rx="15"`, `stroke`, and a proper dark theme `fill="#161b22"` to make it perfectly mimic the other styled containers.

### 7. Connect With Me (Badges)
- **Format**: An explicit HTML `<table align="center" width="1100">`.
- **Content**: Five `img.shields.io` badges (LinkedIn, GitHub, Portfolio, Email, Discord) inside `<td>` cells of width `220px`.
- **Why?**: The table renders as a container with grid lines matching the dark theme, perfectly maintaining the `1100px` width on desktop and enabling scrolling on mobile.

### 8. Random Dev Quote
- **Format**: `<picture>` inside `<div align="center">`
- **Content**: Custom ASCII terminal SVGs (`quote_dark_v1.svg`).

### 9. Footer Animations
- **Content**: A coding GIF (`width="800"`), the GitHub Snake animation (from `output` branch), a capsule-render wave, and a 3000px wide thin line GIF at the very bottom.

---
**Agent Note**: If asked to modify any layout component, respect the `1100px` grid width to maintain visual alignment across the repository and always verify responsive behavior (e.g. mobile horizontal scrolling) is not broken.
