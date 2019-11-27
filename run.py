#Codigo para utilizar whatsapp desde python
#Detector de sismos para Mendoza y San Juan (Inpres DB)
#Basado en yowsup
#Matias Caparros
from layer import EchoLayer
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup.layers                             import YowParallelLayer
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.stacks import YowStack
from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent
from yowsup import env
import os
#from .stack import YowsupEchoStack

import logging
logging.basicConfig(level=logging.DEBUG)


CREDENTIALS = ("54000000000", "xxxxxxxxxx=") # numero de telefono y clave

if __name__==  "__main__":
    layers = (
            EchoLayer,
            YowParallelLayer([YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer]),
            YowAxolotlLayer,
            YowCoderLayer,
            YowCryptLayer,
            YowStanzaRegulator,
            YowNetworkLayer
        )

    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)         #credenciales
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])    #direccio del server de whatsapp
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)              
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())          #info

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #enviamos el mensaje para conectar

    stack.loop() #loop
