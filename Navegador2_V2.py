from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

import threading
import tkinter as tk
import json

#=================================================================
#Archivo JSON
with open("Config.json","r") as archivo:
    config = json.load(archivo) 

navegador = config["Navegador"]
autentication_type = config["Autentication_Type"]
link_jira = config["Link_Jira"]
email = config["Email"]
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

# Get the current URL.
current_url = driver.current_url

# If the current URL is not the expected URL
if current_url != link_jira:

    wait = WebDriverWait(driver,15)

    input_name = wait.until(EC.presence_of_element_located((By.NAME,"UserName")))
    input_name.send_keys(email)

    input_password = wait.until(EC.presence_of_element_located((By.NAME,"Password")))
    input_password.send_keys(password)

    button_submit = wait.until(EC.presence_of_element_located((By.ID,"submitButton")))
    button_submit.click()


    button_change_parameters = wait.until(EC.presence_of_element_located((By.ID,"differentVerificationOption")))
    button_change_parameters.click()

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

else:
    print("Entró directamente al Jira")

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

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.ID, "comment"))
)  # Wait until the `text_to_score` element appear (up to 5 seconds)
driver.find_element(By.ID,"comment").clear()
driver.find_element(By.ID,'comment').send_keys("text")

#print(content)
#input_comment = wait.until(EC.element_to_be_clickable((By.ID, "comment")))
#input_comment.click()
#driver.execute_script("arguments[0].value = arguments[1]",input_comment,content)
#input_comment.clear()
#input_comment.send_keys(content)

# Mantener la ventana abierta hasta que presiones Enter
input("Presiona Enter para finalizar...")

# Cerrar el navegador al presionar Enter
driver.quit()
