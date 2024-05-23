import requests
import sett
import json
import time

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def administrar_chatbot(text,number, messageId, name):
    text = text.lower()#mensaje que envio el usuario
    list = []
    print("mensaje del usuario:", text)

    markRead = markRead_Message(messageId)
    list.append(markRead)
    time.sleep(2)
    
    activador = ["hola", "hello", "buenas","a","1", "menú"]
    footer = "Equipo COFECE"    

    if text in activador:
        body = "¡Hola! Soy COFECEbot asistente de la Comisión Federal de Competencia Económica. Estoy aquí para ayudarte con información y trámites relacionados con la competencia económica. ¿En qué puedo asistirte hoy?"
        options = ["¿Qué hacemos?", "Reporte o Denuncia", "Preguntas Frecuentes"]
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed0",messageId)
        list.append(replyButtonData)
    elif "¿qué hacemos?" in text:
        body = "La COFECE es la entidad en México que vela por la competencia justa y la protección de los consumidores en los mercados económicos. Su objetivo principal es evitar prácticas monopolísticas, fomentar la libre competencia en los mercados y proteger los derechos de los consumidores."
        options = ["¡Quíero conocer más!", "Menú"]

        replyButtonData1 = buttonReply_Message(number, options, body, footer, "sed1",messageId)
        list.append(replyButtonData1)
    elif "¡quíero conocer más!" in text:
        body = "Presiona en este link para saber, ¿Qué hacemos en la Comisión Federal de Competencia Economica (COFECE)? \n https://goo.su/ELJqlE"    
        options = ["Menú"]

        replyButtonData2 = buttonReply_Message(number, options, body, footer, "sed2",messageId)
        list.append(replyButtonData2)
    elif "reporte o denuncia" in text:
        body = "Por favor selecciona una opción :)"
        options = ["Reporte/Denuncia", "Programa inmunidad"]

        replyButtonData3 = buttonReply_Message(number, options, body, footer, "sed3",messageId)
        list.append(replyButtonData3)
    elif "reporte/denuncia" == text:
        body = "La práctica que deseas señalar, habla sobre ¿Compañías telefónicas, internet o redes sociales?"
        options = ["Si","No"]

        replyButtonData4 = buttonReply_Message(number, options, body, footer, "sed4",messageId)
        list.append(replyButtonData4)
    elif "si" == text:
        body = "Tu reporte debe dirigirse al Instituto Federal de Telecomunicaciones 'IFT' aquí te dejamos toda la información de contacto: \n https://goo.su/1LQ4jVV"
        options = ['Menú']

        replyButtonData5 = buttonReply_Message(number, options, body, footer, "sed5",messageId)
        list.append(replyButtonData5)
        ####Comenzar PMA/PMR
    elif "no" == text:
        body = "¿Conoces las diferencias entre PMA y PMR?"
        options = ["Por supuesto que sí", "Aún no"]

        listButtonData6 = buttonReply_Message(number, options, body, footer, "sed6",messageId)
        list.append(listButtonData6)
    elif "aún no" in text: 
        body = "Selecciones una opción :)"
        options = ["¿Qué es una PMA?", "¿Qué es una PMR?"]

        replyButtonData7 = buttonReply_Message(number, options, body, footer, "sed7",messageId)
        list.append(replyButtonData7)

    elif "¿qué es una pma" in text:
        textMessage = text_Message(number, "Puedes ver un video o leer los recursos con los que cuenta la COFECE, aquí tienes :) \n https://goo.su/SMPbE")
        enviar_Mensaje_whatsapp(textMessage)
        
        document = document_Message(number, sett.document_url, "¡Aquí tienes!", "¿Qué es una PMA?.pdf" )
        enviar_Mensaje_whatsapp(document)
        time.sleep(3)
        
        body = "Selecciona una opción:"
        options = ["Menú","¿Qué es una PMR?"]
        replyButtonData8 = buttonReply_Message(number, options, body, footer, "sed8",messageId)
        list.append(replyButtonData8)

    elif "¿qué es una pmr?" in text:
        textMessage = text_Message(number, "Aquí tienes los recursos con los que cuenta la COFECE :)")
        enviar_Mensaje_whatsapp(textMessage)
        
        document1 = document_Message(number, sett.document_url, "¡Aquí tienes!", "¿Qué es una pmr?.pdf" )
        enviar_Mensaje_whatsapp(document1)
        time.sleep(3)
        
        body = "Selecciona una opción:"
        options = ["Menú","¿Qué es una PMA?"]
        replyButtonData9 = buttonReply_Message(number, options, body, footer, "sed9",messageId)
        list.append(replyButtonData9)
        
    elif "por supuesto que sí" in text:
        body ="Selecciona el tipo de práctica que deseas señalar:"
        options = ["PMA", "PMR"]
        
        replyButtonData10 = buttonReply_Message(number, options, body, footer, "sed10",messageId)
        list.append(replyButtonData10)

######## comenzar preguntas PMA
    elif "pma" == text:
        body = "¿Existen acuerdos o contratos entre empresas competidoras para establecer precios de compra o venta de bienes o servicios?"
        options = ["1. Si", "1.a. No"]

        replyButtonData11 = buttonReply_Message(number, options, body, footer, "sed11",messageId)
        list.append(replyButtonData11)
    elif "1.a. no" == text:
        body = "¿Se ha compartido el mercado entre competidores mediante la división de territorios o grupos de clientes?"
        options = ["1. Si", "1.b. No"]

        replyButtonData12 = buttonReply_Message(number, options, body, footer, "sed12",messageId)
        list.append(replyButtonData12)
    elif "1.b. no" == text:
        body = "¿Hubo intercambio de información entre competidores para manipular precios o manipular la oferta?"
        options = ["1. Si", "1.c. No"]

        replyButtonData13 = buttonReply_Message(number, options, body, footer, "sed13",messageId)
        list.append(replyButtonData13)
    elif "1.c. no" == text:
        body = "¿Se ha impuesto la restricción de producir, distribuir o vender solo una cantidad limitada de bienes o servicios?"
        options = ["1. Si", "1.d. No"]

        replyButtonData14 = buttonReply_Message(number, options, body, footer, "sed14",messageId)
        list.append(replyButtonData14)
    elif "1.d. no" == text:
        body = "¿Existe evidencia de coordinación en licitaciones o concursos para fijar precios o condiciones?"
        options = ["1. Si", "1.e. No"]

        replyButtonData15 = buttonReply_Message(number, options, body, footer, "sed15",messageId)
        list.append(replyButtonData15)
    elif "1.e. no" == text:
        body = "Lo sentimos, la práctica que deseas señalar  NO corresponde a una PMA, puedes volver a revisar nuestros materiales y regresar al Menú"
        options = ["Menú","¿Qué es una PMA?","¿Qué es una PMR?"]

        replyButtonData16 = buttonReply_Message(number, options, body, footer, "sed16",messageId)
        list.append(replyButtonData16)
        
########Comenzar Preguntas PMR

    elif "pmr" == text:
        body = "¿Una empresa dominante ha impuesto condiciones exclusivas de comercialización o distribución de bienes o servicios a otros agentes económicos?"
        options = ["1. Si", "2.a. No"]

        replyButtonData17 = buttonReply_Message(number, options, body, footer, "sed17",messageId)
        list.append(replyButtonData17)
    elif "2.a. no" == text:
        body = "¿Una empresa dominante ha impuesto precios o condiciones que los distribuidores o proveedores deben cumplir?"
        options = ["1. Si", "2.b. No"]

        replyButtonData18 = buttonReply_Message(number, options, body, footer, "sed18",messageId)
        list.append(replyButtonData18)
    elif "2.b. no" == text:
        body = "¿Se han ofrecido descuentos o beneficios a cambio de que los compradores no adquieran productos de otros proveedores?" 
        options = ["1. Si", "2.c. No"]

        replyButtonData19 = buttonReply_Message(number, options, body, footer, "sed19",messageId)
        list.append(replyButtonData19)
    elif "2.c. no" == text:
        body = "¿Se ha empleado el poder de mercado para cubrir pérdidas en la venta o prestación de otros productos o servicios?"
        options = ["1. Si", "2.d. No"]

        replyButtonData20 = buttonReply_Message(number, options, body, footer, "sed20",messageId)
        list.append(replyButtonData20)
    elif "2.d. no" == text:
        body = "¿Se ha disminuido el margen entre el precio de acceso a un insumo esencial y el precio del producto o servicio final que depende de ese insumo?"
        options = ["1. Si", "2.e. No"]

        replyButtonData21 = buttonReply_Message(number, options, body, footer, "sed21",messageId)
        list.append(replyButtonData21)
    elif "2.e. no" == text:
        body = "Lo sentimos, la práctica que deseas señalar  NO corresponde a una PMR, puedes volver a revisar nuestros materiales y regresar al Menú"
        options = ["Menú","¿Qué es una PMA?", "¿Qué es una PMR?"]

        replyButtonData22 = buttonReply_Message(number, options, body, footer, "sed22",messageId)
        list.append(replyButtonData22)


        
    ######## Comenzar Proceso Reporte/Denuncia  PMA

    ##REPORTE
    elif "1. si" == text:
        body = "Selecciona una opción:"
        options = ["Reporte","Denuncia","Conoce la diferencia"]

        replyButtonData23 = buttonReply_Message(number, options, body, footer, "sed23",messageId)
        list.append(replyButtonData23)
    elif "reporte" == text:
        reporte = []
        textMessage1 = text_Message(number, "Comenzaremos con el proceso del Reporte o denuncia \n \n Por favor accede al link de abajo para enviar tu reporte, se te solicitara la siguiente información")
        textMessage2 = text_Message(number, "1. Nombre Completo (Si deseas puedes hacerlo de manera anomima, solo coloca 'anónimo') \n \n 2. Correo electrónico \n \n 3. Número de teléfono \n \n 4. Escribe el 'asunto' ej: 'Reporte' + nombre de la empresa o negocio \n \n 5. Descripción de los posibles hechos violatorios de la ley \n \n 6. Adjunta documentos probatorios (No es obligatorio)  \n \n https://forms.office.com/r/Yd8Mby4aQQ")
        
        enviar_Mensaje_whatsapp(textMessage1)
        enviar_Mensaje_whatsapp(textMessage2)
        
        body = "Recuerda, reportar acuerdos ilegales entreempresas es clave para un mercado justo y equitativo. ¡Tú haces la diferencia! #ReportaHoy"
        options = ["Preguntas Frecuentes","Programa Inmunidad", "Menú"]


        replyButtonData24 = buttonReply_Message(number, options, body, footer, "sed24",messageId)
        list.append(replyButtonData24)
    
    ####Denuncia
    
    elif "denuncia" == text:
        textMessage4 = text_Message(number, "Te dejamos un documento con los requerimientos que debe incorporar la denuncia.")
        textMessage5 = text_Message(number, "Recuerda que debes enviarla al correo que te proporcionamos abajo \n denuncias@cofce.mx")
        
        enviar_Mensaje_whatsapp(textMessage4)
        enviar_Mensaje_whatsapp(textMessage5)
        
        document3 = document_Message(number, sett.document_url, "¡Aquí tienes!", "Formato_denuncia.pdf" )
        enviar_Mensaje_whatsapp(document3)
        time.sleep(3)
        
        body = "Recuerda, reportar acuerdos ilegales entreempresas es clave para un mercado justo y equitativo. ¡Tú haces la diferencia! #ReportaHoy"
        options = ["Preguntas Frecuentes","Programa Inmunida", "Menú"]

        replyButtonData27 = buttonReply_Message(number, options, body, footer, "sed27",messageId)
        list.append(replyButtonData27)
        


    ######### Conoce la diferencia
    elif "conoce la diferencia" == text:
        textMessage6 = text_Message(number,"Los reportes no tienen requisitos específicos y se presentan electrónicamente sin acciones legales inmediatas. Si se sospechan infracciones a la LFCE, la Autoridad Investigadora puede iniciar una investigación de oficio.")
        textMessage7 = text_Message(number,"Cualquier persona puede presentar una denuncia por prácticas monopólicas absolutas, prácticas monopólicas relativas o concentraciones ilícitas ante la Autoridad Investigadora, pero las denuncias no pueden ser anónimas.")
        
        enviar_Mensaje_whatsapp(textMessage6)
        enviar_Mensaje_whatsapp(textMessage7)
        
        body = "Selecciona una opción :)"
        options = ["Reporte","Denuncia","Menú"]
        replyButtonData28 = buttonReply_Message(number, options, body, footer, "sed28",messageId)
        list.append(replyButtonData28)
    
    #######Preguntas Frecuentes
    elif "preguntas frecuentes" == text:
        body = "Selecciona una opcion :)"
        options =["Programa Inmunidad","¿Qué es una PMA?","¿Qué es una PMR?"]

        replyButtonData29 = buttonReply_Message(number, options, body, footer, "sed29",messageId)
        list.append(replyButtonData29)
    #######Programa Inmunidad
    elif "programa inmunidad" == text:
        
        textMessage8 = text_Message(number,"Aquí tienes toda la información sobre el programa inmunidad :")
        textMessage9 = text_Message(number,"https://goo.su/gDzNP")
        enviar_Mensaje_whatsapp(textMessage8)
        enviar_Mensaje_whatsapp(textMessage9)
        
        body = "Puedes regresar al Menú si lo deseas."
        options =["Menú"]
        

        replyButtonData30 = buttonReply_Message(number, options, body, footer, "sed30",messageId)
        list.append(replyButtonData30)
        
    else :
        data = text_Message(number,"Lo siento, no entendí lo que dijiste.")
        list.append(data)
    
    for item in list:
        enviar_Mensaje_whatsapp(item)
        list = []
        
#Whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    if s.startswith("521"):
        return "52" + s[3:]
    else:
        return s