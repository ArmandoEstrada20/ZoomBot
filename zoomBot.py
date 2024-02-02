import webbrowser
import schedule
from time import sleep
from threading import Thread
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox


class ZoomBotGUI:
    def __init__(self, name):
        # Inicialización de la interfaz gráfica de usuario (GUI)
        self.title = name
        self.window = tk.Tk()
        self.window.title(self.title)
        self.window.geometry("1020x800")
        self.window.minsize(1020, 800)
        self.window.maxsize(1020, 800)
        self.canvas = Canvas(self.window, width=1020, height=800)
        self.canvas.pack(fill="both", expand=True)
       
        # Inicialización de variables relacionadas con las reuniones programadas
        self.scheduled_meetings_count = 0
        self.meetings = {}

        self.home_page()
    
    def show_error(self, text, pos):
         # Muestra mensajes de error en la GUI
        self.err_text = Label(self.window, text=text, font=("montserrat", 10), fg="red", bg="#f0f1f1")
        self.err_text.place(x=pos[0], y=pos[1])

    def schedule_meeting(self):
        # Programa reuniones utilizando la biblioteca 'schedule' y 'webbrowser'
        time, link, day = self.meetings[self.scheduled_meetings_count - 1]
        days = {
            'Siempre': schedule.every().day,
            'Lunes': schedule.every().monday,
            'Martes':  schedule.every().tuesday,
            'Miércoles': schedule.every().wednesday,
            'Jueves': schedule.every().thursday,
            'Viernes': schedule.every().friday
        }
        if day in days:
            days[day].at(time).do(webbrowser.open_new_tab, link)

    def schedule(self):
        # Programa una nueva reunión y gestiona posibles errores
        try:
            self.err_text.destroy()
        except AttributeError:
            pass

        name = self.name.get()
        link = self.link.get()
        hrs, mins = self.time.get().split(':')
        day = self.select_weekday.get()
        if 24 > int(hrs) > 0 and 60 > int(mins) > 0:
            if 'https://' in link:
                self.meetings[self.scheduled_meetings_count] = [f"{hrs}:{mins}", link, day]
                self.scheduled_meetings.insert(self.scheduled_meetings_count, f"Próxima junta: {name} programada para el {day}, a las {hrs}:{mins} horas.")
                self.scheduled_meetings_count += 1
                self.schedule_meeting()
                self.name.delete(0, END)
                self.link.delete(0, END)
                self.time.delete(0, END)
                self.select_weekday.set('') #El combobox se reinicia
            else:
                self.show_error("El enlace de la reunión no es valido...", (26, 187))
        else:
            self.show_error("Error en la hora de la reunion, asegurate de escribirla en formato de 24 horas...", (26, 275))

    def clear_entries(self):
        self.link.delete(0, END)
        self.time.delete(0, END)

    def home_page(self):
        # Configura y muestra la página principal de la aplicación
        ancho_entry = int(196 * 1.75) 
        alto_entry = int(25 * 1.75)  

        # Añade una etiqueta para el Entry 'nombre'
        name_label = Label(self.window, text="Nombre de la reunión:", font=("monserrat", 14), bg="#f0f1f1")
        name_label.place(x=26, y=95 - alto_entry * 0.5 - 4) 
        self.name = Entry(self.window, font=("montserrat", 14))
        self.name.place(x=26, y=95, width=ancho_entry, height=alto_entry)

        # Añade una etiqueta para el Entry 'enlace'
        link_label = Label(self.window, text="Enlace de la reunión:", font=("monserrat", 14), bg="#f0f1f1")
        link_label.place(x=26, y=162 - alto_entry * 0.5 - 4) 
        self.link = Entry(self.window, font=("montserrat", 14))
        self.link.place(x=26, y=162, width=ancho_entry, height=alto_entry)

        # Añade una etiqueta para el Entry 'hora'
        time_label = Label(self.window, text="Hora de la reunión:", font=("monserrat", 14), bg="#f0f1f1")
        time_label.place(x=26, y=250 - alto_entry * 0.5 - 4) 

        self.time = Entry(self.window, font=("montserrat", 14))
        self.time.place(x=26, y=250, width=ancho_entry, height=alto_entry)

        ancho_combobox = int(30 * 1.75) 

        # Añade una etiqueta para el Combobox 'select_weekday'
        weekday_label = Label(self.window, text="Día de la reunión:", font=("monserrat", 14), bg="#f0f1f1")
        weekday_label.place(x=26, y=334 - alto_entry * 0.5 - 4) 

        self.select_weekday = Combobox(self.window, width=ancho_combobox, textvariable=tk.StringVar())
        self.select_weekday['values'] = ('Siempre', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes')
        self.select_weekday.place(x=26, y=334, width=ancho_entry, height=alto_entry)
        self.select_weekday.current()

        self.schedule_btn = Button(self.window, text="Programar reunión", command=self.schedule, borderwidth=1, bg="#389B00")
        self.schedule_btn.place(x=150, y=500)

        self.clear_btn = Button(self.window, text="Limpiar panel de reuniones", command=self.clear_listbox, borderwidth=1, bg="#DAD400")
        #self.clear_btn.place(x=150, y=570)

        # Ajusta el ancho y la altura
        ancho_listbox = 60 
        alto_listbox = 30  
        self.scheduled_meetings = Listbox(self.window, width=ancho_listbox, height=alto_listbox, font=("Arial", 12))

        # Ajusta las coordenadas x y y para centrar el Listbox
        x = (1400 - ancho_listbox * 8) // 2  # 8 es el ancho aproximado de un carácter en la fuente Arial de tamaño 12
        y = (768 - alto_listbox * 20) // 2  # 20 es la altura aproximada de un carácter en la fuente Arial de tamaño 12
        self.scheduled_meetings.place(x=x, y=y)

        # Ajusta las coordenadas x y y para el botón clear_btn
        clear_btn_x = x + ancho_listbox * 8 // 2  # Coloca el botón en el centro horizontal del Listbox
        clear_btn_y = y + alto_listbox * 20 + 10  # Añade 10 píxeles de espacio vertical
        self.clear_btn.place(x=clear_btn_x, y=clear_btn_y)


    def clear_listbox(self):
        self.scheduled_meetings.delete(0, END)

def scheduler():
    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    gui = ZoomBotGUI('Reuniones Semanales')
    Thread(target=scheduler, daemon=True).start() # Inicia un hilo para ejecutar el planificador de tareas en segundo plano
    gui.window.mainloop() # Inicia el bucle principal de la interfaz gráfica
    