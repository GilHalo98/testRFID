# -*- coding: utf-8 -*-

import time
import random
import socketio
import multiprocessing
import requests

def identificarse(id, args):
    print('Identificando dispositivo ' + id)

def iniciarCliente(dispositivo: dict, tokenAuth: str) -> None:
    request = requests.get(
        'http://127.0.0.1:3001/apiV0.1.0/dispositivo/generar/token?id={}'.format(
            dispositivo['id']
        ),
        headers={
            'authorization': tokenAuth
        }
    )

    respuesta = request.json()

    dispositivo['token'] = respuesta['authorization']

    cliente = socketio.Client()

    cliente.on(
        'toggle_identificarse',
        lambda args: identificarse(str(dispositivo['id']), args)
    )

    tipo = dispositivo['idTipoDispositivoVinculado']
    id = dispositivo['id']

    if(tipo == 1) :
        checador(dispositivo, cliente)

    elif(tipo == 2):
        if(id == 9):
            lector_entrada_retrete(dispositivo, cliente)

        elif(id == 10):
            lector_salida_retrete(dispositivo, cliente)

        else:
            lector(dispositivo, cliente)

    elif(tipo == 3):
        controlador(dispositivo, cliente)

    elif(tipo == 4):
        controlador_puerta(dispositivo, cliente)

def checador(dispositivo: dict, cliente):
    cliente.connect('http://127.0.0.1:3001', namespaces=['/'], headers={
        'Authorization': dispositivo['token']
    })

    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 1})
    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 2})

    while True:
        if(random.random() < 0.2):
            cliente.emit('reportar_status', {'status': 8})

            time.sleep(2)
            cliente.emit('reportar_status', {'status': 2})

        time.sleep(10)

def lector(dispositivo: dict, cliente):
    cliente.connect('http://127.0.0.1:3001', namespaces=['/'], headers={
        'Authorization': dispositivo['token']
    })

    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 1})
    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 2})

    while True:
        if(random.random() < 0.2):
            cliente.emit('reportar_status', {'status': 8})

            if(random.random() < 0.1):
                cliente.emit('peticion_acceso', {
                    'resolucion': True
                })
            else:
                cliente.emit('peticion_acceso', {
                    'resolucion': False
                })

            time.sleep(2)
            cliente.emit('reportar_status', {'status': 2})

        time.sleep(10)

def lector_entrada_retrete(dispositivo: dict, cliente):
    cliente.connect('http://127.0.0.1:3001', namespaces=['/'], headers={
        'Authorization': dispositivo['token']
    })

    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 1})
    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 2})

    while True:
        if(random.random() < 0.2):
            cliente.emit('reportar_status', {'status': 8})

            cliente.emit('peticion_acceso_bloquear', {
                'resolucion': True
            })

            time.sleep(2)
            cliente.emit('reportar_status', {'status': 2})

        time.sleep(10)

def lector_salida_retrete(dispositivo: dict, cliente):
    cliente.connect('http://127.0.0.1:3001', namespaces=['/'], headers={
        'Authorization': dispositivo['token']
    })

    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 1})
    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 2})

    while True:
        if(random.random() < 0.2):
            cliente.emit('reportar_status', {'status': 8})

            cliente.emit('peticion_acceso_desbloquear', {
                'resolucion': True
            })

            time.sleep(2)
            cliente.emit('reportar_status', {'status': 2})

        time.sleep(10)

def controlador(dispositivo: dict, cliente):
    cliente.connect('http://127.0.0.1:3001', namespaces=['/'], headers={
        'Authorization': dispositivo['token']
    })

    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 1})
    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 2})

    cliente.on(
        'activar',
        lambda args: cliente.emit('reportar_status', {'status': 8})
    )

    cliente.on(
        'desactivar',
        lambda args: cliente.emit('reportar_status', {'status': 2})
    )

    while True:
        if(random.random() < 0.2):
            cliente.emit('reportar_status', {'status': 8})

            time.sleep(random.randint(1, 60))

            cliente.emit('reportar_status', {'status': 2})

        time.sleep(10)

def controlador_puerta(dispositivo: dict, cliente):
    cliente.connect('http://127.0.0.1:3001', namespaces=['/'], headers={
        'Authorization': dispositivo['token']
    })

    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 1})
    time.sleep(random.randint(0, 10))
    cliente.emit('reportar_status', {'status': 2})

    cliente.on(
        'bloquear_puerta',
        lambda args: cliente.emit('reportar_status', {'status': 16})
    )

    cliente.on(
        'desbloquear_puerta',
        lambda args: cliente.emit('reportar_status', {'status': 2})
    )

    def secuencia_abrir_puerta(args):
        cliente.emit('reportar_status', {'status': 8})
        time.sleep(4)
        cliente.emit('reportar_status', {'status': 2})

    def secuencia_cerrar_puerta(args):
        cliente.emit('reportar_status', {'status': 8})
        time.sleep(4)
        cliente.emit('reportar_status', {'status': 2})

    def secuencia_abrir_cerrar_puerta(args):
        print('Acceso garantizado')
        cliente.emit('reportar_status', {'status': 8})
        time.sleep(8)
        cliente.emit('reportar_status', {'status': 2})
            
    def secuencia_abrir_cerrar_puerta_bloquear_desbloquear(args, bloquear_puerta):
        print('Acceso garantizado')

        if(bloquear_puerta):
            print('Bloqueando puerta')
            cliente.emit('reportar_status', {'status': 8})
            time.sleep(8)
            cliente.emit('reportar_status', {'status': 16})

        else:
            print('Desbloqueando puerta')
            cliente.emit('reportar_status', {'status': 8})
            time.sleep(8)
            cliente.emit('reportar_status', {'status': 2})

    cliente.on(
        'abrir_puerta',
        lambda args: secuencia_abrir_puerta(args)
    )

    cliente.on(
        'cerrar_puerta',
        lambda args: secuencia_cerrar_puerta(args)
    )

    cliente.on(
        'garantizar_acceso',
        lambda args: secuencia_abrir_cerrar_puerta(args)
    )

    cliente.on(
        'negar_acceso_desbloquear',
        lambda args: secuencia_abrir_cerrar_puerta_bloquear_desbloquear(args, False)
    )

    cliente.on(
        'garantizar_acceso_bloquear',
        lambda args: secuencia_abrir_cerrar_puerta_bloquear_desbloquear(args, True)
    )

    cliente.on(
        'negar_acceso',
        lambda args: print('Acceso negado')
    )

    while True:
        time.sleep(1000)

def main() -> None:
    request = requests.post(
        'http://127.0.0.1:3001/apiV0.1.0/usuario/login',
        data={
            'nombreUsuario': 'admon',
            'password': 'admin'
        }
    )

    respuesta = request.json()

    request = requests.get(
        'http://127.0.0.1:3001/apiV0.1.0/dispositivo/consultar',
        headers={
            'authorization': respuesta['authorization']
        }
    )

    dispositivos = request.json()['registros']

    for dispositivo in dispositivos:
        proceso = multiprocessing.Process(
            target=iniciarCliente,
            args=(dispositivo, respuesta['authorization']),
            daemon=True
        )
        proceso.start()

    while True:
        time.sleep(1000)

if __name__ == '__main__':
    main()
