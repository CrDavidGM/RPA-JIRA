from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

import tkinter as tk
import json

#=================================================================
#Archivo JSON
with open("ConfigPersonal.json","r") as archivo:
    config = json.load(archivo)

navegador = config["Navegador"]
autentication_type = config["Autentication_Type"]
link_jira = config["Link_Jira"]
user_short = config["User_Short"]
password = config["Password"]
answers = config["Answers"]

mascota = answers['mascota']
equipo = answers['equipo']
pelicula = answers['pelicula']
colegio = answers['colegio']

logwork_hours = config["Logwork_hours"]
logwork_date_hour = config["Logwork_date_hour"]
#=================================================================

#=================================================================
#Cuadro emergente - descripción del trabajo
ventana = tk.Tk()
ventana.title("Campo de Texto Pop-up")

def save_text():
    global content 
    content = campo_texto.get("1.0", "end-1c")
    ventana.quit()

campo_texto = tk.Text(ventana, height=10, width=40)
campo_texto.grid(row=0,column=0,columnspan=2)

btn_save = tk.Button(ventana,text="Aceptar",command=save_text)
btn_save.grid(row=1,column=0,sticky="ew")

btn_cancel = tk.Button(ventana,text="Cancelar",command=ventana.quit)
btn_cancel.grid(row=1,column=1,sticky="ew")

content = "Hola desde el script"

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
#=================================================================


#Meses dict
meses = {"01":"ene","02":"feb","03":"mar","04":"abr","05":"may","06":"jun","07":"jul","08":"ago","09":"sep","10":"oct","11":"nov","12":"dic"}

# Obtener la fecha y hora actual
fecha_actual = datetime.now()
formato = "%d/%m/%y"
dia,mes,año = fecha_actual.strftime(formato).split("/")

if logwork_date_hour == "":
    fecha_formateada = f"{dia}/{meses[mes]}/{año} 09:00 AM"
else:
    fecha_formateada = logwork_date_hour
#print(fecha_formateada)

opciones = webdriver.ChromeOptions()
#opciones.add_argument("--headless")
driver = webdriver.Chrome(options=opciones)

# Abrir el sitio web del Jira
driver.get(link_jira)
time.sleep(5)
# Get the current URL.
current_url = driver.current_url

wait = WebDriverWait(driver,15)

#Posibles respuestas al link
# 1. Ingreso deirecto
# 2. Colocando el correo completo
# 3. Colocando el usuario corto

link_responses_html_elements = ['UserName','','']

# If the current URL is not the expected URL
if current_url != link_jira:

    new_url = f"{current_url[0:8]}{user_short}:{password}@{current_url[8:]}"
    print(new_url)
    time.sleep(1)
    driver.get(new_url)
    #verificar para cuando se encienda el VPN

    #wait.until(EC.number_of_windows_to_be(2))
    

    #to have in count https://umane.emeal.nttdata.com/jiraito/plugins/servlet/easysso/saml/fail -> page failed

    print(len(driver.window_handles))

    print("Llegué hasta acá")

    input_name = wait.until(EC.presence_of_element_located((By.NAME,"UserName")))
    input_name.send_keys(f"{user_short}@emeal.nttdata.com")

    input_password = wait.until(EC.presence_of_element_located((By.NAME,"Password")))
    input_password.send_keys(password)

    button_submit = wait.until(EC.presence_of_element_located((By.ID,"submitButton")))
    button_submit.click()

    button_change_parameters = wait.until(EC.presence_of_element_located((By.ID,"differentVerificationOption")))
    button_change_parameters.click()

    #Tipo de autenticación
    if autentication_type =='Answers':
        button_questions = wait.until(EC.presence_of_element_located((By.ID,"verificationOption2")))
        button_questions.click()

        lbl_question1 = wait.until(EC.presence_of_element_located((By.ID, "question1Input")))
        lbl_question2 = wait.until(EC.presence_of_element_located((By.ID, "question2Input")))
        question1 = lbl_question1.get_attribute("value")
        question2 = lbl_question2.get_attribute("value")

        input_ans1 = wait.until(EC.presence_of_element_located((By.NAME,"Answer1")))
        input_ans2 = wait.until(EC.presence_of_element_located((By.NAME,"Answer2")))

        question_words_ES = {"mascota":mascota,"película":pelicula,"colegio":colegio,"equipo":equipo}
        #question_words_EN = ["pet","movies","school","team"]

        for word in question_words_ES:
            if word in question1:
                input_ans1.send_keys(question_words_ES[word])
            elif word in question2:
                input_ans2.send_keys(question_words_ES[word])
            else:
                pass

        button_login = wait.until(EC.presence_of_element_located((By.ID,"authenticateButton")))
        button_login.click()

    elif autentication_type == 'Call':
        button_call = wait.until(EC.presence_of_element_located((By.ID,"verificationOption1")))
        button_call.click()

    elif autentication_type == 'Message':
        pass

else:
    print("Entró directamente al Jira")


#if current_url != link_jira:
    #driver.get(link_jira)

##Crear un def para lo de abajo (acá ya se hace el incurrido)
button_more = wait.until(EC.presence_of_element_located((By.ID,"opsbar-operations_more")))
button_more.click()

button_logwork = wait.until(EC.presence_of_element_located((By.ID,"log-work")))
button_logwork.click()

input_hours_logged = wait.until(EC.presence_of_element_located((By.ID,"log-work-time-logged")))
input_hours_logged.clear()
input_hours_logged.send_keys(logwork_hours)

input_date_logged = wait.until(EC.presence_of_element_located((By.ID,"log-work-date-logged-date-picker")))
input_date_logged.clear()
input_date_logged.send_keys(fecha_formateada)


formulario = wait.until(EC.presence_of_element_located((By.ID,"log-work")))
text_area = driver.find_elements(By.ID,"comment")

for element in text_area:
    try:
        element.send_keys(content)
    except:
        print("No se pudo escribir en ningún ta")

log_submit_button = wait.until(EC.presence_of_element_located((By.ID,"log-work-submit")))
#log_submit_button.click()

# Mantener la ventana abierta hasta que presiones Enter
input("Presiona Enter para finalizar...")

# Cerrar el navegador al presionar Enter
driver.quit()