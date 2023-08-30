import json
import os

import requests

from wikiteam3.dumpgenerator.api.get_json import do_get_json
from wikiteam3.dumpgenerator.cli.delay import Delay
from wikiteam3.dumpgenerator.config import Config


def save_site_info(config: Config, session: requests.Session):
    """Save a file with site info"""

    if not config.api:
        return
    if os.path.exists(f"{config.path}/siteinfo.json"):
        print("siteinfo.json exists, do not overwrite")
    else:
        print("Downloading site info as siteinfo.json")

        # MediaWiki 1.13+
        r = session.get(
            url=config.api,
            params={
                "action": "query",
                "meta": "siteinfo",
                "siprop": "general|namespaces|statistics|dbrepllag|interwikimap|namespacealiases|specialpagealiases|usergroups|extensions|skins|magicwords|fileextensions|rightsinfo",
                "sinumberingroup": 1,
                "format": "json",
            },
            timeout=10,
        )
        # MediaWiki 1.11-1.12
        if "query" not in do_get_json(r):
            r = session.get(
                url=config.api,
                params={
                    "action": "query",
                    "meta": "siteinfo",
                    "siprop": "general|namespaces|statistics|dbrepllag|interwikimap",
                    "format": "json",
                },
                timeout=10,
            )
            # MediaWiki 1.8-1.10
        if "query" not in do_get_json(r):
            r = session.get(
                url=config.api,
                params={
                    "action": "query",
                    "meta": "siteinfo",
                    "siprop": "general|namespaces",
                    "format": "json",
                },
                timeout=10,
            )
        result = do_get_json(r)
        Delay(config=config)
        with open(f"{config.path}/siteinfo.json", "w", encoding="utf-8") as outfile:
            outfile.write(json.dumps(result, indent=4, sort_keys=True))
