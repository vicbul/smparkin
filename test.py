import base64

x = 'AQIDBAUGBwgJCg=='
y = base64.b64encode('esto es una prueba')
print y

print base64.b64decode(x)