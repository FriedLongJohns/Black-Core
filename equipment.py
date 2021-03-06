from random import randint
FRAMES = {
    "Talus": {
        "hp": 100,
        "act_time": 5,
        "move": 3,
        "desc": "A jack-of-all-trades frame, the Talus has hp to survive a few hits while being able to act and move fairly quickly.",
    },
    "Prevada": {
        "hp": 70,
        "act_time": 4,
        "move": 3,
        "desc": "The Prevada is quick and fast, although it's low hp means it needs to be used carefully.",
    },
    "Chralor": {
        "hp": 145,
        "act_time": 4.5,
        "move": 2,
        "desc": "Named sarcastically after the word 'Valor,' the Chralor is designed to be used as the word would imply: Slowly go into battle, tanking damage while destroying everything in it's path."
    },
    "Ketaris": {
        "hp": 50,
        "act_time": 2,
        "move": 1,
        "desc": "The Ketaris emerged after a particularly ambitious attempt to have an extremely low act time to use full-size artillery cannons on a frame, and as such also carries the consequences: Extremely low hp, and horrendusly slow."
    }
}

WEAPONS = {
    "Hammer": {
        "damage": 65,
        "range": 2,
        "use_time_speed": .8,
        "cooldown": 2,
    },
    "Knife": {
        "damage": 40,
        "range": 1,
        "use_time_speed": .5,
        "cooldown": 0,
    },
    "STICK": {
        "damage": 60,
        "range": 3,
        "use_time_speed": .7,
        "cooldown": 2,
    },

    "Burst Rifle": {
        "damage": 50,
        "range": 5,
        "use_time_speed": .7,
        "cooldown": 6,
    },
    "Sniper Rifle": {
        "damage": 60,
        "range": 10,
        "use_time_speed": 1.2,
        "cooldown": 8,
    },

    "Pistol": {
        "damage": 30,
        "range": 4,
        "use_time_speed": .5,
        "cooldown": 4,
    },
    "SMG": {
        "damage": 10,
        "range": 5,
        "use_time_speed": .4,
        "cooldown": 0,
    },

    "Cannon": {
        "damage": 100,
        "range": 5,
        "use_time_speed": 1.1,
        "cooldown": 20,
    },
    "Railgun": {
        "damage": 150,
        "range": 20,
        "use_time_speed": 1.5,
        "cooldown": 30,
    },
    "Shotgun": {
        "damage": 90,
        "range": 3,
        "use_time_speed": .9,
        "cooldown": 8,
    },
}

ARMORS = {
    "None": {
        "hp": 0,
        "act_time_multiplier": 1,
        "damage_multiplier": 1,
    },
    "Heavy Composite": {
        "hp": 40,
        "act_time_multiplier": 1.35,
        "damage_multiplier": .8,
    },
    "Fiber Skeletals": {
        "hp": -5,
        "act_time_multiplier": .95,
        "damage_multiplier": .95,
    },
    "Blast Segment Plating": {
        "hp": 30,
        "act_time_multiplier": 1.1,
        "damage_multiplier": 1.1,
    },
    "Aerodynamic Refits": {
        "hp": 3,
        "act_time_multiplier": .85,
        "damage_multiplier": 1.1,
    },
    "Magnetic Shielding": {
        "hp": -10,
        "act_time_multiplier": 1.5,
        "damage_multiplier": .5,
    },
}

len_frms=len(list(FRAMES.keys()))-1
len_wps=len(list(WEAPONS.keys()))-1
len_arms=len(list(ARMORS.keys()))-1

def randFrameName():
    return list(FRAMES.keys())[randint(0,len_frms)]
def randWeaponName():
    return list(WEAPONS.keys())[randint(0,len_wps)]
def randArmorName():
    return list(ARMORS.keys())[randint(0,len_arms)]
