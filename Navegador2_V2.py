from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from tkinter import messagebox
from tkinter import simpledialog

import re
import time
import sys

import tkinter as tk
import json

#================================================================
#RAMA PRUEBAS_V3 --
#Si no harás un merge, cambia a la rama de pruebas.
#=================================================================
#Patrones y configuraciones
autentication_type_conf = ["Answers","Call","Message"]
link_jira_patron = "https://umane.emeal.nttdata.com/jiraito/browse"
user_short_patron = r"\b[a-z]+$"
logwork_hours_patron = r"\d{1,2}h"
logwork_date_hour_patron = r"\b\d{2}/[a-z]{3}/\d{2} \d{1,2}:\d{1,2} [A,P]M\b" #04/sep/23 7:14 AM
#=================================================================
#Archivo JSON
with open("ConfigPersonal.json","r") as archivo:
    config = json.load(archivo)

navegador = config["Navegador"]
authentication_type = config["Autentication_Type"]
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

##REVISIÓN DE CONFIGURACIÓN
authentication_type_is_correct = True if link_jira_patron in link_jira else False
user_short_intication_type_is_correct = True if authentication_type in autentication_type_conf else False
link_jiras_correct = True if re.search(user_short_patron,user_short) else False
logwork_hours_is_correct = True if re.search(logwork_hours_patron,logwork_hours) else False  
logwork_date_hours_is_correct = True if logwork_date_hour == "" else (True if re.search(logwork_date_hour_patron,logwork_date_hour) else False)

err_msg_array = ["Error en Auth Config","Error en Short User","Error en Link","Error en logwork hours","Error en logwork hours date"]
err_array = [authentication_type_is_correct,user_short_intication_type_is_correct,link_jiras_correct,logwork_hours_is_correct,logwork_date_hours_is_correct]


def create_err_msg(err_array,err_msg_array):
    str_err = ""
    for i,err_bool in enumerate(err_array):
        if not err_bool:
            str_err += f"{err_msg_array[i]}\n"
    #print(str_err)

    if str_err != "":
        messagebox.showerror("Error",str_err)
        sys.exit()        

create_err_msg(err_array,err_msg_array)

#=================================================================
def destruir():
    sys.exit()
#=================================================================

#Cuadro emergente - descripción del trabajo
ventana = tk.Tk()
ventana.title("Campo de Texto Pop-up")

ventana.protocol("WM_DELETE_WINDOW", destruir)

def save_text():
    global content 
    content = campo_texto.get("1.0", "end-1c")
    ventana.destroy()
    #destruir()

campo_texto = tk.Text(ventana, height=10, width=40)
campo_texto.pack(expand=True,fill="both")
#campo_texto.grid(row=0,column=0,columnspan=2,sticky="ewns")

f = tk.Frame(master=ventana,height=10)
f.pack(expand=True,fill="both")

btn_save = tk.Button(f,text="Aceptar",command=save_text)
btn_save.pack(side="left",expand=True,fill="both")
#btn_save.grid(row=0,column=0,sticky="ewsn")

btn_cancel = tk.Button(f,text="Cancelar",command=destruir)
btn_cancel.pack(side="right",expand=True,fill="both")
#btn_cancel.grid(row=0,column=1,sticky="ewsn")

content = "Hola desde el script"

# Iniciar el bucle principal de la interfaz gráfica
ventana.mainloop()
#=================================================================

#Meses dict
meses = {"01":"ene","02":"feb","03":"mar","04":"abr","05":"may","06":"jun",
         "07":"jul","08":"ago","09":"sep","10":"oct","11":"nov","12":"dic"}

# Obtener la fecha y hora actual
fecha_actual = datetime.now()
formato = "%d/%m/%y"
dia,mes,año = fecha_actual.strftime(formato).split("/")

if logwork_date_hour == "":
    fecha_formateada = f"{dia}/{meses[mes]}/{año} 09:00 AM"
else:
    fecha_formateada = logwork_date_hour

opciones = webdriver.ChromeOptions()
#opciones.add_argument("--headless")
driver = webdriver.Chrome(options=opciones)

# Abrir el sitio web del Jira
driver.get(link_jira)
time.sleep(3)
# Get the current URL.
current_url = driver.current_url

wait = WebDriverWait(driver,10)

#Posibles respuestas al link
# 1. Ingreso deirecto
# 2. Colocando el correo completo
# 3. Colocando el usuario corto2
#============================#============================#============================#        
def crear_html_input_element(id,keys):
    input_name = wait.until(EC.presence_of_element_located((By.ID,id)))
    input_name.clear()
    input_name.send_keys(keys)

#==========================="=#============================#============================#
def login_by_credentials():
    credentials_error = False
    for i in range(2):
        crear_html_input_element("userNameInput",f"{user_short}@emeal.nttdata.com")
        crear_html_input_element("passwordInput",password)

        button_submit = wait.until(EC.presence_of_element_located((By.ID,"submitButton")))
        button_submit.click()

        time.sleep(1)

        try:
            lbl_err_msg_crd = wait.until(EC.presence_of_element_located((By.ID,"error")))
            if lbl_err_msg_crd.is_displayed():
                credentials_error = True
            else:
                credentials_error = False
                choose_verification()
                break
        except Exception as error:
                #print(error,"1")
                credentials_error = False
                choose_verification()
                break

    #Crear un pop up donde termine el programa indicando el programa.
    if credentials_error: messagebox.showerror("Error","Credenciales incorrectas.")
#============================#============================#============================#

def choose_verification():
    if autentication_type != "Message":
        button_change_parameters = wait.until(EC.presence_of_element_located((By.ID,"differentVerificationOption")))
        button_change_parameters.click()
        #Tipo de autenticación
        button_questions = wait.until(EC.presence_of_element_located((By.ID,"verificationOption2")))
        button_questions.click()
        answers_error = False
        if autentication_type =='Answers':
            for i in range(3):            

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

                try:
                    lbl_err_msg_ans = wait.until(EC.presence_of_element_located((By.ID,"errorDiv")))
                    if lbl_err_msg_ans.is_displayed():
                        answers_error = True
                    else:
                        answers_error = False
                        incur_process()
                        break
                except Exception as error:
                        print(error,"2")
                        answers_error = False
                        incur_process()
                        break

            if answers_error:messagebox.showerror("Error","Las respuestas no coinciden.")
            # Try Except para determinar el error - si existe ... 
            # Retry answer authentication 2 veces más
            # Si no funciona, pop up de error & finish

        elif autentication_type == 'Call':
            call_error = False
            for i in  range(2):
                button_call = wait.until(EC.presence_of_element_located((By.ID,"verificationOption1")))
                button_call.click()

                try:
                    lbl_err_msg_call = wait.until(EC.presence_of_element_located((By.ID,"errorDiv")))
                    if lbl_err_msg_call.is_displayed():
                        call_error = True
                        button_change_parameters = wait.until(EC.presence_of_element_located((By.ID,"differentVerificationOption")))
                        button_change_parameters.click()
                    else:
                        call_error = False
                        incur_process()
                        break
                except Exception as error:
                        #print(error,"3")
                        call_error = False
                        incur_process()
                        break
                
            if call_error: messagebox.showerror("Error","Las llamadas no han sido contestadas o no se ha marcado el símobolo '#'")

    else:           #AUTENTICATION TYPE = MESSAGE
        msg_error = False
        for _ in range(3):
            input_code_message = wait.until(EC.presence_of_element_located((By.ID,"oneTimePasscodeInput")))
            resultado = simpledialog.askstring("Código", "Ingresa el código del mensaje:")
            input_code_message.send_keys(resultado)
            button_login = wait.until(EC.presence_of_element_located((By.ID,"authenticateButton")))
            time.sleep(1)
            button_login.click()
            #ACÁ ESTÁ MAL 
            try:
                lbl_err_msg_msg = wait.until(EC.presence_of_element_located((By.ID,"errorDiv")))
                if lbl_err_msg_msg.is_displayed():
                    msg_error = True
                else:
                    incur_process()
                    msg_error = False
                    break
            except Exception as error:
                #print(error,"4")
                incur_process()
                msg_error = False
                break
        
        if msg_error: messagebox.showerror("Error","Los códigos ingresados no son correctos")

    time.sleep(1)

#============================#============================#============================#

def incur_process():
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

    text_area = driver.find_elements(By.ID,"comment")

    for index,element in enumerate(text_area):
        try:
            element.send_keys(content)
        except Exception as error:
            #print(error,"5")
            print(index)

    log_submit_button = wait.until(EC.presence_of_element_located((By.ID,"log-work-submit")))
    #log_submit_button.click()

#=======================================================================================


if current_url != link_jira:
    
    #True: Ingresó directamente pero mandó a la página de error
    #False: Ingresó a página de credenciales -> VPN - No VPN
    if "fail" in current_url: 
        time.sleep(1)
        #Redireccionar al link principal
        driver.get(link_jira) #Debería llevar a la página de la tarea
    else: #Si no está en la página fail, quiere decir que ha redireccionado a una de las páginas de login 
        try:
            login_by_credentials()
        except Exception as error:
            #(error,"6")
            login_error = False
            for i in range(3):
                #Si están mal las credenciales, vuelve a pedirlas
                new_url = f"{current_url[0:8]}{user_short}:{password}@{current_url[8:]}"
                time.sleep(1)
                if driver.current_url != link_jira:
                    if "fail" in driver.current_url:
                        msg_error = False
                        driver.get(link_jira)
                        break
                    else:
                        msg_error = True
                        driver.get(new_url)   
                else:
                    msg_error = False
                    incur_process() 
            if msg_error: messagebox.showerror("Error","Credenciales incorrectas 2")

else:
    incur_process()

# Mantener la ventana abierta hasta que presiones Enter
input("Presiona Enter para finalizar...")

driver.quit()