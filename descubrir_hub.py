import asyncio
from azure.iot.device.aio import ProvisioningDeviceClient

ID_SCOPE = "0ne00FE097D"
DEVICE_ID = "Vacuna-VM-Python"
KEY = "7RFRZtrR5xud+iCXvhsuaNl8azq08X2RKE+Z2KJppFo="

async def main():
    client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host="global.azure-devices-provisioning.net",
        registration_id=DEVICE_ID,
        id_scope=ID_SCOPE,
        symmetric_key=KEY,
        websockets=True
    )
    res = await client.register()
    print("\n" + "="*50)
    print(f"TU HUB ES: {res.registration_state.assigned_hub}")
    print("="*50 + "\n")

asyncio.run(main())
