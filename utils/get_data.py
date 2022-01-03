from pathlib import Path
from glob import glob
import pickle
from dataclasses import dataclass

import pandas as pd
import numpy as np
from tqdm import tqdm

from db_models import session, Item


@dataclass
class ItemData:
    """Data for Items."""

    name: str = ""
    item_id: int = 0
    type: str = ""
    # Details
    weight: int = 0
    npc_buy: int = 0
    npc_sell: int = 0
    refineable: bool = None
    equip_locations: str = ""
    # Stats
    range: int = 0
    defense: int = 0
    attack: int = 0
    weapon_level: int = 0
    slots: int = 0
    # Restrictions
    level_range: str = ""
    usage: str = ""
    trade: str = ""
    job_class_type: str = ""
    job_classes: str = ""
    gender: str = ""
    # Scripts
    use_script: str = ""
    equip_script: str = ""
    unequip_script: str = ""


def process_item(item):
    item_data = ItemData()
    for table in item:
        if "Use Script" in table.columns:
            item_data.use_script = table["Use Script"][0]
            item_data.equip_script = table["Use Script"][2]
            item_data.unequip_script = table["Use Script"][4]
        elif "ID" in table.columns:
            pass
        elif table[0][0] == "Name":
            item_data.name = table[1][0]
            item_data.item_id = int(table[1][1].split()[0])
            item_data.type = table[1][2]
        elif table[0][0] == "Weight":
            item_data.weight = int(table[1][0])
            item_data.npc_buy = int(table[1][1].split()[0].replace(",", ""))
            item_data.npc_sell = int(table[1][2].split()[0].replace(",", ""))
            item_data.refineable = True if table[1][3] == "Yes" else False
            item_data.equip_locations = table[1][4]
        elif table[0][0] == "Range":
            item_data.range = int(table[1][0])
            item_data.defense = int(table[1][1])
            item_data.attack = int(table[1][2])
            item_data.weapon_level = int(table[1][3])
            item_data.slots = int(table[1][4])
        elif table[0][0] == "Level Range":
            item_data.level_range = table[1][0]
            item_data.usage = table[1][1]
            item_data.trade = table[1][2]
            item_data.job_class_types = table[1][3]
            item_data.job_classes = table[1][4]
            item_data.gender = table[1][5]
    return item_data


BASE_DIR = Path.cwd()

items_pages = glob(f"{BASE_DIR / 'data/cp.originsro.org/item/view/index.html?id=*'}")

if Path(BASE_DIR / "data/items_data.pkl").exists():
    with open(BASE_DIR / "data/items_data.pkl", "rb") as f:
        items_data = pickle.load(f)
else:
    items_data = {}
    for page in tqdm(items_pages):
        item_id = page.split("=")[1]
        items_data[int(item_id)] = pd.read_html(page)

    with open(BASE_DIR / "data/items_data.pkl", "wb") as f:
        pickle.dump(items_data, f)

items = []
for item_id in tqdm(sorted(list(items_data.keys()))):
    item_data = process_item(items_data[item_id])
    item = Item(
        # Basic Info
        name=item_data.name,
        item_id=item_data.item_id,
        type=item_data.type,
        # Details
        weight=item_data.weight,
        npc_buy=item_data.npc_buy,
        npc_sell=item_data.npc_sell,
        refineable=item_data.refineable,
        equip_locations=item_data.equip_locations,
        # Stats
        range=item_data.range,
        defense=item_data.defense,
        attack=item_data.attack,
        weapon_level=item_data.weapon_level,
        slots=item_data.slots,
        # Restrictions
        level_range=item_data.level_range,
        usage=item_data.usage,
        trade=item_data.trade,
        job_class_types=item_data.job_class_types,
        job_classes=item_data.job_classes,
        gender=item_data.gender,
        # Scripts
        use_script=item_data.use_script,
        equip_script=item_data.equip_script,
        unequip_script=item_data.unequip_script,
    )
    items.append(item)
session.bulk_save_objects(items)
session.commit()
