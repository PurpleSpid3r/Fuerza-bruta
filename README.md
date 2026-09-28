# Fuerza-bruta

Herramienta de fuerza bruta para formularios de login HTTP, desarrollada en
Python 3. Prueba las contraseñas de una wordlist contra un formulario de
autenticación y detecta el éxito por la **ausencia** del mensaje de error de
login. Pensada para laboratorios como **DVWA** en Metasploitable.

> ⚠️ **Uso autorizado únicamente.** Emplea esta herramienta solo contra
> sistemas de tu propiedad o para los que tengas autorización explícita por
> escrito. El acceso no autorizado a sistemas ajenos es un delito.

## Requisitos

- Python 3.6 o superior
- [`requests`](https://pypi.org/project/requests/)
- [`termcolor`](https://pypi.org/project/termcolor/) (opcional; sin él la
  salida se muestra sin color)

```bash
pip install -r requirements.txt
```

## Uso

Modo con argumentos (recomendado):

```bash
python3 fuerza_bruta.py \
  -u "http://10.0.0.1/dvwa/vulnerabilities/brute/" \
  -U admin \
  -w rockyou.txt \
  -f "Username and/or password incorrect." \
  -X get \
  -C "PHPSESSID=abc123; security=low"
```

Modo interactivo (si no pasas argumentos, los pregunta):

```bash
python3 fuerza_bruta.py
```

## Opciones

| Opción             | Descripción                                             |
|--------------------|---------------------------------------------------------|
| `-u`, `--url`      | URL del formulario de login                             |
| `-U`, `--username` | Usuario a atacar                                        |
| `-w`, `--wordlist` | Archivo de contraseñas (una por línea)                  |
| `-f`, `--fail`     | Texto que la web muestra cuando el login **falla**      |
| `-X`, `--method`   | Método HTTP: `get` o `post` (def. `post`)               |
| `-C`, `--cookies`  | Cookies: `nombre=valor; otra=valor`                     |
| `-t`, `--timeout`  | Timeout por petición en segundos (def. `10.0`)          |

## Nota sobre los campos del formulario

Los nombres de los campos (`username`, `password`, `Login`) dependen de la web
objetivo. Los valores por defecto corresponden a **DVWA**. Si tu objetivo usa
otros nombres, edítalos en la función `brute_force` dentro de
[`fuerza_bruta.py`](fuerza_bruta.py). Puedes identificarlos analizando el
código fuente HTML del formulario.
