import tkinter as tk
from tkinter import simpledialog

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Campo de Texto Pop-up")

def save_text():
    global content 
    content = campo_texto.get("1.0", "end-1c")
    ventana.quit()
    return content

def cancel_text():
    pass

# Crear un campo de texto
campo_texto = tk.Text(ventana, height=10, width=40)
campo_texto.grid(row=0,column=0,columnspan=2)

btn_save = tk.Button(ventana,text="Aceptar",command=save_text)
btn_save.grid(row=1,column=0,sticky="ew")

btn_cancel = tk.Button(ventana,text="Cancelar",command=ventana.quit)
btn_cancel.grid(row=1,column=1,sticky="ew")

content = ""

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()

print(content)