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

def create_drop_area(root, texture, label_text, prefix, checkbox_values):
    """Erstellt ein individuelles Label mit Drop-Zone für jede Textur."""
    frame = tk.Frame(root, padx=10, pady=10, relief=tk.RAISED, borderwidth=2)
    frame.pack(fill=tk.X, padx=5, pady=5)

    label = tk.Label(frame, text=f'Drop .rvmat for {label_text}', padx=10, pady=10)
    label.pack(fill=tk.X)

    root.drop_target_register(DND_FILES)
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', lambda event: drop(event, texture, prefix, checkbox_values))

def main():
    """Hauptprogramm für die Tkinter-GUI."""
    root = TkinterDnD.Tk()
    root.title('RwG RVMat Speedo')
    root.geometry('500x610')

    # Icon hinzufügen
    root.iconbitmap('RwG_Logo_Modelling.ico')

    # Checkboxen für NOHQ, AS und SMDI (werden JETZT nach root erstellt)
    checkbox_values = {
        "NOHQ": tk.BooleanVar(),
        "AS": tk.BooleanVar(),
        "SMDI": tk.BooleanVar()
    }

    checkbox_frame = tk.Frame(root, padx=10, pady=10)
    checkbox_frame.pack()

    tk.Checkbutton(checkbox_frame, text="Replace NOHQ with default", variable=checkbox_values["NOHQ"]).pack(anchor="w")
    tk.Checkbutton(checkbox_frame, text="Replace AS with default", variable=checkbox_values["AS"]).pack(anchor="w")
    tk.Checkbutton(checkbox_frame, text="Replace SMDI with default", variable=checkbox_values["SMDI"]).pack(anchor="w")

    # Texturen für Auswahl
    textures = [
        ('dz\\characters\\data\\generic_worn_mc.paa', 'Generic Worn', '_worn'),
        ('dz\\characters\\data\\generic_damage_mc.paa', 'Generic Damage', '_damage'),
        ('dz\\characters\\data\\generic_destruct_mc.paa', 'Generic Destruct', '_destruct'),
        ('dz\\characters\\data\\generic_plastic_damage_mc.paa', 'Plastic Damage', '_damage'),
        ('dz\\characters\\data\\generic_wood_worn_mc.paa', 'Wood Worn', '_worn'),
        ('dz\\characters\\data\\generic_wood_damage_mc.paa', 'Wood Damage', '_damage'),
        ('dz\\characters\\data\\generic_wood_destruct_mc.paa', 'Wood Destruct', '_destruct')
    ]

    for texture, label_text, prefix in textures:
        create_drop_area(root, texture, label_text, prefix, checkbox_values)

    root.mainloop()

if __name__ == '__main__':
    main()




