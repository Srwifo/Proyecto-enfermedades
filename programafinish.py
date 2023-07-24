import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import random
import json
import math
import matplotlib.pyplot as plt

class SimulacionWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Simulación de infección")

        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.num_ciudadanos_entry = Gtk.Entry()
        self.num_ciudadanos_entry.set_text("1000")
        hbox = Gtk.Box(spacing=6)
        hbox.pack_start(Gtk.Label("Población total:"), False, False, 0)
        hbox.pack_start(self.num_ciudadanos_entry, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        self.tasa_recuperacion_entry = Gtk.Entry()
        self.tasa_recuperacion_entry.set_text("0.05")
        hbox = Gtk.Box(spacing=6)
        hbox.pack_start(Gtk.Label("Tasa de recuperación:"), False, False, 0)
        hbox.pack_start(self.tasa_recuperacion_entry, True, True, 0)
        vbox.pack_start(hbox,True,True,0)

        self.tasa_infeccion_entry = Gtk.Entry()
        self.tasa_infeccion_entry.set_text("0.1")
        hbox = Gtk.Box(spacing=6)
        hbox.pack_start(Gtk.Label("Tasa de infección:"), False, False, 0)
        hbox.pack_start(self.tasa_infeccion_entry, True, True, 0)
        vbox.pack_start(hbox,True,True,0)

        button = Gtk.Button(label="Simular")
        button.connect("clicked", self.on_simular_clicked)
        vbox.pack_start(button,True,True,0)

    def on_simular_clicked(self, button):
        num_ciudadanos = int(self.num_ciudadanos_entry.get_text())
        tasa_recuperacion = float(self.tasa_recuperacion_entry.get_text())
        tasa_infeccion = float(self.tasa_infeccion_entry.get_text())

        print(f"Ejecutando simulación con {num_ciudadanos} ciudadanos,tasa de recuperación {tasa_recuperacion} y tasa de infección {tasa_infeccion}")

        ENFERMEDAD = "Sano"
        comunidad = Comunidad(num_ciudadanos=num_ciudadanos, promedio_conexion_fisica=random.uniform(0, 1), enfermedad=ENFERMEDAD, num_infectados=0, probabilidad_conexion_fisica=random.uniform(0, 1), tasa_infeccion=tasa_infeccion, tasa_recuperacion=tasa_recuperacion)
        ciudadanos = []
        dias = []
        totales = []
        infectados_lista = []
        nuevos_infectados_lista = []
        recuperados_lista = []
        vacunados_lista = []

        with open('datosnombres.json', 'r') as f:
            data = json.load(f)
            nombres = data['nombres']
            apellidos = data['apellidos']

        for i in range(num_ciudadanos):
            estado = "Sano"
            ciudadano = Ciudadano(comunidad=comunidad, id=i,nombre=random.choice(nombres), apellido=random.choice(apellidos), familia=random.randint(1,10), enfermedad=ENFERMEDAD, estado=estado)
            ciudadanos.append(ciudadano)

        porcentaje_infectados = random.randint(1, 10) / 100
        num_infectados_iniciales = math.ceil(num_ciudadanos * porcentaje_infectados)

        infectados_iniciales = random.sample(ciudadanos,num_infectados_iniciales)
        for infectado in infectados_iniciales:
            infectado.estado="Infectado"

        resultados_win = ResultadosWindow(comunidad=comunidad,
                                            ciudadanos=ciudadanos,
                                            dias=dias,
                                            totales=totales,
                                            infectados_lista=infectados_lista,
                                            nuevos_infectados_lista=nuevos_infectados_lista,
                                            recuperados_lista=recuperados_lista,
                                            vacunados_lista=vacunados_lista)
        resultados_win.show_all()
class ResultadosWindow(Gtk.Window):
    def __init__(self, comunidad, ciudadanos, dias, totales, infectados_lista, nuevos_infectados_lista, recuperados_lista, vacunados_lista):
      Gtk.Window.__init__(self,title="Resultados de la simulación")
      self.set_default_size(500,400)
      self.set_border_width(10)

      self.comunidad = comunidad
      self.ciudadanos = ciudadanos
      self.dias = dias
      self.totales = totales
      self.infectados_lista = infectados_lista
      self.nuevos_infectados_lista = nuevos_infectados_lista
      self.recuperados_lista = recuperados_lista
      self.vacunados_lista = vacunados_lista

      hbox=Gtk.Box(spacing=6)
      self.add(hbox)

      self.resultados_label=Gtk.Label()
      self.resultados_label.set_line_wrap(True)
      self.resultados_label.set_max_width_chars(50)
      hbox.pack_start(self.resultados_label,True,True,0)

      scrolled_window=Gtk.ScrolledWindow()
      scrolled_window.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)
      hbox.pack_start(scrolled_window,True,True,0)

      self.historial_label=Gtk.Label()
      self.historial_label.set_line_wrap(True)
      scrolled_window.add(self.historial_label)

      vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
      hbox.pack_start(vbox,True,True,0)

      button=Gtk.Button(label="Simular día")
      button.connect("clicked",self.on_simular_dia_clicked)
      vbox.pack_start(button,True,True,0)

      button=Gtk.Button(label="Gráfico")
      button.connect("clicked",self.on_grafico_clicked)
      vbox.pack_start(button,True,True,0)

      menu_button=Gtk.MenuButton.new()
      vbox.pack_start(menu_button,True,True,0)
      menu=Gtk.PopoverMenu.new()
      menu_button.set_popover(menu)

      box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
      menu.add(box)

      button=Gtk.ModelButton(label="Información ciudadanos")
      button.connect("clicked",self.on_info_ciudadanos_clicked)
      box.pack_start(button,True,True,0)

      button=Gtk.ModelButton(label="Información vacunados")
      button.connect("clicked",self.on_info_vacunados_clicked)
      box.pack_start(button,True,True,0)

      button=Gtk.ModelButton(label="Manual")
      button.connect("clicked",self.on_manual_clicked)
      box.pack_start(button,True,True,0)

      menu.show_all()

    def on_simular_dia_clicked(self,button):
        dia = len(self.dias)
        simular_dia(dia,
                    self.comunidad,
                    self.ciudadanos,
                    self.dias,
                    self.totales,
                    self.infectados_lista,
                    self.nuevos_infectados_lista,
                    self.recuperados_lista,
                    self.vacunados_lista)
        infectados = self.infectados_lista[-1]
        recuperados = self.recuperados_lista[-1]
        
        vacunados = self.vacunados_lista[-1]
        susceptibles = self.totales[-1] - infectados - recuperados- vacunados
        resultados = f"Resultados del día {dia}:\nTotal Infectados: {infectados}\nTotal Recuperados: {recuperados}\nTotal Susceptibles: {susceptibles}\nVacunados: {vacunados}"
        historial = self.historial_label.get_text() + "\n\n" + resultados
        self.resultados_label.set_text(resultados)
        self.historial_label.set_text(historial)

    def on_grafico_clicked(self,button):
        plt.plot(self.dias, self.infectados_lista, label="Infectados totales")
        plt.plot(self.dias, self.nuevos_infectados_lista, label="Nuevos infectados")
        plt.plot(self.dias, self.recuperados_lista,label="Recuperados")
        plt.plot(self.dias,self.vacunados_lista,label="Vacunados")
        plt.legend()
        plt.show()

    def on_info_ciudadanos_clicked(self,button):
        info_win=InfoCiudadanosWindow(ciudadanos=self.ciudadanos)
        info_win.show_all()

    def on_info_vacunados_clicked(self,button):
        info_win=InfoVacunadosWindow(ciudadanos=self.ciudadanos)
        info_win.show_all()

    def on_manual_clicked(self,button):
        info_win=ManualWindow()
        info_win.show_all()

class InfoCiudadanosWindow(Gtk.Window):
    def __init__(self, ciudadanos):
        Gtk.Window.__init__(self,title="Información ciudadanos")
        self.set_default_size(600,400)
        scrolled_window=Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)
        self.add(scrolled_window)

        label=Gtk.Label()
        label.set_line_wrap(True)

        texto = "\n".join([str(c) for c in ciudadanos])
        label.set_text(texto)

        scrolled_window.add(label)

class InfoVacunadosWindow(Gtk.Window):
    def __init__(self, ciudadanos):
        Gtk.Window.__init__(self,title="Información vacunados")
        self.set_default_size(600,400)

        scrolled_window=Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)
        self.add(scrolled_window)

        label=Gtk.Label()
        label.set_line_wrap(True)

        vacunados = [c for c in ciudadanos if c.vacuna is not None]
        tipos_vacunas = {"A": 0, "B": 0, "C": 0}
        for c in vacunados:
            tipos_vacunas[c.vacuna.tipo] += 1
        inmunes = [c for c in vacunados if c.estado == "Inmune"]
        texto = f"Total de vacunados: {len(vacunados)}\n\n"
        texto += f"Vacunas tipo A: {tipos_vacunas['A']}\n"
        texto += f"Vacunas tipo B: {tipos_vacunas['B']}\n"
        texto += f"Vacunas tipo C: {tipos_vacunas['C']}\n\n"
        texto += f"Vacunas que ganaron inmunidad: {len(inmunes)}\n\n"
        texto += "\n".join([str(c) for c in vacunados])
        label.set_text(texto)

        scrolled_window.add(label)

class ManualWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Manual")
        self.set_default_size(600,400)

        scrolled_window=Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER,Gtk.PolicyType.AUTOMATIC)
        self.add(scrolled_window)

        label=Gtk.Label()
        label.set_line_wrap(True)

        label.set_text("Manual del usuario...")
        scrolled_window.add(label)

def simular_dia(dia, comunidad, ciudadanos, dias, totales, infectados_lista, nuevos_infectados_lista, recuperados_lista, vacunados_lista):
    infectados = 0
    susceptibles = 0
    recuperados = 0
    for ciudadano in ciudadanos:
        if ciudadano.estado == "Infectado":
            infectados += 1
            prob_recuperacion = comunidad.tasa_recuperacion
            if random.random() < prob_recuperacion:
                ciudadano.estado = "Recuperado"
        elif ciudadano.estado == "Sano" and (ciudadano.vacuna is None or (ciudadano.vacuna is not None and ciudadano.estado not in ["Inmune", "No inmune"])):
            susceptibles += 1
            prob_infeccion = comunidad.tasa_infeccion
            if tiene_familiar_infectado(ciudadano, ciudadanos):
                prob_infeccion *= 2
            if ciudadano.comunidad.probabilidad_conexion_fisica == 1:
                prob_infeccion = 1
            if random.random() < prob_infeccion:
                ciudadano.estado = "Infectado"
        elif ciudadano.estado == "Recuperado":
            recuperados += 1

    for ciudadano in ciudadanos:
        if ciudadano.vacuna is not None and dia - ciudadano.vacuna.dia >= 1 and ciudadano.estado != "Inmune":
            if not ciudadano.tuvo_oportunidad_inmunidad: 
                if random.random() <= ciudadano.vacuna.efectividad:
                    ciudadano.estado = "Inmune"
                else:
                    ciudadano.estado= "No inmune"
                ciudadano.tuvo_oportunidad_inmunidad = True

    vacunados = [c for c in ciudadanos if c.vacuna is not None]
    inmunes = [c for c in vacunados if c.estado == "Inmune"]

    print(f"Día {dia}:")
    print(f"Infectados = {infectados}")
    print(f"Susceptibles = {susceptibles}")
    print(f"Recuperados = {recuperados}")
    print(f"Vacunados = {len(vacunados)}")
    print(f"Inmunes = {len(inmunes)}")
    print()

    dias.append(dia)
    totales.append(len(ciudadanos))
    infectados_lista.append(infectados)
    nuevos_infectados = infectados - (infectados_lista[-2] if len(infectados_lista) > 1 else 0)
    nuevos_infectados_lista.append(nuevos_infectados)
    recuperados_lista.append(recuperados)
    vacunados_lista.append(len(vacunados))

    asignar_vacunas(dia, comunidad, ciudadanos)

def tiene_familiar_infectado(ciudadano, ciudadanos):
    for otro in ciudadanos:
        if otro.familia == ciudadano.familia:
            if otro.estado == "Infectado":
                return True
    return False


class Comunidad:
    def __init__(self, num_ciudadanos, promedio_conexion_fisica, enfermedad, num_infectados, probabilidad_conexion_fisica, tasa_infeccion, tasa_recuperacion):
        self.num_ciudadanos = num_ciudadanos 
        self.promedio_conexion_fisica = promedio_conexion_fisica 
        self.enfermedad = enfermedad 
        self.num_infectados = num_infectados 
        self.probabilidad_conexion_fisica = probabilidad_conexion_fisica
        self.tasa_infeccion = tasa_infeccion
        self.tasa_recuperacion=tasa_recuperacion
       
class Ciudadano:
    def __init__(self, comunidad, id, nombre, apellido, familia, enfermedad, estado):
        self.comunidad = comunidad
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.familia = familia
        self.enfermedad = enfermedad
        self.estado = estado
        self.vacuna = None
        self.tuvo_oportunidad_inmunidad = False

    def __str__(self):
        vacunado = "Sí" if self.vacuna is not None else "No"
        tipo_vacuna = self.vacuna.tipo if self.vacuna is not None else "N/A"
        return f"ID: {self.id} Nombre: {self.nombre} Apellido: {self.apellido} Familia: {self.familia}\nEnfermedad: {self.enfermedad} Estado: {self.estado} Vacunado: {vacunado} Tipo de vacuna: {tipo_vacuna}"
class Vacunacion:
    def __init__(self, tipo, efectividad, dia):
        self.tipo = tipo
        self.efectividad = efectividad
        self.dia = dia

def asignar_vacunas(dia,comunidad, ciudadanos):
    num_vacunas = int(comunidad.num_ciudadanos * 0.4)
    vacunas = {
            "A": {"cantidad": int(num_vacunas * 0.25), "efectividad": 1.0},
            "B": {"cantidad": int(num_vacunas * 0.5), "efectividad": 0.5},
            "C": {"cantidad": int(num_vacunas * 0.25), "efectividad": 0.25}
        }
    if 5 == dia:
        ciudadanos.sort(key=lambda c: tiene_familiar_infectado(c, ciudadanos))
        vacunas_asignadas = 0  
        for ciudadano in ciudadanos:
            if ciudadano.estado == "Sano" and ciudadano.vacuna is None:
                for tipo, datos in vacunas.items():
                    if datos["cantidad"] > 0:
                        ciudadano.vacuna = Vacunacion(tipo=tipo, efectividad=datos["efectividad"], dia=dia)
                        datos["cantidad"] -= 1
                        vacunas_asignadas += 1  
                        if vacunas_asignadas >= num_vacunas: 
                            return
                        break

win = SimulacionWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()