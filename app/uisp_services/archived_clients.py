import requests
import yaml
import pandas as pd

from app.config import Settings


def guardar_respuesta_en_yaml(respuesta, archivo_salida):
    with open(archivo_salida, "w") as archivo:
        yaml.dump(respuesta, archivo, default_flow_style=False)
    print(f"Respuesta guardada en {archivo_salida}")


def get_archived_clients():
    # Consultar el servicio
    headers = {"X-Auth-App-Key": Settings().x_auth_token}
    response = requests.get(
        f"{Settings().uisp_url}/api/v1.0/clients?isArchived=1",
        headers=headers,
        verify=False,
    )
    respuesta_servicio: list[dict] = response.json()

    if respuesta_servicio:
        # Guardar la respuesta en un archivo YAML
        archivo_yaml = "./data/archived_clients.yaml"
        respuesta = []

        for elemento in respuesta_servicio:
            filter = {
                "id": elemento.get("id", {}),
                "clientType": elemento.get("clientType", {}),
                "companyName": elemento.get("companyName", {}),
                "city": elemento.get("city", {}),
                "note": elemento.get("note", {}),
                "organizationId": elemento.get("organizationId", {}),
                "firstName": elemento.get("firstName", {}),
                "lastName": elemento.get("lastName", {}),
                "accountBalance": elemento.get("accountBalance", {}),
                "accountCredit": elemento.get("accountCredit", {}),
                "accountOutstanding": elemento.get("accountOutstanding", {}),
                "contacts": elemento.get("contacts", {}),
                "tags": elemento.get("tags", {}),
                "isArchived": elemento.get("isArchived", {}),
            }
            respuesta.append(filter)

        guardar_respuesta_en_yaml(respuesta, archivo_yaml)
        return pd.DataFrame(respuesta)
    else:
        raise Exception("No se pudo obtener la respuesta del servicio get clients.")
