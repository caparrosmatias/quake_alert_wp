import feedparser
import segundo
import time
import layer

d = feedparser.parse('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom')
actual = d['entries'][0]['title']

def actualizar():
    d2 = feedparser.parse('http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.atom')
    return d2['entries'][0]['title']

while 1<2:
    nueva = actualizar()
    print("-----")
    print(nueva)
    print(actual)
    print("-----")
    if actual==nueva:
        print("No hay noticias")
    else:
        print("Hay noticias")
        self.toLower(TextMessageProtocolEntity("Hubo un sismo", to=para))
        actual = nueva
    time.sleep(60)
