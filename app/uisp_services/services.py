import requests
import yaml
import pandas as pd

from app.config import Settings


def guardar_respuesta_en_yaml(respuesta, archivo_salida):
    with open(archivo_salida, "w") as archivo:
        yaml.dump(respuesta, archivo, default_flow_style=False)
    print(f"Respuesta guardada en {archivo_salida}")


def get_services():
    # Consultar el servicio
    headers = {"X-Auth-App-Key": Settings().x_auth_token}
    response = requests.get(
        # f"{Settings().uisp_url}/api/v1.0/clients/services?statuses[]=3",
        f"{Settings().uisp_url}/api/v1.0/clients/services",
        headers=headers,
        verify=False,
    )
    respuesta_servicio: list[dict] = response.json()

    if respuesta_servicio:
        # Guardar la respuesta en un archivo YAML
        archivo_yaml = "./data/services.yaml"
        respuesta = []

        for elemento in respuesta_servicio:
            filter = {
                "clientId": elemento.get("clientId", {}),
                "city": elemento.get("city", {}),
                "name": elemento.get("name", {}),
                "totalPrice": elemento.get("totalPrice", {}),
                "status": elemento.get("status", {}),
                "unmsClientSiteId": elemento.get("unmsClientSiteId", {}),
                "servicePlanId": elemento.get("servicePlanId"),
            }
            respuesta.append(filter)

        guardar_respuesta_en_yaml(respuesta, archivo_yaml)
        return pd.DataFrame(respuesta)
    else:
        raise Exception("No se pudo obtener la respuesta del servicio get services.")
