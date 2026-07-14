import asyncio
import main as m

class _Message:
    def __init__(self):
        self.replies=[]
    async def reply_text(self, text, **kwargs):
        self.replies.append(text)

class _Update:
    def __init__(self):
        self.message=_Message()

class _Context:
    args=[]

def test_runtimehealth_s281_no_nameerror_and_two_outputs():
    update=_Update()
    asyncio.run(m.runtimehealth1160ltss28_cmd(update,_Context()))
    assert len(update.message.replies) >= 2
    assert any('RUNTIME HEALTH BAND' in x for x in update.message.replies)
    assert m.V1160_VERSION_MANAGER.number == '116.0-LTS-S2.8.1'

def test_runtimehealth_handler_still_registered():
    assert m.V90_COMMAND_REGISTRY['runtimehealth'] is m.runtimehealth1160ltss28_cmd
    audit=m.v91_preflight(force=True)
    assert audit['ok'], audit.get('failed')
