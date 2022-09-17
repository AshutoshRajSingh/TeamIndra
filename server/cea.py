import asyncio
import aiohttp
import datetime

class PSPEnergyEntry:
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.pop('ID')
        self._month = kwargs.pop('Month')
        self.state = kwargs.pop('State').strip()
        self.energy_requirement = kwargs.pop('energy_requirement')
        self.energy_availability = kwargs.pop('energy_availability')
    
    @property
    def month(self):
        return datetime.datetime.strptime(self._month, '%b-%Y')

    def __repr__(self):
        return f'<PSPEnergyEntry id={self.id}, month={self.month}, state={self.state}, energy_requirement={self.energy_requirement}>'
    


class CEAClient:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session
        self.BASE_URL = 'https://cea.nic.in/api/'
        self.state_cache = {}

    def __del__(self):
        asyncio.create_task(self.session.close())

    async def populate_cache(self):
        async with self.session.get(self.BASE_URL + 'psp_energy.php/') as r:
            if r.status >= 200 and r.status <= 400:
                d = await r.json(content_type=None)
                for entry_ in d:
                    entry = PSPEnergyEntry(**entry_)

                    if entry.state in self.state_cache:
                        self.state_cache[entry.state].append(entry)
                    else:
                        self.state_cache[entry.state] = [entry]

        for _, v in self.state_cache.items():
            v.sort(key=lambda a: a.month)
