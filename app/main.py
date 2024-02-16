from fastapi import FastAPI, BackgroundTasks
import pandas as pd
import yaml

from app.uisp_services.clients import get_clients
from app.uisp_services.devices import get_devices
from app.uisp_services.services import get_services

app = FastAPI(
    title="UISP Analytics API",
    version="0.0.1",
)


def update_data():
    get_clients()
    get_devices()
    get_services()


@app.get("/getBlacklist")
async def get_blacklist(background_tasks: BackgroundTasks):
    # Carga los datos
    with open("./data/services.yaml", "r") as file:
        services = pd.DataFrame(yaml.safe_load(file))
    with open("./data/devices.yaml", "r") as file:
        devices = pd.DataFrame(yaml.safe_load(file))
    
    # Actualiza la informacion en segundo plano
    background_tasks.add_task(update_data)

    # Filtra solo los servicios suspendidos
    services = services[services["status"] == 3]

    # Une los dataframes
    merged = pd.merge(
        services, devices, left_on="unmsClientSiteId", right_on="unms_key", how="left"
    )

    # Crea el dataframe 'blacklist'
    blacklist = merged[merged["ipAddress"].notna()].copy()
    blacklist["ipAddress"] = blacklist["ipAddress"].str.split("/").str[0]
    blacklist = blacklist.drop(["unmsClientSiteId", "unms_key"], axis=1)

    ip_list = blacklist["ipAddress"].tolist()
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
        services = services[services["status"] == 3]

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
        "countMisconfigured": len(service_without_device),
        "misconfigured": service_without_device.to_dict(orient="records"),
        "countDuplicated": len(duplicated),
        "duplicated": duplicated.to_dict(orient="records"),
    }

