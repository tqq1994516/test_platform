import asyncio
from srf.mq_ext.pulsar_plugin import pulsar_consumer
from srf.nacos_ext.nacos_plugin import nacos_client


# @boost('persistent://test_used/ui_test/exec', broker_kind=BROKER_KIND_PULSAR, qps=0.1, concurrent_num=1)
# def exec_test(action):
#     print(f'action={action}')

async def nacos_beat(
    serviceName: str,
    beat: dict,
    groupName: str = None,
    ephemeral: bool = None
):
    while True:
        nacos_client.send_beat(serviceName, beat, groupName, ephemeral)
        await asyncio.sleep(5)
