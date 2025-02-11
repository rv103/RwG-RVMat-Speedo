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
    frame = tk.Frame(root, padx=5, pady=5, relief=tk.RAISED, borderwidth=2)
    frame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")  # Stellt sicher, dass das Layout sauber bleibt

    # Textfeld für die Beschriftung
    text_widget = tk.Text(frame, height=1, width=19, borderwidth=0, bg=frame.cget("bg"))
    text_widget.pack(fill=tk.BOTH, expand=True)
    text_widget.insert(tk.END, label_text)
    
    # Textzentrierung
    text_widget.tag_configure("center", justify="center")
    text_widget.tag_add("center", "1.0", "end")

    # Wörter farblich markieren
    color_tags = {
        "Worn": "gold",
        "Damage": "orange",
        "Destruct": "red",
        "Burn": "brown",
        "Rotten": "turquoise"
        }

    for word, color in color_tags.items():
        if word in label_text:
            start_idx = label_text.index(word)
            end_idx = start_idx + len(word)
            text_widget.tag_configure(color, foreground=color)
            text_widget.tag_add(color, f"1.{start_idx}", f"1.{end_idx}")

    text_widget.config(state=tk.DISABLED)  # Deaktivieren der Bearbeitung

    def on_enter(event):
        frame.config(bg='red')

    def on_leave(event):
        frame.config(bg='SystemButtonFace')

    def on_drop(event):
        frame.config(bg='SystemButtonFace')
        drop(event, texture, prefix, checkbox_values)

    root.drop_target_register(DND_FILES)
    text_widget.drop_target_register(DND_FILES)
    text_widget.dnd_bind('<<DropEnter>>', on_enter)
    text_widget.dnd_bind('<<DropLeave>>', on_leave)
    text_widget.dnd_bind('<<Drop>>', on_drop)




def main():
    """Hauptprogramm für die Tkinter-GUI."""
    root = TkinterDnD.Tk()
    root.title('RwG RVMat Speedo 1.2')
    root.geometry('740x800')  # Breitere Fenstergröße für horizontales Layout

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

    tk.Label(root, text="Cloth Textures", font=("Arial", 14)).grid(row=9, column=0, columnspan=3)
    drop_frame_cloth = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_cloth.grid(row=10, column=0, columnspan=3, padx=10, pady=10)

    tk.Label(root, text="Plastic Textures", font=("Arial", 14)).grid(row=11, column=0, columnspan=3)
    drop_frame_plastic = tk.Frame(root, relief=tk.RIDGE, borderwidth=3)
    drop_frame_plastic.grid(row=12, column=0, columnspan=3, padx=10, pady=10)

    # Texturen für Auswahl
    textures_generic = [
        ('dz\\characters\\data\\generic_worn_mc.paa', 'Worn', '_worn'),
        ('dz\\characters\\data\\generic_damage_mc.paa', 'Damage', '_damage'),
        ('dz\\characters\\data\\generic_destruct_mc.paa', 'Destruct', '_destruct')
    ]

    textures_wood =[
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

    row = 1
    column = 0
    for texture, label_text, prefix in textures_weapons_metal:
        create_drop_area(drop_frame_weapons, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 2
    column = 0
    for texture, label_text, prefix in textures_weapons_wood:
        create_drop_area(drop_frame_weapons, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_cloth_tops:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, column)
        row += 1
    
    row = 0
    column = 1
    for texture, label_text, prefix in textures_cloth_vests:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, column)
        row += 1

    row = 0
    column = 2
    for texture, label_text, prefix in textures_cloth_pants:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, column)
        row += 1
    
    row = 0
    column = 3
    for texture, label_text, prefix in textures_cloth_shoes:
        create_drop_area(drop_frame_cloth, texture, label_text, prefix, checkbox_values, row, column)
        row += 1

    row = 0
    column = 0
    for texture, label_text, prefix in textures_plastic:
        create_drop_area(drop_frame_plastic, texture, label_text, prefix, checkbox_values, row, column)
        column += 1

    root.mainloop()

if __name__ == '__main__':
    main()