import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("8 segment editor")
root.geometry("640x400")
root.resizable(False, False)

segments = ["A","B","C","D","E","F","G","P"]

pin_map = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"P":7}
seg_state = {s:0 for s in segments}

# ==============================
# HITUNG NILAI
# ==============================

def calculate():

    bits=[0]*8

    for s in segments:
        if seg_state[s]:
            bits[pin_map[s]]=1

    binary="".join(str(x) for x in reversed(bits))
    dec=int(binary,2)
    hx=format(dec,"02X")

    cath_hex.set(hx)
    cath_dec.set(dec)
    cath_bin.set(binary)

    inv="".join("1" if b=="0" else "0" for b in binary)

    dec2=int(inv,2)
    hx2=format(dec2,"02X")

    ano_hex.set(hx2)
    ano_dec.set(dec2)
    ano_bin.set(inv)

# ==============================
# TOGGLE SEGMENT
# ==============================

def toggle(seg):

    seg_state[seg]=1-seg_state[seg]

    color="red" if seg_state[seg] else "white"
    canvas.itemconfig(seg_shapes[seg],fill=color)

    calculate()

# ==============================
# UPDATE PIN MAP
# ==============================

def update_mapping():

    for s in segments:
        pin_map[s]=int(combos[s].get())

    calculate()

# ==============================
# EXPORT
# ==============================

def show_export():

    digit_segments = {
        0:["A","B","C","D","E","F"],
        1:["B","C"],
        2:["A","B","G","E","D"],
        3:["A","B","C","D","G"],
        4:["F","G","B","C"],
        5:["A","F","G","C","D"],
        6:["A","F","G","E","C","D"],
        7:["A","B","C"],
        8:["A","B","C","D","E","F","G"],
        9:["A","B","C","D","F","G"]
    }

    text="COMMON CATHODE\n"
    text+="Digit | Hex | Dec | Binary\n"
    text+="---------------------------\n"

    cath_values=[]

    for digit in range(10):

        bits=[0]*8

        for seg in digit_segments[digit]:
            bits[pin_map[seg]]=1

        binary="".join(str(x) for x in reversed(bits))
        dec=int(binary,2)
        hx=format(dec,"02X")

        cath_values.append(dec)

        text+=f"{digit}     | {hx}  | {dec:3d} | {binary}\n"

    text+="\nCOMMON ANODE\n"
    text+="Digit | Hex | Dec | Binary\n"
    text+="---------------------------\n"

    anode_values=[]

    for digit in range(10):

        cath=cath_values[digit]
        anode=(~cath)&0xFF

        anode_values.append(anode)

        binary=format(anode,"08b")
        dec=anode
        hx=format(anode,"02X")

        text+=f"{digit}     | {hx}  | {dec:3d} | {binary}\n"

    text+="\nARDUINO ARRAY\n\n"

    cath_array="byte segCathode[10] = {"
    cath_array+=",".join(f"0x{format(v,'02X')}" for v in cath_values)
    cath_array+="};\n\n"

    anode_array="byte segAnode[10] = {"
    anode_array+=",".join(f"0x{format(v,'02X')}" for v in anode_values)
    anode_array+="};"

    text+=cath_array
    text+=anode_array

    win=tk.Toplevel(root)
    win.title("7 Segment Table 0-9")
    win.geometry("450x420")

    txt=tk.Text(win,font=("Consolas",11))
    txt.pack(fill="both",expand=True)

    txt.insert("1.0",text)
    txt.config(state="disabled")

# ==============================
# LAYOUT
# ==============================

left=tk.Frame(root)
left.pack(side="left",padx=10,pady=10)

center=tk.Frame(root)
center.pack(side="left")

right=tk.Frame(root)
right.pack(side="right",padx=10)

# ==============================
# PANEL KIRI
# ==============================

tk.Label(left,text="Common cathode").pack(anchor="w")

cath_hex=tk.StringVar(value="00")
cath_dec=tk.StringVar(value="0")
cath_bin=tk.StringVar(value="00000000")

tk.Entry(left,textvariable=cath_hex,width=14).pack(anchor="w")
tk.Entry(left,textvariable=cath_dec,width=14).pack(anchor="w")
tk.Entry(left,textvariable=cath_bin,width=14).pack(anchor="w")

tk.Label(left,text="").pack()

tk.Label(left,text="Common anode").pack(anchor="w")

ano_hex=tk.StringVar(value="FF")
ano_dec=tk.StringVar(value="255")
ano_bin=tk.StringVar(value="11111111")

tk.Entry(left,textvariable=ano_hex,width=14).pack(anchor="w")
tk.Entry(left,textvariable=ano_dec,width=14).pack(anchor="w")
tk.Entry(left,textvariable=ano_bin,width=14).pack(anchor="w")

# ==============================
# CANVAS
# ==============================

canvas=tk.Canvas(center,width=260,height=320,bg="white")
canvas.pack()

seg_shapes={}

seg_shapes["A"]=canvas.create_polygon(90,30,170,30,185,45,170,60,90,60,75,45,outline="red",fill="white",width=2)
seg_shapes["B"]=canvas.create_polygon(185,55,205,75,205,145,185,165,165,145,165,75,outline="red",fill="white",width=2)
seg_shapes["C"]=canvas.create_polygon(185,175,205,195,205,265,185,285,165,265,165,195,outline="red",fill="white",width=2)
seg_shapes["D"]=canvas.create_polygon(90,290,170,290,185,305,170,320,90,320,75,305,outline="red",fill="white",width=2)
seg_shapes["E"]=canvas.create_polygon(55,195,75,175,95,195,95,265,75,285,55,265,outline="red",fill="white",width=2)
seg_shapes["F"]=canvas.create_polygon(55,75,75,55,95,75,95,145,75,165,55,145,outline="red",fill="white",width=2)
seg_shapes["G"]=canvas.create_polygon(90,155,170,155,185,170,170,185,90,185,75,170,outline="red",fill="white",width=2)
seg_shapes["P"]=canvas.create_oval(215,290,230,305,outline="red",fill="white",width=2)

# label segmen
canvas.create_text(130,15,text="A")
canvas.create_text(220,110,text="B")
canvas.create_text(220,230,text="C")
canvas.create_text(130,275,text="D")
canvas.create_text(40,230,text="E")
canvas.create_text(40,110,text="F")
canvas.create_text(130,170,text="G")
canvas.create_text(230,315,text="P")

for s in seg_shapes:
    canvas.tag_bind(seg_shapes[s],"<Button-1>",lambda e,seg=s:toggle(seg))

# ==============================
# PANEL LED PIN
# ==============================

tk.Label(right,text="LED PIN").pack()

combos={}

for seg in segments:

    row=tk.Frame(right)
    row.pack(anchor="w")

    tk.Label(row,text=seg,width=2).pack(side="left")

    combo=ttk.Combobox(row,values=list(range(8)),width=4,state="readonly")
    combo.set(pin_map[seg])
    combo.pack(side="left")

    combos[seg]=combo

tk.Button(right,text="Update",command=update_mapping).pack(pady=6)

# ==============================
# BUTTON
# ==============================

tk.Button(root,text="Export 0-9",command=show_export,width=14).pack(side="bottom",pady=8)

calculate()

root.mainloop()

