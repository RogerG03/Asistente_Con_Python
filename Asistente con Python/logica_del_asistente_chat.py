import pywhatkit, keyboard, datetime, openai, time, os, webbrowser, psutil
from pygame import mixer
import colores
from multiprocessing import Process, Queue
import subprocess as sub
from AppOpener import open as app_open
import chatbot


#Openai Chatgpt
openai.api_key = ''

#-----------------------------------------------------------------------
sitios = {
    'google': 'https://www.google.com',
    'facebook': 'https://www.facebook.com',
    'twitter': 'https://www.twitter.com',
    'linkedin': 'https://www.linkedin.com',
    'github': 'https://www.github.com',
    'reddit': 'https://www.reddit.com',
    'youtube': 'https://www.youtube.com',
    'instagram': 'https://www.instagram.com',
    'whatsapp': 'https://web.whatsapp.com',
}

#-----------------------------------------------------------------------------------------
def hablar(texto):
    chat.ruperta_responde(texto)

#Funcion de escuchar

def establecer_referencia(ref):
    global chat
    chat = ref

#------------------------------------------------------------------------------------------------------

def obtener_saludo():
    hora_actual = datetime.datetime.now().hour

    if 6 <= hora_actual < 12:
        return "Buenos días, usuario. ¿Cómo puedo asistirte hoy?"
    elif 12 <= hora_actual < 18:
        return "Buenas tardes, usuario. ¿Qué te gustaría hacer hoy?"
    else:
        return "Buenas noches, usuario. ¿Necesitas algo antes de ir a dormir?"    

#Funciones de abrir y cerrar programas-----------------
def abrir_aplicacion(nombre_aplicacion):
    try:
        app_open(nombre_aplicacion, match_closest=True)
        hablar(f"Abriendo {nombre_aplicacion}")
    except Exception as e:
        hablar(f"Hubo un error al intentar abrir {nombre_aplicacion}")
        print(f"Error: {e}")

def cerrar_programa(nombre_programa):
    for proceso in psutil.process_iter():
        try:
            info = proceso.as_dict(attrs=['name', 'pid'])
            if nombre_programa.lower() in info['name'].lower():
                proceso.terminate()
                print(f"Se ha cerrado el programa: {info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

#Realiza una pregunta o solicitud y mediante la key da una respuesta de Chat-Gpt------------------

def obtener_respuesta_openai(pregunta):
    respuesta = openai.Completion.create(
        engine='text-davinci-003',
        prompt=pregunta,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5
    )
    respuesta_texto = respuesta.choices[0].text.strip()
    escribir_archivo(pregunta, respuesta_texto)
    return respuesta_texto

#Escribe la respuesta de openai en un archivo para facilitar obtencion del texto 

def escribir_archivo(nombre_archivo, contenido):
    # Asegúrate de que la carpeta 'archivos' exista, si no, la crea
    if not os.path.exists('archivos'):
        os.makedirs('archivos')

    # Incluye la ruta de la carpeta en el nombre del archivo
    nombre_archivo = os.path.join('archivos', nombre_archivo + '.txt')

    # Comprueba si el archivo ya existe
    if os.path.isfile(nombre_archivo + '.txt'):
        print(f"El archivo {nombre_archivo} ya existe. Sobrescribiendo...")
    else:
        print(f"Creando el archivo {nombre_archivo + '.txt'}...")

    # Abre el archivo en modo de escritura (esto creará el archivo si no existe, o lo sobrescribirá si ya existe)
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        # Escribe el contenido en el archivo
        archivo.write(contenido)
    print(f"El contenido ha sido escrito en {nombre_archivo}")
    sub.Popen(os.path.abspath(nombre_archivo), shell=True)

#Funcion de las notas en archivo nota.txt-----------
def anotar(nota_escrita):
    try:
        with open(os.path.abspath("notas/notas.txt"), 'a', encoding='utf-8') as f:
            f.write('-' + nota_escrita + os.linesep)
            f.close()
            hablar("Nota anotada en notas.txt... Esperando nueva orden")
            sub.Popen(os.path.abspath("notas/notas.txt"), shell=True) #abre el archivo notas        
    
    except FileNotFoundError as e:
        print(e)
        file = open(os.path.abspath("notas/notas.txt"), 'w', encoding='utf-8')
        file.write('-' + nota_escrita + os.linesep)
        file.close()
        hablar("Nota anotada en notas.txt... Esperando nueva orden")
        sub.Popen(os.path.abspath("notas/notas.txt"), shell=True) #abre el archivo notas

#Funciones de crear y eliminar carpeta---------------------------------------------------------

def crear_carpeta(nombre_carpeta):
    ruta_carpeta = os.path.join(os.path.expanduser('~'), 'Desktop', nombre_carpeta)
    try:
        os.makedirs(ruta_carpeta)
        hablar(f"La carpeta {nombre_carpeta} ha sido creada en el escritorio.")
    except FileExistsError:
        hablar(f"La carpeta {nombre_carpeta} ya existe en el escritorio.")

def eliminar_carpeta(nombre_carpeta):
    ruta_carpeta = os.path.join(os.path.expanduser('~'), 'Desktop', nombre_carpeta)
    try:
        os.rmdir(ruta_carpeta)
        hablar(f"La carpeta {nombre_carpeta} ha sido eliminada del escritorio.")
    except FileNotFoundError:
        hablar(f"La carpeta {nombre_carpeta} no existe en el escritorio.")


#Funcion iniciada como subproceso--------------------------------

def funcion_alarma(alarma):
    while True:
        if datetime.datetime.now().strftime('%H:%M') == alarma: #Si la hora actual es igual a alarma 
            print("Despierta!!!!")
            hablar("alarma sonando")
            mixer.init()
            mixer.music.load(R"GUI/alarma.mp3")
            mixer.music.play()
            if keyboard.is_pressed("up"):
                mixer.music.stop()
                break
        time.sleep(10)  # Espera 10 segundos antes de comprobar de nuevo

#Respuestas de Ruperta ------------------------------------------------------
def chatbot_response(message):
    ints = chatbot.predict_class(message)
    res = chatbot.get_response(ints, chatbot.intents)
    return res

#------------------------------------------------------
def definir_alarma(alarma):
    alarma = alarma.replace(".", "").strip()
    alarma = alarma.replace("a las", "").strip()
    print(alarma)
    hablar("Alarma activada a las " + alarma + " horas")
    p = Process(target=funcion_alarma, args=(alarma,))
    p.start()
#Codigo para el chat----------------

def iniciar_chat(mensaje_ruperta):
   
        #manda a llamar funcion escuchar
        orden = mensaje_ruperta
        print(f'Usuario: {orden}') #Imprime la orden del usuario 
        
        if "reproduce" in orden: #Reproduce musica en YT
            cancion = orden.replace("reproduce", "").strip() #reemplazamos reproduce con espacio vacio 
            hablar("¡Excelente elección! Reproduciendo " + cancion)
            pywhatkit.playonyt(cancion)

        elif "dime" in orden: #Llama a la libreria de openai y responde una pregunta 
            pregunta = orden.replace("dime", "").strip()
            hablar("Permíteme buscar información sobre ello.")
            respuesta = obtener_respuesta_openai(pregunta) #Funcion pregunta 
            hablar("Aquí está lo que encontré: " + respuesta)
            print("Aquí está lo que encontré: " + respuesta)

        elif "busca" in orden: #Busca cualquier cosa en google
            consulta = orden.replace("busca", "").strip()
            hablar("¡Vamos a buscar eso en Internet! Buscando: " + consulta)
            pywhatkit.search(consulta)

        elif "alarma" in orden: #Programa alarma a cualquier hora
            hablar("¿A qué hora debo establecer la alarma?") #R/ a las 1:05
            hablar("El formato debe ser: 'a las 1:05' por ejemplo")
            chat.respuesta2 = True
            chat.funcion = lambda alarma: definir_alarma(alarma)


        elif 'colores' in orden:
            hablar('Como usted diga!!')
            q = Queue()
            p = Process(target=colores.captura, args=(q,))
            p.start()
            while True:
                if not q.empty():
                    color = q.get()
                    hablar(f"Detecté el color {color}")
                    chat.window.update()
                    time.sleep(2)
                elif keyboard.is_pressed("up"):
                    p.terminate()
                    break
        
        elif 'entra a' in orden: #entra a paginas preestablecidas
            for sitio_a_buscar in sitios:
                if sitio_a_buscar in orden:
                    url = sitios.get(sitio_a_buscar)
                    if url:
                        hablar(f'abriendo{sitio_a_buscar}') 
                        webbrowser.open(url, new=2)  # new=2 abre en una nueva pestaña, si es posible
                    else:
                        print(f"No tengo la URL para {sitio_a_buscar}")

        elif 'escribe' in orden:
            
            hablar("Dime. ¿que quieres anotar?")
            chat.respuesta2 = True
            chat.funcion = lambda nota: anotar(nota)

        elif "abre" in orden:
            nombre_aplicacion = orden.replace("abre", "").strip()
            abrir_aplicacion(nombre_aplicacion)
        
        elif "cierra" in orden:
            nombre_aplicacion = orden.replace("cierra", "").strip()
            cerrar_programa(nombre_aplicacion)
            hablar(f"Se ha cerrado {nombre_aplicacion}")

        elif 'hora' in orden:
            hora_actual = datetime.datetime.now().time()  # obtiene la hora actual
            hablar(f"Son las {hora_actual.hour} con {hora_actual.minute}")

        elif 'fecha' in orden:
            fecha_actual = datetime.datetime.now().date()  # obtiene la fecha actual
            hablar(f"Hoy es el {fecha_actual.day} del mes {fecha_actual.month} del año {fecha_actual.year}")

        elif 'crear carpeta' in orden:
            hablar("¿Cómo quieres llamar a la carpeta?")
            chat.respuesta2 = True
            chat.funcion = lambda nombre_carpeta: crear_carpeta(nombre_carpeta)


        elif 'eliminar carpeta' in orden:
            hablar("¿Cuál carpeta quieres eliminar?")
            chat.respuesta2 = True
            chat.funcion = lambda nombre_carpeta: eliminar_carpeta(nombre_carpeta)
        
        elif "nos vemos" in orden:
            hablar("Fue un placer ayudarte. ¡Hasta luego!")
        
        else:
            # Si no se encontró ninguna coincidencia, pasa la orden al chatbot
            if orden is "":
                pass
            
            else:    
                respuesta_chatbot = chatbot_response(orden)
                hablar(respuesta_chatbot)
                print(respuesta_chatbot)

#if __name__ == '__main__':
    #saludo = obtener_saludo()
    #hablar(saludo)
    #hablar("Soy Ruperta, tu asistente virtual. ¿Cómo puedo ayudarte hoy?")
    #iniciar()

