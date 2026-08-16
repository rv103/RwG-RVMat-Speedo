import os
import re
import sys
import json
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

# --------------------------------------------------------------------------- #
#  RwG dark theme (matches the RwG Texture Converter)                          #
# --------------------------------------------------------------------------- #
THEME = {
    "bg":        "#1e1f22",   # window background
    "panel":     "#26282c",   # group / drop-frame background
    "field":     "#2f3237",   # drop-tile / entry background
    "border":    "#3a3d42",   # subtle separators
    "fg":        "#e6e6e6",   # primary text
    "muted":     "#a8adb3",   # secondary text
    "accent":    "#4a8f66",   # RwG green
    "accent_hi": "#6fae86",   # brighter green (hover / highlight)
    "white":     "#ffffff",
}

# Damage-stage words, tinted for readability on the dark background.
WORD_COLORS = {
    "Worn":     "#ffd54a",   # gold
    "Damage":   "#ff9f45",   # orange
    "Destruct": "#ff5c5c",   # red
    "Burn":     "#d9945a",   # tan / brown
    "Rotten":   "#3fd0c9",   # turquoise
}


# --------------------------------------------------------------------------- #
#  Core: rewrite the .rvmat                                                    #
# --------------------------------------------------------------------------- #
def modify_rvmat(file_path, texture, prefix, checkbox_values):
    """Modifiziert eine .rvmat-Datei, ersetzt Texturen in Stage1, Stage3, Stage4 und Stage5 je nach Auswahl."""
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()

    # Ersetze texture in Stage3 (gefixt)
    pattern_stage3 = r'(class Stage3\s*{[^}]*?\btexture=)"[^"]+";'
    replacement_stage3 = r'\1"' + texture.replace("\\", "\\\\") + '";'
    content = re.sub(pattern_stage3, replacement_stage3, content, flags=re.DOTALL)

    # Falls NOHQ-Checkbox aktiv ist, ersetze texture in Stage1
    if checkbox_values["NOHQ"].get():
        pattern_stage1 = r'(class Stage1\s*{[^}]*?\btexture=)"[^"]+";'
        replacement_stage1 = r'\1"#(argb,8,8,3)color(0.5,0.5,1,1,NOHQ)";'
        content = re.sub(pattern_stage1, replacement_stage1, content, flags=re.DOTALL)

    # Falls AS-Checkbox aktiv ist, ersetze texture in Stage4
    if checkbox_values["AS"].get():
        pattern_stage4 = r'(class Stage4\s*{[^}]*?\btexture=)"[^"]+";'
        replacement_stage4 = r'\1"#(argb,8,8,3)color(1,1,1,1,AS)";'
        content = re.sub(pattern_stage4, replacement_stage4, content, flags=re.DOTALL)

    # Falls SMDI-Checkbox aktiv ist, ersetze texture in Stage5
    if checkbox_values["SMDI"].get():
        pattern_stage5 = r'(class Stage5\s*{[^}]*?\btexture=)"[^"]+";'
        replacement_stage5 = r'\1"#(argb,8,8,3)color(1,1,1,1,SMDI)";'
        content = re.sub(pattern_stage5, replacement_stage5, content, flags=re.DOTALL)

    # Neuer Dateiname mit Suffix
    new_file_path = os.path.splitext(file_path)[0] + prefix + '.rvmat'
    with open(new_file_path, 'w', encoding="utf-8") as file:
        file.write(content)

    print(f'Modified file saved as: {new_file_path}')
    return new_file_path


def drop(event, texture, prefix, checkbox_values):
    """Event-Handler für Drag & Drop. ``texture`` darf ein String ODER eine
    Funktion sein (für benutzereigene, live aus einem Eingabefeld gelesene Pfade)."""
    tex = texture() if callable(texture) else texture
    if not tex:
        print("No texture set for this slot — enter a custom _mc path first.")
        return
    file_path = event.data.strip('{}')  # Entfernt geschweifte Klammern bei Drag & Drop Pfaden
    if file_path.endswith('.rvmat'):
        modify_rvmat(file_path, tex, prefix, checkbox_values)
    else:
        print('Please drop a valid .rvmat file.')


# --------------------------------------------------------------------------- #
#  Presets for custom textures (save / load)                                  #
# --------------------------------------------------------------------------- #
def _presets_path():
    """Where the custom-texture presets live (next to the .exe / script)."""
    base = (os.path.dirname(sys.executable) if getattr(sys, "frozen", False)
            else os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "rvmat_speedo_presets.json")


def load_presets():
    try:
        with open(_presets_path(), encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_presets(presets):
    try:
        with open(_presets_path(), "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2)
    except Exception as e:
        print(f"Could not save presets: {e}")


# --------------------------------------------------------------------------- #
#  Widgets                                                                     #
# --------------------------------------------------------------------------- #
def create_drop_area(root, texture, label_text, prefix, checkbox_values, row, column):
    """Erstellt ein Label mit Drop-Zone. ``texture`` = fester Pfad oder Callable."""
    frame = tk.Frame(root, padx=5, pady=5, bg=THEME["field"],
                     highlightthickness=1, highlightbackground=THEME["border"],
                     highlightcolor=THEME["border"])
    frame.grid(row=row, column=column, padx=6, pady=6, sticky="nsew")

    text_widget = tk.Text(frame, height=1, width=19, borderwidth=0,
                          bg=THEME["field"], fg=THEME["fg"],
                          highlightthickness=0, cursor="hand2")
    text_widget.pack(fill=tk.BOTH, expand=True)
    text_widget.insert(tk.END, label_text)

    text_widget.tag_configure("center", justify="center")
    text_widget.tag_add("center", "1.0", "end")

    for word, color in WORD_COLORS.items():
        if word in label_text:
            start_idx = label_text.index(word)
            end_idx = start_idx + len(word)
            text_widget.tag_configure(color, foreground=color)
            text_widget.tag_add(color, f"1.{start_idx}", f"1.{end_idx}")

    text_widget.config(state=tk.DISABLED)

    def _set_bg(color):
        frame.config(bg=color)
        text_widget.config(state=tk.NORMAL)
        text_widget.config(bg=color)
        text_widget.config(state=tk.DISABLED)

    def on_enter(event):
        _set_bg(THEME["accent"])          # green hover feedback

    def on_leave(event):
        _set_bg(THEME["field"])

    def on_drop(event):
        _set_bg(THEME["field"])
        drop(event, texture, prefix, checkbox_values)

    root.drop_target_register(DND_FILES)
    text_widget.drop_target_register(DND_FILES)
    text_widget.dnd_bind('<<DropEnter>>', on_enter)
    text_widget.dnd_bind('<<DropLeave>>', on_leave)
    text_widget.dnd_bind('<<Drop>>', on_drop)


def _group_label(root, text, row):
    tk.Label(root, text=text, font=("Segoe UI", 13, "bold"),
             bg=THEME["bg"], fg=THEME["accent_hi"]
             ).grid(row=row, column=0, columnspan=3, pady=(10, 0))


def _drop_frame(root, row):
    f = tk.Frame(root, bg=THEME["panel"], highlightthickness=1,
                 highlightbackground=THEME["border"], highlightcolor=THEME["border"])
    f.grid(row=row, column=0, columnspan=3, padx=10, pady=(4, 8))
    return f


def _button(parent, text, command):
    return tk.Button(parent, text=text, command=command,
                     bg=THEME["panel"], fg=THEME["fg"], relief="flat", bd=0,
                     activebackground=THEME["accent"], activeforeground=THEME["white"],
                     padx=10, pady=3, highlightthickness=0, cursor="hand2")


class _Rows:
    """Tiny incrementing grid-row counter so the layout stays easy to reorder."""
    def __init__(self):
        self.r = 0

    def next(self):
        v = self.r
        self.r += 1
        return v


# --------------------------------------------------------------------------- #
#  Main GUI                                                                    #
# --------------------------------------------------------------------------- #
def main():
    root = TkinterDnD.Tk()
    root.title('RwG RVMat Speedo 1.3')
    root.geometry('760x940')
    root.configure(bg=THEME["bg"])

    try:  # window icon (Windows); harmless if unavailable / on other OSes
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        root.iconbitmap(os.path.join(base, "RwG_Logo_Modelling.ico"))
    except Exception:
        pass

    rr = _Rows()

    # ----- header ---------------------------------------------------------- #
    header = tk.Frame(root, bg=THEME["bg"])
    header.grid(row=rr.next(), column=0, columnspan=3, pady=(16, 2), sticky="ew")
    tk.Label(header, text="RwG RVMat Speedo", font=("Segoe UI", 20, "bold"),
             bg=THEME["bg"], fg=THEME["accent_hi"]).pack()
    tk.Label(header,
             text="Drag & drop a .rvmat onto a field to spawn its "
                  "worn / damage / destruct variant",
             font=("Segoe UI", 9), bg=THEME["bg"], fg=THEME["muted"]).pack(pady=(2, 0))
    tk.Frame(root, bg=THEME["accent"], height=2).grid(
        row=rr.next(), column=0, columnspan=3, sticky="ew", padx=40, pady=(6, 4))

    # ----- default-map checkboxes ------------------------------------------ #
    checkbox_frame = tk.Frame(root, bg=THEME["bg"], padx=10, pady=6)
    checkbox_frame.grid(row=rr.next(), column=0, columnspan=3)

    def _checkbox(text, var):
        tk.Checkbutton(checkbox_frame, text=text, variable=var,
                       bg=THEME["bg"], fg=THEME["fg"], selectcolor=THEME["field"],
                       activebackground=THEME["bg"], activeforeground=THEME["accent_hi"],
                       highlightthickness=0, bd=0, anchor="w").pack(anchor="w")

    checkbox_values = {
        "NOHQ": tk.BooleanVar(),
        "AS": tk.BooleanVar(),
        "SMDI": tk.BooleanVar(),
    }
    _checkbox("Replace NOHQ with default", checkbox_values["NOHQ"])
    _checkbox("Replace AS with default", checkbox_values["AS"])
    _checkbox("Replace SMDI with default", checkbox_values["SMDI"])

    # ----- CUSTOM textures (your own _mc) + save / load -------------------- #
    _group_label(root, "Custom Textures  (your own _mc)", rr.next())
    custom = tk.Frame(root, bg=THEME["panel"], padx=8, pady=8,
                      highlightthickness=1, highlightbackground=THEME["border"])
    custom.grid(row=rr.next(), column=0, columnspan=3, padx=10, pady=(4, 4), sticky="ew")
    custom.grid_columnconfigure(1, weight=1)

    custom_vars = {"Worn": tk.StringVar(), "Damage": tk.StringVar(), "Destruct": tk.StringVar()}
    custom_suffix = {"Worn": "_worn", "Damage": "_damage", "Destruct": "_destruct"}

    def _browse_paa(var):
        p = filedialog.askopenfilename(
            title="Select your _mc texture",
            filetypes=[("DayZ texture", "*.paa;*.tga"), ("All files", "*.*")])
        if p:
            var.set(p)

    for i, name in enumerate(("Worn", "Damage", "Destruct")):
        tk.Label(custom, text=name, width=9, anchor="w", bg=THEME["panel"],
                 fg=WORD_COLORS[name], font=("Segoe UI", 10, "bold")
                 ).grid(row=i, column=0, padx=(2, 6), pady=4, sticky="w")
        tk.Entry(custom, textvariable=custom_vars[name], width=42,
                 bg=THEME["field"], fg=THEME["fg"], insertbackground=THEME["fg"],
                 relief="flat", highlightthickness=1, highlightbackground=THEME["border"],
                 highlightcolor=THEME["accent"]
                 ).grid(row=i, column=1, padx=6, pady=4, sticky="we")
        _button(custom, "Browse", lambda v=custom_vars[name]: _browse_paa(v)
                ).grid(row=i, column=2, padx=4, pady=4)
        # drop tile that reads the entry live at drop time
        create_drop_area(custom, (lambda v=custom_vars[name]: v.get().strip()),
                         f"Drop → {name}", custom_suffix[name], checkbox_values,
                         row=i, column=3)

    # presets bar
    bar = tk.Frame(root, bg=THEME["bg"])
    bar.grid(row=rr.next(), column=0, columnspan=3, pady=(2, 6))
    tk.Label(bar, text="Preset:", bg=THEME["bg"], fg=THEME["fg"]).pack(side="left", padx=(4, 4))

    preset_var = tk.StringVar()
    presets = load_presets()
    preset_menu = tk.OptionMenu(bar, preset_var, "")
    preset_menu.config(bg=THEME["panel"], fg=THEME["fg"], activebackground=THEME["accent"],
                       activeforeground=THEME["white"], relief="flat", highlightthickness=0,
                       width=18)
    preset_menu["menu"].config(bg=THEME["panel"], fg=THEME["fg"],
                               activebackground=THEME["accent"], activeforeground=THEME["white"])
    preset_menu.pack(side="left", padx=4)

    def _refresh_menu():
        m = preset_menu["menu"]
        m.delete(0, "end")
        names = sorted(presets.keys())
        for n in names:
            m.add_command(label=n, command=lambda v=n: preset_var.set(v))
        if names:
            if preset_var.get() not in names:
                preset_var.set(names[0])
        else:
            preset_var.set("")

    def on_save():
        name = simpledialog.askstring("Save preset", "Preset name:", parent=root)
        if not name:
            return
        presets[name] = {k: custom_vars[k].get().strip() for k in custom_vars}
        save_presets(presets)
        _refresh_menu()
        preset_var.set(name)

    def on_load():
        n = preset_var.get()
        if n in presets:
            for k in custom_vars:
                custom_vars[k].set(presets[n].get(k, ""))

    def on_delete():
        n = preset_var.get()
        if n in presets and messagebox.askyesno("Delete preset",
                                                f"Delete preset '{n}'?", parent=root):
            presets.pop(n, None)
            save_presets(presets)
            _refresh_menu()

    _button(bar, "Save", on_save).pack(side="left", padx=3)
    _button(bar, "Load", on_load).pack(side="left", padx=3)
    _button(bar, "Delete", on_delete).pack(side="left", padx=3)
    _refresh_menu()

    # ----- built-in DayZ categories ---------------------------------------- #
    def _category(title):
        _group_label(root, title, rr.next())
        return _drop_frame(root, rr.next())

    drop_frame_generic = _category("Generic Textures")
    drop_frame_wood = _category("Wood Textures")
    drop_frame_food = _category("Food Textures")
    drop_frame_weapons = _category("Weapons Textures")
    drop_frame_cloth = _category("Cloth Textures")
    drop_frame_plastic = _category("Plastic Textures")

    textures_generic = [
        ('dz\\characters\\data\\generic_worn_mc.paa', 'Worn', '_worn'),
        ('dz\\characters\\data\\generic_damage_mc.paa', 'Damage', '_damage'),
        ('dz\\characters\\data\\generic_destruct_mc.paa', 'Destruct', '_destruct')
    ]
    textures_wood = [
        ('dz\\characters\\data\\generic_wood_worn_mc.paa', 'Worn', '_worn'),
        ('dz\\characters\\data\\generic_wood_damage_mc.paa', 'Damage', '_damage'),
        ('dz\\characters\\data\\generic_wood_destruct_mc.paa', 'Destruct', '_destruct')
    ]
    textures_food = [
        ('dz\\gear\\food\\data\\food_generic_burn_mc.paa', 'Burn', '_burnt'),
        ('dz\\gear\\food\\data\\food_generic_rot_mc.paa', 'Rotten', '_rotten'),
        ('dz\\gear\\food\\data\\food_generic_rot2_mc.paa', 'Rotten2', '_rotten')
    ]
    textures_weapons = [
        ('dz\\weapons\\data\\weapons_damage_generic_mc.paa', 'Damage Generic', '_damage'),
        ('dz\\weapons\\data\\weapons_destruct_generic_mc.paa', 'Destruct Generic', '_destruct')
    ]
    textures_weapons_metal = [
        ('dz\\weapons\\data\\weapons_damage_metal_mc.paa', 'Damage Metal', '_damage'),
        ('dz\\weapons\\data\\weapons_destruct_metal_mc.paa', 'Destruct Metal', '_destruct')
    ]
    textures_weapons_wood = [
        ('dz\\weapons\\data\\weapons_damage_wood_mc.paa', 'Damage Wood', '_damage'),
        ('dz\\weapons\\data\\weapons_destruct_wood_mc.paa', 'Destruct Wood', '_destruct')
    ]
    textures_plastic = [
        ('dz\\characters\\data\\generic_plastic_damage_mc.paa', 'Damage', '_damage')
    ]
    textures_cloth_tops = [
        ('dz\\characters\\tops\\data\\tops_damage_mc.paa', 'Tops Damage', '_damage'),
        ('dz\\characters\\tops\\data\\tops_destruct_mc.paa', 'Tops Destruct', '_destruct')
    ]
    textures_cloth_vests = [
        ('dz\\characters\\vests\\data\\vests_damage_mc.paa', 'Vests Damage', '_damage'),
        ('dz\\characters\\vests\\data\\vests_destruct_mc.paa', 'Vests Destruct', '_destruct')
    ]
    textures_cloth_pants = [
        ('dz\\characters\\pants\\data\\pants_damage_mc.paa', 'Pants Damage', '_damage'),
        ('dz\\characters\\pants\\data\\pants_destruct_mc.paa', 'Pants Destruct', '_destruct')
    ]
    textures_cloth_shoes = [
        ('dz\\characters\\shoes\\data\\shoes_damage_mc.paa', 'Shoes Damage', '_damage'),
        ('dz\\characters\\shoes\\data\\shoes_destruct_mc.paa', 'Shoes Destruct', '_destruct')
    ]

    column = 0
    for texture, label_text, prefix in textures_generic:
        create_drop_area(drop_frame_generic, texture, label_text, prefix, checkbox_values, 0, column)
        column += 1

    column = 0
    for texture, label_text, prefix in textures_wood:
        create_drop_area(drop_frame_wood, texture, label_text, prefix, checkbox_values, 0, column)
        column += 1

    column = 0
    for texture, label_text, prefix in textures_food:
        create_drop_area(drop_frame_food, texture, label_text, prefix, checkbox_values, 0, column)
        column += 1

    column = 0
    for texture, label_text, prefix in textures_weapons:
        create_drop_area(drop_frame_weapons, texture, label_text, prefix, checkbox_values, 0, column)
        column += 1
    column = 0
    for texture, label_text, prefix in textures_weapons_metal:
        create_drop_area(drop_frame_weapons, texture, label_text, prefix, checkbox_values, 1, column)
        column += 1
    column = 0
    for texture, label_text, prefix in textures_weapons_wood:
        create_drop_area(drop_frame_weapons, texture, label_text, prefix, checkbox_values, 2, column)
        column += 1

    row = 0
    for texture, label_text, prefix in textures_cloth_tops:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, 0)
        row += 1
    row = 0
    for texture, label_text, prefix in textures_cloth_vests:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, 1)
        row += 1
    row = 0
    for texture, label_text, prefix in textures_cloth_pants:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, 2)
        row += 1
    row = 0
    for texture, label_text, prefix in textures_cloth_shoes:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, 3)
        row += 1

    column = 0
    for texture, label_text, prefix in textures_plastic:
        create_drop_area(drop_frame_plastic, texture, label_text, prefix, checkbox_values, 0, column)
        column += 1

    # size to fit the content (keeps every category fully visible)
    root.update_idletasks()
    root.geometry(f"{max(760, root.winfo_reqwidth() + 20)}x{root.winfo_reqheight() + 20}")

    root.mainloop()


if __name__ == '__main__':
    main()
