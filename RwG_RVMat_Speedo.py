import os
import re
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

def modify_rvmat(file_path, texture, prefix, checkbox_values):
    """Modifiziert eine .rvmat-Datei, ersetzt Texturen in Stage1, Stage3, Stage4 und Stage5 je nach Auswahl."""
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()

    # Ersetze texture in Stage3
    pattern_stage3 = r'(class Stage3\s*{[^}]*?\btexture=)"[^"]+";'
    replacement_stage3 = rf'\1"{texture.replace("\\", "\\\\")}";'
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
    """Event-Handler für Drag & Drop mit korrekten Textur-Parametern."""
    file_path = event.data.strip('{}')  # Entfernt geschweifte Klammern bei Drag & Drop Pfaden
    if file_path.endswith('.rvmat'):
        modify_rvmat(file_path, texture, prefix, checkbox_values)
    else:
        print('Please drop a valid .rvmat file.')

def create_drop_area(root, texture, label_text, prefix, checkbox_values, row, column):
    """Erstellt ein individuelles Label mit Drop-Zone für jede Textur."""
    frame = tk.Frame(root, padx=10, pady=10, relief=tk.RAISED, borderwidth=2)
    frame.grid(row=row, column=column, padx=5, pady=5)

    label = tk.Label(frame, text=f'Add {label_text}', padx=10, pady=10)
    label.pack(fill=tk.X)

    def on_enter(event):
        frame.config(bg='red')

    def on_leave(event):
        frame.config(bg='SystemButtonFace')

    def on_drop(event):
        frame.config(bg='SystemButtonFace')
        drop(event, texture, prefix, checkbox_values)

    root.drop_target_register(DND_FILES)
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<DropEnter>>', on_enter)
    label.dnd_bind('<<DropLeave>>', on_leave)
    label.dnd_bind('<<Drop>>', on_drop)

def main():
    """Hauptprogramm für die Tkinter-GUI."""
    root = TkinterDnD.Tk()
    root.title('RwG RVMat Speedo 1.1')
    root.geometry('600x980')  # Breitere Fenstergröße für horizontales Layout

    # Checkboxen für NOHQ, AS und SMDI (werden JETZT nach root erstellt)
    checkbox_values = {
        "NOHQ": tk.BooleanVar(),
        "AS": tk.BooleanVar(),
        "SMDI": tk.BooleanVar()
    }

    checkbox_frame = tk.Frame(root, padx=10, pady=10)
    checkbox_frame.grid(row=0, column=0, columnspan=3)

    tk.Checkbutton(checkbox_frame, text="Replace NOHQ with default", variable=checkbox_values["NOHQ"]).pack(anchor="w")
    tk.Checkbutton(checkbox_frame, text="Replace AS with default", variable=checkbox_values["AS"]).pack(anchor="w")
    tk.Checkbutton(checkbox_frame, text="Replace SMDI with default", variable=checkbox_values["SMDI"]).pack(anchor="w")

    # Rahmen für die Drop-Zonen
    tk.Label(root, text="Generic Textures", font=("Arial", 14)).grid(row=1, column=0, columnspan=3)
    drop_frame_generic = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_generic.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Wood Textures", font=("Arial", 14)).grid(row=3, column=0, columnspan=3)
    drop_frame_wood = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_wood.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Food Textures", font=("Arial", 14)).grid(row=5, column=0, columnspan=3)
    drop_frame_food = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_food.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Weapons Textures", font=("Arial", 14)).grid(row=7, column=0, columnspan=3)
    drop_frame_weapons = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_weapons.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Weapons Metal Textures", font=("Arial", 14)).grid(row=9, column=0, columnspan=3)
    drop_frame_weapons_metal = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_weapons_metal.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Weapons Wood Textures", font=("Arial", 14)).grid(row=11, column=0, columnspan=3)
    drop_frame_weapons_wood = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_weapons_wood.grid(row=12, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Plastic Textures", font=("Arial", 14)).grid(row=13, column=0, columnspan=3)
    drop_frame_plastic = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_plastic.grid(row=14, column=0, columnspan=3, padx=10, pady=10)

    # Texturen für Auswahl
    textures_generic = [
        ('dz\\characters\\data\\generic_worn_mc.paa', 'Generic Worn', '_worn'),
        ('dz\\characters\\data\\generic_damage_mc.paa', 'Generic Damage', '_damage'),
        ('dz\\characters\\data\\generic_destruct_mc.paa', 'Generic Destruct', '_destruct')
    ]

    textures_wood =[
        ('dz\\characters\\data\\generic_wood_worn_mc.paa', 'Wood Worn', '_worn'),
        ('dz\\characters\\data\\generic_wood_damage_mc.paa', 'Wood Damage', '_damage'),
        ('dz\\characters\\data\\generic_wood_destruct_mc.paa', 'Wood Destruct', '_destruct')
    ]
    textures_food = [
        ('dz\\gear\\food\\data\\food_generic_burn_mc.paa', 'Food Generic Burn', '_burnt'),
        ('dz\\gear\\food\\data\\food_generic_rot_mc.paa', 'Food Generic Rotten', '_rotten'),
        ('dz\\gear\\food\\data\\food_generic_rot2_mc.paa', 'Food Generic Rotten2', '_rotten')
    ]
    textures_weapons = [
        ('dz\\weapons\\data\\weapons_damage_generic_mc.paa', 'Weapons Damage Generic', '_damage'),
        ('dz\\weapons\\data\\weapons_destruct_generic_mc.paa', 'Weapons Destruct Generic', '_destruct')
    ]
    textures_weapons_metal = [
        ('dz\\weapons\\data\\weapons_damage_metal_mc.paa', 'Weapons Damage Metal', '_damage'),
        ('dz\\weapons\\data\\weapons_destruct_metal_mc.paa', 'Weapons Destruct Metal', '_destruct')
    ]
    textures_weapons_wood = [
        ('dz\\weapons\\data\\weapons_damage_wood_mc.paa', 'Weapons Damage Wood', '_damage'),
        ('dz\\weapons\\data\\weapons_destruct_wood_mc.paa', 'Weapons Destrcut Wood', '_destruct')
    ]
    textures_plastic = [
        ('dz\\characters\\data\\generic_plastic_damage_mc.paa', 'Plastic Damage', '_damage')
    ]

    row = 0
    column = 0
    for texture, label_text, prefix in textures_generic:
        create_drop_area(drop_frame_generic, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_wood:
        create_drop_area(drop_frame_wood, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_food:
        create_drop_area(drop_frame_food, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_weapons:
        create_drop_area(drop_frame_weapons, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_weapons_metal:
        create_drop_area(drop_frame_weapons_metal, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_weapons_wood:
        create_drop_area(drop_frame_weapons_wood, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_plastic:
        create_drop_area(drop_frame_plastic, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    root.mainloop()

if __name__ == '__main__':
    main()