# Changelog

All notable changes to **RwG RVMat Speedo** are listed here.

## v1.3 — Custom textures + dark UI (2026-08)

### Added

- **Custom Textures** — set your **own** `_mc` paths for **Worn**, **Damage**
  and **Destruct** and drop a `.rvmat` onto their fields to bake them into
  `Stage3`. Each field reads its path live, so the same drop zone follows
  whatever you type or **Browse**.
- **Save / Load presets** — store the three custom paths under a name and bring
  them back in one click; **Delete** (with confirm) removes one. Presets are
  kept in `rvmat_speedo_presets.json` next to the app.

### Changed

- **Dark RwG interface** matching the RwG Texture Converter — dark panels, green
  accents, a titled header, and **green hover feedback** on the drop fields
  (was red).
- Damage-stage words (Worn / Damage / Destruct / Burn / Rotten) are re-tinted
  for readability on the dark background.
- The window auto-sizes to its content and now shows a proper app icon.

### Unchanged

- The `.rvmat` rewrite logic (Stage3 swap, optional NOHQ/AS/SMDI defaults, new
  file with the `_worn` / `_damage` / `_destruct` suffix) and all built-in DayZ
  texture categories are exactly as before.

## v1.2 — Baseline

Drag-&-drop `.rvmat` damage/destruct generator with built-in DayZ textures for
Generic, Wood, Food, Weapons, Cloth and Plastic, plus optional NOHQ/AS/SMDI
default replacement.
