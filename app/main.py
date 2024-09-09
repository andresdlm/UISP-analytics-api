from fastapi import FastAPI, Response
import pandas as pd
import yaml

from app.uisp_services.clients import get_clients
from app.uisp_services.devices import get_devices
from app.uisp_services.services import get_services
from app.uisp_services.archived_clients import get_archived_clients

app = FastAPI(
    title="UISP Analytics API",
    version="0.0.1",
)


def update_data():
    clients = get_clients()
    devices = get_devices()
    services = get_services()
    archived_clients = get_archived_clients()
    return clients, devices, services, archived_clients


@app.get("/getBlacklist")
async def get_blacklist():
    # Carga los datos
    clients, devices, services, archived_clients = update_data()

    # Concatenar clientes + archivados
    clients = pd.concat([clients, archived_clients], ignore_index=True)

    # Une los dataframes
    merged = pd.merge(
        services, devices, left_on="unmsClientSiteId", right_on="unms_key", how="left"
    )
    merged = pd.merge(merged, clients, left_on="clientId", right_on="id", how="left")
    merged = merged[merged["ipAddress"].notna()]
    merged["ipAddress"] = merged["ipAddress"].str.split("/").str[0]
    merged = merged.drop_duplicates(subset="ipAddress", keep="first")
    merged = merged.drop(
        ["unmsClientSiteId", "unms_key", "id", "city_x", "city_y", "note", "firstName", "lastName", "companyName", "name", "contacts"],
        axis=1,
    )

    # Crea el dataframe 'blacklist'
    blacklist = merged

    # Filtra los servicios activos
    blacklist = blacklist[blacklist["status"] != 1]

    ip_list = blacklist.sort_values(by=["clientId"])["ipAddress"].to_list()

    return {
        "count": len(ip_list),
        "blacklist": ip_list,
    }


@app.get("/getServicesMisconfigured")
async def get_services_misconfigured(suspended: bool = True):
    with open("./data/services.yaml", "r") as file:
        services = pd.DataFrame(yaml.safe_load(file))
    with open("./data/devices.yaml", "r") as file:
        devices = pd.DataFrame(yaml.safe_load(file))

    # Filtra solo los servicios suspendidos
    if suspended:
        services = services[services["status"] != 1]

    # Une servicios con dispositivos
    merged = pd.merge(
        services, devices, left_on="unmsClientSiteId", right_on="unms_key", how="left"
    )

    # Crea el dataframe 'blacklist'
    blacklist = merged[merged["ipAddress"].notna()].copy()
    blacklist["ipAddress"] = blacklist["ipAddress"].str.split("/").str[0]
    blacklist = blacklist.drop(["unmsClientSiteId", "unms_key"], axis=1)

    # Crea el dataframe 'duplicated'
    duplicated = blacklist[blacklist.duplicated("ipAddress", keep=False)]

    # Crea el dataframe 'service_without_device'
    service_without_device = merged[merged["unms_key"].isna()].copy()
    service_without_device = service_without_device.drop(
        ["ipAddress", "unms_key"], axis=1
    )

    return {
        "totalNoIncome": service_without_device["totalPrice"].sum(), 
        "countMisconfigured": len(service_without_device),
        "misconfigured": service_without_device.to_dict(orient="records"),
        "countDuplicated": len(duplicated),
        "duplicated": duplicated.to_dict(orient="records"),
    }


@app.get("/getClientsByService")
async def get_clients_by_service(service_id: int = 0):
    # Define las variables
    with open("./data/services.yaml", "r") as file:
        services = pd.DataFrame(yaml.safe_load(file))
    with open("./data/clients.yaml", "r") as file:
        clients = pd.DataFrame(yaml.safe_load(file))

    # Eliminar columnas no necesarias en el DataFrame de clientes
    clients = clients.drop(["contacts", "tags"], axis=1)

    # Eliminar columnas no necesarias en el DataFrame de servicios
    services = services.drop(["unmsClientSiteId", "city"], axis=1)
    services.rename(columns={"name": "servicePlan"}, inplace=True)
    services["totalPrice"] = services["totalPrice"].round(2)

    # Filtrar servicios por ID si se proporciona un ID específico
    if service_id != 0:
        services = services[services["servicePlanId"] == service_id]

    # Unir DataFrames de servicios y clientes
    merged = pd.merge(services, clients, left_on="clientId", right_on="id", how="left")
    merged = merged.drop(["id"], axis=1)

    # Convertir el DataFrame a formato CSV
    csv_data = merged.to_csv(index=False)

    # Definir la respuesta como un archivo CSV adjunto
    response = Response(content=csv_data, media_type="text/csv")
    response.headers["Content-Disposition"] = (
        "attachment; filename=services_by_client.csv"
    )

    return response
