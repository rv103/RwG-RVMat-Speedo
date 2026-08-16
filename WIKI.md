# RwG RVMat Speedo — Wiki

A drag-&-drop helper that spawns **damage / destruct / worn** `.rvmat` variants
for DayZ in seconds. Drop your base `.rvmat` on a field, get a new file with the
right damage `_mc` texture baked into `Stage3` — original untouched.

> Each `##` section is self-contained and can become its own wiki page. Part of
> the RwG toolset — more at [rwg-addon.com](https://rwg-addon.com/).

---

## Table of contents

1. [What problem it solves](#what-problem-it-solves)
2. [How a DayZ damage rvmat works](#how-a-dayz-damage-rvmat-works)
3. [Install & run](#install--run)
4. [Basic workflow](#basic-workflow)
5. [The categories](#the-categories)
6. [Default NOHQ / AS / SMDI](#default-nohq--as--smdi)
7. [Custom textures & presets](#custom-textures--presets)
8. [Building the .exe](#building-the-exe)
9. [Troubleshooting & FAQ](#troubleshooting--faq)
10. [Credits & license](#credits--license)

---

## What problem it solves

A DayZ item usually needs several material states — a clean `.rvmat`, plus
`_damage` and `_destruct` (and sometimes `_worn`) versions that differ only in
which **`_mc`** (macro / colour-mask) texture the material uses. Making those by
hand — copy the file, rename it, edit the `Stage3` texture line — is repetitive.
RVMat Speedo does it with a single drag & drop and never touches your original.

---

## How a DayZ damage rvmat works

The visible "damage" of an item comes from the **`_mc`** texture referenced in
**`Stage3`** of the `.rvmat`. Swapping that texture for a *damaged* or
*destroyed* `_mc` is what turns a clean material into a damaged one. The engine
picks the right state through the item's `config.cpp` health levels, which point
at these `_worn` / `_damage` / `_destruct` files.

RVMat Speedo rewrites **`Stage3`** to the chosen `_mc` and writes a new file with
the matching suffix. Optionally it also resets:

| Stage | Map | Default written |
|---|---|---|
| Stage1 | `NOHQ` (normal) | `#(argb,8,8,3)color(0.5,0.5,1,1,NOHQ)` |
| Stage4 | `AS` (ambient shadow) | `#(argb,8,8,3)color(1,1,1,1,AS)` |
| Stage5 | `SMDI` (specular) | `#(argb,8,8,3)color(1,1,1,1,SMDI)` |

Those flat-colour defaults are DayZ's "no-op" values for a channel you don't need
on the damage state.

---

## Install & run

**From source**

```
pip install tkinterdnd2
python RwG_RVMat_Speedo.py
```

**Packaged** — download `RwG_RVMat_Speedo.exe` from the repo's **Releases**; no
Python needed.

Requirement: **tkinterdnd2** (drag & drop). Tkinter itself ships with Python.

---

## Basic workflow

1. Start the app.
2. (Optional) tick **Replace NOHQ / AS / SMDI with default** if the damage state
   should drop those channels.
3. **Drag your base `.rvmat`** onto the field for the state you want — e.g.
   *Generic → Destruct*. The field glows **green** while hovering.
4. Release. A new file appears **next to the original**, e.g.
   `myitem.rvmat` → `myitem_destruct.rvmat`, with the destruct `_mc` in Stage3.

Repeat for each state; drop the same base file on Worn, Damage and Destruct to
generate the full set.

---

## The categories

Built-in DayZ `_mc` textures, grouped so you grab the right one fast:

- **Generic** — Worn / Damage / Destruct (`dz\characters\data\generic_*`).
- **Wood** — Worn / Damage / Destruct (`generic_wood_*`).
- **Food** — Burn / Rotten / Rotten2 (`dz\gear\food\data\food_generic_*`).
- **Weapons** — Damage/Destruct for Generic, Metal and Wood
  (`dz\weapons\data\weapons_*`).
- **Cloth** — Damage/Destruct for Tops, Vests, Pants, Shoes
  (`dz\characters\<slot>\data\*`).
- **Plastic** — Damage (`generic_plastic_damage_mc`).

The suffix on the output file follows the field (`_worn` / `_damage` /
`_destruct`, and `_burnt` / `_rotten` for food).

---

## Default NOHQ / AS / SMDI

The three checkboxes at the top decide whether, **in addition** to the Stage3
swap, the tool also overwrites Stage1/4/5 with the flat default colour values
above. Leave them off to keep the material's existing normal/AS/SMDI; tick the
ones your damage state should blank out. The setting applies to every drop while
it's ticked.

---

## Custom textures & presets

Use your **own** `_mc` maps instead of the built-in DayZ ones:

1. In **Custom Textures**, fill **Worn**, **Damage** and/or **Destruct** with the
   mod-relative path to your `_mc` (type it, or **Browse** to a file). Example:
   `MyMod\weapons\data\ak_damage_mc.paa`.
2. Drop a `.rvmat` onto that row's field — the tool reads the path **live** and
   writes it into Stage3, with the same `_worn` / `_damage` / `_destruct` suffix
   rule.
3. **Save** stores the three paths under a name you choose. **Load** applies the
   selected preset back into the fields. **Delete** removes it (asks first).

Presets are stored in **`rvmat_speedo_presets.json`** next to the app, so they
persist between sessions and are easy to back up or share.

> Tip: use **mod-relative** paths (as they must appear in-game), not absolute
> `C:\...` paths. Browse is a convenience for locating the file — adjust the
> path to its `P:\`/mod-relative form if needed.

---

## Building the .exe

```
pip install pyinstaller tkinterdnd2
pyinstaller RwG_RVMat_Speedo.spec
```

`dist\RwG_RVMat_Speedo.exe` is produced. The spec bundles the **tkinterdnd2**
data files and the window icon and builds a windowed (no-console) one-file exe.
If PyInstaller can't find tkinterdnd2, correct the path in the spec's `datas`
line to your environment's `site-packages\tkinterdnd2`.

---

## Troubleshooting & FAQ

**Nothing happens when I drop a file.** — It must be a `.rvmat`. Other files are
ignored (the console prints a note).

**The texture didn't change.** — The tool edits **`Stage3`** only. If your
material puts the `_mc` in a different stage, that line won't match. Send me a
sample `.rvmat` and I'll adapt the pattern.

**My custom path didn't get written.** — The matching **Custom Textures** field
was empty at drop time. Fill Worn/Damage/Destruct (or Load a preset) first.

**`ModuleNotFoundError: tkinterdnd2`.** — `pip install tkinterdnd2` into the
Python you run the app with.

**Absolute path ended up in the rvmat.** — Browse inserts the file's real path;
edit it to the mod-relative form DayZ expects before dropping.

---

## Credits & license

Built by **RwG** for the DayZ modding community. Licensed under **GPL-3.0** — see
[`LICENSE`](LICENSE). Video: https://youtu.be/3A_nh4P5XZA
