import asyncio
import main

class Msg:
    def __init__(self): self.texts=[]
    async def reply_text(self,text,**kwargs): self.texts.append((text,kwargs)); return text
class Update:
    def __init__(self): self.effective_message=Msg(); self.message=self.effective_message
class Ctx:
    args=[]

def test_version_and_freeze():
    assert main.V1160_VERSION_MANAGER.number=='116.0-RC4.9.25'
    a=main.v91_preflight(force=True)
    assert a['ok'], a['failed']
    assert a['regression_risk']=='NONE'
    assert len(main.V90_COMMAND_REGISTRY)==341

def test_status_has_no_html_tags():
    u=Update(); asyncio.run(main.status1160rc4925_cmd(u,Ctx()))
    text='\n'.join(x[0] for x in u.effective_message.texts)
    assert '<b>' not in text and '</b>' not in text
    assert 'Mode:' in text and 'Live: OFF' in text

def test_active_handlers():
    assert main.V90_COMMAND_REGISTRY['status'] is main.status1160rc4925_cmd
    assert main.V90_COMMAND_REGISTRY['performanceaudit'] is main.performanceaudit1160rc4925_cmd
    assert main.V90_COMMAND_REGISTRY['commandcert'] is main.commandcert1160rc4925_cmd
