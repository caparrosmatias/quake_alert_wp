# -*- coding: utf-8 -*-

import MySQLdb
import os

from yowsup.layers import YowLayer
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity

bd = MySQLdb.connect("server_db","user_db","clave_db","nombre_db")
cursor = bd.cursor()

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        nombre = messageProtocolEntity.getNotify()
        mensaje = messageProtocolEntity.getBody()
        para = messageProtocolEntity.getFrom()
	numero = messageProtocolEntity.getFrom(False)
	
	print("------------")
        print(nombre)
        print(mensaje)
	print(para)
        print(numero)
        print("...")
		
	sql = "SELECT * FROM  `temblor` WHERE  `NUMERO` = " + str(numero)
		
	try:
		#Esto va a suceder si el numero esta en la DB
		cursor.execute(sql)
		resultado = cursor.fetchall()
		for res in resultado:
			ID = res[0]
			NUMERO = res[1]
			ACTIVO = res[2]
		print("Numero existente")
		print("------------")
		#self.toLower(TextMessageProtocolEntity("Tu numero esta en la DB", to=para))

		if int(ACTIVO) == 1: #Si ACTIVO = 1
			if 'BAJA' in mensaje:
				#Coloco ACTIVO = 0
				sql = "UPDATE `temblor` SET `ACTIVO` = 0 WHERE `NUMERO` = " + str(numero)
				try:
					cursor.execute(sql)
					bd.commit()
					self.toLower(TextMessageProtocolEntity("Tu numero fue dado de baja", to=para))
				except:
					bd.rollback()
			else:
				self.toLower(TextMessageProtocolEntity("No comprendo tu comando", to=para))
				self.toLower(TextMessageProtocolEntity("Escribi BAJA para cancelar el servicio", to=para))
				#Escribo No comprendo el comando
		elif 'AYUDA' in mensaje:
			self.toLower(TextMessageProtocolEntity("Este es un servicio experimental de notificaciones via Whatsapp. Para darte de baja escribe BAJA.", to=para))
			self.toLower(TextMessageProtocolEntity("Porfavor agrega este numero a tu lista de contactos para evitar bloqueos por parte de los servidores de WhatsApp.", to=para))
			self.toLower(TextMessageProtocolEntity("Muchas gracias por utilizar este servicio.", to=para))
		else:
			if 'ALTA' in mensaje:
				sql = "UPDATE `temblor` SET `ACTIVO` = 1 WHERE `NUMERO` = " + str(numero)
				try:
					cursor.execute(sql)
					bd.commit()
					self.toLower(TextMessageProtocolEntity("Bienvenido nuevamente al sistema", to=para))
				except:
					bd.rollback()
			else:
				self.toLower(TextMessageProtocolEntity("No comprendo tu comando", to=para))
				self.toLower(TextMessageProtocolEntity("Escribi ALTA para iniciar el servicio", to=para))
	except:
		#Esto va a suceder si el numero no esta en la DB
		print("Numero no existente")
		print("------------")
		#self.toLower(TextMessageProtocolEntity("Tu numero NO esta en la DB", to=para))
		self.toLower(TextMessageProtocolEntity("Bienvenido " + nombre + ". Para darte de alta escribi ALTA", to=para))
		
		if 'ALTA' in mensaje:
			sql = "SELECT * FROM  `temblor` WHERE  `ID` = (SELECT MAX(ID) from temblor)"
			
			try:
				cursor.execute(sql)
				busqueda = cursor.fetchall()
				for busq in busqueda:
					ID = int(busq[0])+1
				sql = "INSERT INTO `matias`.`temblor` (`ID`, `NUMERO`, `ACTIVO`) VALUES ('"+str(ID)+"', '"+str(numero)+"', '1')"
			
				try:
					cursor.execute(sql)
					bd.commit()
					self.toLower(TextMessageProtocolEntity("Fuiste dado de alta, ¡Felicitaciones!", to=para))
					self.toLower(TextMessageProtocolEntity("Porfavor, agrega este numero a tu lista de contactos", to=para))
					self.toLower(TextMessageProtocolEntity("Para mas informacion escribi AYUDA", to=para))
					self.toLower(TextMessageProtocolEntity("Para cancelar el servicio envia BAJA", to=para))
				except:
					bd.rollback()

			except:
				print("error")


		
		else:
			self.toLower(TextMessageProtocolEntity("No comprendo tu comando.", to=para))
			self.toLower(TextMessageProtocolEntity("Escribi ALTA para iniciar el servicio", to=para))
			

