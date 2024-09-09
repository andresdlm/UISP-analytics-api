import requests
import yaml
import pandas as pd

from app.config import Settings


def guardar_respuesta_en_yaml(respuesta, archivo_salida):
    with open(archivo_salida, "w") as archivo:
        yaml.dump(respuesta, archivo, default_flow_style=False)
    print(f"Respuesta guardada en {archivo_salida}")


def get_devices():
    # Consultar el servicio
    headers = {"x-auth-token": Settings().x_auth_token}
    response = requests.get(
        f"{ Settings().uisp_url}/v2.1/devices", headers=headers, verify=False
    )
    respuesta_servicio: list[dict] = response.json()  # type: ignore

    if respuesta_servicio:
        # Guardar la respuesta en un archivo YAML
        archivo_yaml = "./data/devices.yaml"
        respuesta = []

        for elemento in respuesta_servicio:
            identification: dict = elemento.get("identification", {})

            if identification:
                site: dict = identification.get("site", {})

                if site:
                    filter = {
                        "ipAddress": elemento.get("ipAddress", {}),
                        "unms_key": site.get("id", {}),
                    }
                    respuesta.append(filter)

        guardar_respuesta_en_yaml(respuesta, archivo_yaml)
        return pd.DataFrame(respuesta)
    else:
        raise Exception("No se pudo obtener la respuesta del servicio get devices.")
