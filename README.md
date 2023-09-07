# RPA-JIRA
##Robot (RPA) para automatizar incurridos en el entorno JIRA para el entorno Laboral de NTTData.
###INSTRUCCIONES
El archivo Config.json se usará para configurar el robot antes de ser ejecutado.
A continuación se proporciona un ejemplo de cómo completar el archivo .json

    {                                               
1.      "Navegador":"",                                                                 --> No se usa, siempre se usará Chrome
2.      "Autentication_Type":"Answers",                                                 --> Tipo de autenticación puede ser ["Answers","Call","Message"], se detalla en el punto 2
3.      "Link_Jira": "https://umane.emseal.nttdata.com/jiraito/browse/DXRPA-1835",      --> Link directo a la tarea donde se incurrirá
4.      "User_Short": "afloresc",                                                       --> Tu usuario corto
5.      "Password": "K1$vs25",                                                          --> Contraseña de tu cuenta
6.      "Answers":                                                                      --> Acá no se escribe nada, son respuestas de las preguntas de seguridad (debajo)
            {
    6.1          "mascota": "Firulays",                                                 --> Respuesta a la pregunta "¿Cuál es tu nombre de mascota preferido?"
    6.2          "equipo": "SKT Telekom",                                               --> Respuesta a la pregunta "¿Cuál es tu equipo preferido?"
    6.3          "pelicula": "Transformers",                                            --> Respuesta a la pregunta "¿Cuál es tu película favorita?"
    6.4          "colegio": "Fleming"                                                   --> Respuesta a la pregunta "¿Cuál es el nombre de tu colegio?"
            }
        ,
7.      "Logwork_hours":"9h",                                                           --> Horas incurridas, se detalla en el punto 7
8.      "Logwork_date_hour": "04/sep/23 09:00 AM"                                       --> Se detalla debajo en el punto 8
    }

##################################################################################################################################

2. Autentication_Type --- Tipo de autenticación
"Answers"   -> Para verificación por Preguntas de seguridad
"Call"      -> Para verificación por llamada #
"Message"   -> Para ingresar código enviado por mensaje de texto
Recomendado: "Answers"

7. Logwork_hour --- Horas Trabajadas
formato: "Xh" -> X son las horas
ejemplo: "9h"

8. Logwork_date_hour --- Fecha y hora en la que se incurre
formato: "dd/mmm/yy hh:mm XX" -> "dd" día / "mmm" mes / "yy" año / "hh" hora / "mm" minutos / XX AM o PM
ejemplo: "04/sep/23 7:14 AM"

NOTA: Si se deja vacío (""), tomará la fecha actual y la hora se establecerá como: "09:00 AM"
 
#meses aceptados:
mes = "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"