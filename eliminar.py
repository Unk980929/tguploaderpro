from yarl import URL
from bs4 import BeautifulSoup
import os
import re
import json
import requests

def fname_remove_invalid_chars(fname: str) -> str:
    valores = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-".replace("", "*").split("*")
    fname = fname.replace(" ", "-").replace("_", "-").replace("á", "a").replace("Á", "A").replace("é", "e").replace("É", "E").replace("í", "i").replace("Í", "I").replace("ó", "o").replace("Ó", "O").replace("ú", "u").replace("Ú", "U").replace("Ñ", "-N-").replace("ñ", "-n-").replace("", "*").split("*")
    nombre = []
    for f in fname:
        if f != "":
            nombre.append(f)
    res = [i for i in nombre if i in valores]
    fname = "".join(res)
    if ".mpv" in fname:
        fname = fname.replace(".mpv", ".mkv")
    return fname

def delFile(session, enlace):
        print('eliminando archivo')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        filename = enlace.split('/')[-1]
        itemid = enlace.split('/')[-2]
        print("Eliminando {}...".format(filename))
        response = session.get(server + "/user/files.php", headers=headers)
        resp_1 = response.text
        soup = BeautifulSoup(resp_1,'html.parser')
        query = URL(soup.find('object',attrs={'type':'text/html'})['data']).query
        client_id_pattern = '"client_id":"\w{13}"'
        client_id = re.findall(client_id_pattern, resp_1)
        client_id = re.findall("\w{13}", client_id[0])[0]
        data_delete = {
            'sesskey': query["sesskey"],
            'client_id':client_id,
            'filepath': "/",
            'itemid': itemid,
            'filename': filename
        }
        response = session.post(server + "/repository/draftfiles_ajax.php?action=delete", data=data_delete, headers=headers)
        resp = response.text
        if resp == '{"filepath":"\/"}':
                    return "**{}** 🗑 **__Eliminado__**👍🏻\n".format(filename)
        else:
                    return "❌❌__El archivo {} NO FUE ELIMINADO__❌❌,\n**INTENTELO DE NUEVO**♻️".format(filename)


#inicio sesion en la nube
# yo habia declarado s = requests.Session() por lo que mi sesion es s
# ojo lo que dice server debes cambiarlo seguin creas conveniente y segun hallas programado
session = requests.Session()
file = 'asdñña as ññas´´ 8().001' #este es el nombre del archivo de ejemplo
os.rename(file, fname_remove_invalid_chars(file)) # aqui le cambie el nombre
file = fname_remove_invalid_chars(file) #sustitullo el nuevo nombre en la variable

enlace = file_upload(session, file) #subi el archivo a la nube y guardo el enlace
print(enlace)
respuesta = delFile(session, enlace) #elimino el archivo mediante el enlace
print(respuesta)

'''este es el log del proceso completo
(en este script no esta como subir ni iniciar sesion pues no es ese el fin del mismo)
iniciando Sesion
Session iniciada
subiendo archivo
https://server/draftfile.php/444379/user/draft/5123123/asd-n--n-a-as--n--n-as-8.001
eliminando archivo
Eliminando asd-n--n-a-as--n--n-as-8.001...
**asd-n--n-a-as--n--n-as-8.001** 🗑 **__Eliminado__**👍🏻
'''