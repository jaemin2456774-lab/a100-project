import asyncio
import main

class Msg:
    def __init__(self): self.text = None
    async def reply_text(self, text, **kwargs):
        self.text = text
        return text
class Update:
    def __init__(self): self.message = Msg()

def test_status_command_no_nameerror_and_replies():
    u=Update()
    asyncio.run(main.status1160ltss21_cmd(u, None))
    assert u.message.text
    assert 'SPRINT 2 CERTIFICATION STATUS' in u.message.text
    assert 'Last recovery' in u.message.text

def test_status_registry_points_to_hotfix_handler():
    assert main.V90_COMMAND_REGISTRY['status'] is main.status1160ltss21_cmd
