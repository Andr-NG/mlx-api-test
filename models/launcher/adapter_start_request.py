from pathlib import Path
from typing import Optional
from pydantic import BaseModel



class Proxy:
    username: str
    host: str
    type: str
    password: str
    port: str
    save_traffic: bool




class Overrides(BaseModel):
    Timezone: Optional[str] = None
    PublicIP: Optional[str] = None
    Coordinate: Optional[Coordinate] = None
    Proxy: Optional[str] = None

class StartRequest(BaseModel):
    ProfileID: str
    ProfilePathDir: Path
    Selenium: bool
    Puppeteer: bool
    Headless: bool
    FpRaw: Optional[str] = None
    Overrides: Optional[Overrides] = None
