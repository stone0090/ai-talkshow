import pyvts
import asyncio

async def connect_auth(myvts):
    await myvts.connect()
    await myvts.request_authenticate_token()
    await myvts.request_authenticate()
    await myvts.close()

async def trigger(myvts):
    await myvts.connect()
    await myvts.request_authenticate()
    # response_data = await myvts.request(myvts.vts_request.BaseRequest("Live2DParameterListRequest"))
    # response_data = await myvts.request(myvts.vts_request.BaseRequest("InputParameterListRequest"))
    # data = {"name": "VoiceVolumePlusMouthOpen"}
    # response_data = await myvts.request(myvts.vts_request.BaseRequest("ParameterValueRequest", data))
    response_data = await myvts.request(myvts.vts_request.requestParameterValue("VoiceVolumePlusMouthOpen"))
    print(response_data)
    await myvts.request(myvts.vts_request.requestSetParameterValue("VoiceVolumePlusMouthOpen", 0.8))
    # hotkey_list = []
    # for hotkey in response_data["data"]["availableHotkeys"]:
    #     hotkey_list.append(hotkey["name"])
    # send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[0])
    # await myvts.request(send_hotkey_request)  # send request to play 'My Animation 1'
    await myvts.close()

if __name__ == "__main__":
    myvts = pyvts.vts()
    asyncio.run(connect_auth(myvts))
    asyncio.run(trigger(myvts))