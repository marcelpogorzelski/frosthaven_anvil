import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

#https://github.com/cmlenius/gloomhaven-card-browser/blob/main/data/scripts/characters.js

class_names = {
  "Blinkblade": { 
    'id': "BB",
    'name': "Blinkblade",
    'matImage': "character-mats/frosthaven/fh-blinkblade.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-blinkblade-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-blinkblade-perks.jpeg" 
  },
  "Bannerspear": {
    'id': "BN",
    'name': "Banner Spear",
    'matImage': "character-mats/frosthaven/fh-banner-spear.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-banner-spear-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-banner-spear-perks.jpeg"
  },
  "Boneshaper": {
    'id': "BO",
    'name': "Boneshaper",
    'matImage': "character-mats/frosthaven/fh-boneshaper.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-boneshaper-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-boneshaper-perks.jpeg"
  },
  "Drifter": {
    'id': "DF",
    'name': "Drifter",
    'matImage': "character-mats/frosthaven/fh-drifter.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-drifter-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-drifter-perks.jpeg"
  },
  "Deathwalker": {
    'id': "DW",
    'name': "Deathwalker",
    'matImage': "character-mats/frosthaven/fh-deathwalker.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-deathwalker-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-deathwalker-perks.jpeg"
  },
  "Geminate": {
    'id': "GE",
    'name': "Geminate",
    'matImage': "character-mats/frosthaven/fh-geminate.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-geminate-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-geminate-perks.jpeg"
  },
  "Coral": {
    'id': "CR",
    'name': "Crashing Tide",
    'matImage': "character-mats/frosthaven/fh-crashing-tide.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-crashing-tide-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-crashing-tide-perks.jpeg"
  },
  "Kelp": {
    'id': "DT",
    'name': "Deepwraith",
    'matImage': "character-mats/frosthaven/fh-deepwraith.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-deepwraith-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-deepwraith-perks.jpeg"
  },
  "Fist": {
    'id': "FF",
    'name': "Frozen Fist",
    'matImage': "character-mats/frosthaven/fh-frozen-fist.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-frozen-fist-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-frozen-fist-perks.jpeg"
  },
  "Prism": {
    'id': "HV",
    'name': "Hive",
    'matImage': "character-mats/frosthaven/fh-hive.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-hive-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-hive-perks.jpeg"
  },
  "Astral": {
    'id': "IF",
    'name': "Infuser",
    'matImage': "character-mats/frosthaven/fh-infuser.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-infuser-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-infuser-perks.jpeg"
  },
  "Drill": {
    'id': "ME",
    'name': "Metal Mosaic",
    'matImage': "character-mats/frosthaven/fh-metal-mosaic.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-metal-mosaic-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-metal-mosaic-perks.jpeg"
  },
  "Shackles": {
    'id': "PC",
    'name': "Pain Conduit",
    'matImage': "character-mats/frosthaven/fh-pain-conduit.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-pain-conduit-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-pain-conduit-perks.jpeg"
  },
  "Meteor": {
    'id': "PY",
    'name': "Pyroclast",
    'matImage': "character-mats/frosthaven/fh-pyroclast.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-pyroclast-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-pyroclast-perks.jpeg"
  } ,
  "Snowflake": {
    'id': "SD",
    'name': "Snowdancer",
    'matImage': "character-mats/frosthaven/fh-snowdancer.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-snowdancer-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-snowdancer-perks.jpeg"
  },
  "Shards": {
    'id': "SH",
    'name': "Shattersong",
    'matImage': "character-mats/frosthaven/fh-shattersong.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-shattersong-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-shattersong-perks.jpeg"
  },
  "Trap": {
    'id': "TA",
    'name': "Trapper",
    'matImage': "character-mats/frosthaven/fh-trapper.jpeg",
    'matImageBack': "character-mats/frosthaven/fh-trapper-back.jpeg",
    'sheetImage': "character-perks/frosthaven/fh-trapper-perks.jpeg"
  }
}

class_cards_info = { "BB": [
    {
    "name": "bb-back",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-bb-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "blurry jab",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-blurry-jab.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "borrowed time",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-borrowed-time.jpeg",
    "initiative": 2,
    "level": 1.5
    },
    {
    "name": "breakneck speed",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-breakneck-speed.jpeg",
    "initiative": 3,
    "level": 5
    },
    {
    "name": "cascading reaction",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-cascading-reaction.jpeg",
    "initiative": 19,
    "level": 1
    },
    {
    "name": "double time",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-double-time.jpeg",
    "initiative": 22,
    "level": 3
    },
    {
    "name": "drive recharge",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-drive-recharge.jpeg",
    "initiative": 69,
    "level": 1
    },
    {
    "name": "experimental adjustment",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-experimental-adjustment.jpeg",
    "initiative": 12,
    "level": 1.5
    },
    {
    "name": "fastest alive",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-fastest-alive.jpeg",
    "initiative": 1,
    "level": 8
    },
    {
    "name": "flashing flurry",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-flashing-flurry.jpeg",
    "initiative": 40,
    "level": 5
    },
    {
    "name": "fractured timeline",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-fractured-timeline.jpeg",
    "initiative": 55,
    "level": 9
    },
    {
    "name": "hit and run",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-hit-and-run.jpeg",
    "initiative": 41,
    "level": 1
    },
    {
    "name": "kinetic transfer",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-kinetic-transfer.jpeg",
    "initiative": 36,
    "level": 1
    },
    {
    "name": "make it count",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-make-it-count.jpeg",
    "initiative": 51,
    "level": 3
    },
    {
    "name": "overdrive",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-overdrive.jpeg",
    "initiative": 60,
    "level": 1
    },
    {
    "name": "phasing blades",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-phasing-blades.jpeg",
    "initiative": 63,
    "level": 7
    },
    {
    "name": "potential energy",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-potential-energy.jpeg",
    "initiative": 32,
    "level": 4
    },
    {
    "name": "power leak",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-power-leak.jpeg",
    "initiative": 17,
    "level": 1
    },
    {
    "name": "precision timing",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-precision-timing.jpeg",
    "initiative": 15,
    "level": 4
    },
    {
    "name": "quantum uncertainty",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-quantum-uncertainty.jpeg",
    "initiative": 35,
    "level": 8
    },
    {
    "name": "reckless augmentation",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-reckless-augmentation.jpeg",
    "initiative": 10,
    "level": 2
    },
    {
    "name": "reverse the flow",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-reverse-the-flow.jpeg",
    "initiative": 58,
    "level": 9
    },
    {
    "name": "rushed to the end",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-rushed-to-the-end.jpeg",
    "initiative": 32,
    "level": 7
    },
    {
    "name": "sand in the hourglass",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-sand-in-the-hourglass.jpeg",
    "initiative": 52,
    "level": 1.5
    },
    {
    "name": "sap speed",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-sap-speed.jpeg",
    "initiative": 45,
    "level": 1
    },
    {
    "name": "stab them all",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-stab-them-all.jpeg",
    "initiative": 4,
    "level": 6
    },
    {
    "name": "systems reboot",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-systems-reboot.jpeg",
    "initiative": 57,
    "level": 2
    },
    {
    "name": "temporal displacement",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-temporal-displacement.jpeg",
    "initiative": 44,
    "level": 1
    },
    {
    "name": "the knife's edge",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-the-knifes-edge.jpeg",
    "initiative": 65,
    "level": 6
    },
    {
    "name": "twin strike",
    "class": "BB",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BB/fh-twin-strike.jpeg",
    "initiative": 24,
    "level": 1
    }
],
"BN": [
    {
    "name": "bn-back",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-bn-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "air support",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-air-support.jpeg",
    "initiative": 20,
    "level": 4
    },
    {
    "name": "at all costs",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-at-all-costs.jpeg",
    "initiative": 60,
    "level": 1
    },
    {
    "name": "barricade",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-barricade.jpeg",
    "initiative": 16,
    "level": 6
    },
    {
    "name": "boldening blow",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-boldening-blow.jpeg",
    "initiative": 72,
    "level": 4
    },
    {
    "name": "bolstering shout",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-bolstering-shout.jpeg",
    "initiative": 75,
    "level": 6
    },
    {
    "name": "combined effort",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-combined-effort.jpeg",
    "initiative": 32,
    "level": 1
    },
    {
    "name": "deflecting maneuver",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-deflecting-maneuver.jpeg",
    "initiative": 15,
    "level": 1
    },
    {
    "name": "driving inspiration",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-driving-inspiration.jpeg",
    "initiative": 18,
    "level": 1.5
    },
    {
    "name": "explosive epicenter",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-explosive-epicenter.jpeg",
    "initiative": 78,
    "level": 5
    },
    {
    "name": "hail of spears",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-hail-of-spears.jpeg",
    "initiative": 44,
    "level": 9
    },
    {
    "name": "head of the hammer",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-head-of-the-hammer.jpeg",
    "initiative": 87,
    "level": 3
    },
    {
    "name": "hold the line",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-hold-the-line.jpeg",
    "initiative": 5,
    "level": 5
    },
    {
    "name": "incendiary throw",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-incendiary-throw.jpeg",
    "initiative": 22,
    "level": 1.5
    },
    {
    "name": "javelin",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-javelin.jpeg",
    "initiative": 21,
    "level": 1
    },
    {
    "name": "lead from afar",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-lead-from-afar.jpeg",
    "initiative": 80,
    "level": 7
    },
    {
    "name": "let them come",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-let-them-come.jpeg",
    "initiative": 24,
    "level": 3
    },
    {
    "name": "meat grinder",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-meat-grinder.jpeg",
    "initiative": 62,
    "level": 2
    },
    {
    "name": "pincer movement",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-pincer-movement.jpeg",
    "initiative": 69,
    "level": 1
    },
    {
    "name": "pinning charge",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-pinning-charge.jpeg",
    "initiative": 17,
    "level": 2
    },
    {
    "name": "rallying cry",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-rallying-cry.jpeg",
    "initiative": 71,
    "level": 1
    },
    {
    "name": "regroup",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-regroup.jpeg",
    "initiative": 25,
    "level": 1
    },
    {
    "name": "resolved courage",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-resolved-courage.jpeg",
    "initiative": 10,
    "level": 1.5
    },
    {
    "name": "set for the charge",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-set-for-the-charge.jpeg",
    "initiative": 6,
    "level": 1
    },
    {
    "name": "sweeping aid",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-sweeping-aid.jpeg",
    "initiative": 73,
    "level": 8
    },
    {
    "name": "take no prisoners",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-take-no-prisoners.jpeg",
    "initiative": 85,
    "level": 9
    },
    {
    "name": "taunting howl",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-taunting-howl.jpeg",
    "initiative": 11,
    "level": 8
    },
    {
    "name": "tip of the spear",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-tip-of-the-spear.jpeg",
    "initiative": 67,
    "level": 1
    },
    {
    "name": "tri-thrust",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-tri-thrust.jpeg",
    "initiative": 27,
    "level": 7
    },
    {
    "name": "unbreakable wall",
    "class": "BN",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BN/fh-unbreakable-wall.jpeg",
    "initiative": 83,
    "level": 1
    }
],
"BO": [
    {
    "name": "bo-back",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-bo-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "angry spirits",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-angry-spirits.jpeg",
    "initiative": 76,
    "level": 1
    },
    {
    "name": "approach oblivion",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-approach-oblivion.jpeg",
    "initiative": 53,
    "level": 1.5
    },
    {
    "name": "behold the shrouded sun",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-behold-the-shrouded-sun.jpeg",
    "initiative": 10,
    "level": 9
    },
    {
    "name": "bone dagger",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-bone-dagger.jpeg",
    "initiative": 29,
    "level": 2
    },
    {
    "name": "command the wretched",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-command-the-wretched.jpeg",
    "initiative": 83,
    "level": 1
    },
    {
    "name": "critical failure",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-critical-failure.jpeg",
    "initiative": 95,
    "level": 4
    },
    {
    "name": "damned horde",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-damned-horde.jpeg",
    "initiative": 71,
    "level": 1
    },
    {
    "name": "dark tidings",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-dark-tidings.jpeg",
    "initiative": 43,
    "level": 1
    },
    {
    "name": "decaying will",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-decaying-will.jpeg",
    "initiative": 46,
    "level": 1
    },
    {
    "name": "endless numbers",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-endless-numbers.jpeg",
    "initiative": 86,
    "level": 8
    },
    {
    "name": "eternal torment",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-eternal-torment.jpeg",
    "initiative": 70,
    "level": 1
    },
    {
    "name": "exploding corpse",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-exploding-corpse.jpeg",
    "initiative": 21,
    "level": 1.5
    },
    {
    "name": "fell remedy",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-fell-remedy.jpeg",
    "initiative": 30,
    "level": 1
    },
    {
    "name": "flesh shield",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-flesh-shield.jpeg",
    "initiative": 16,
    "level": 4
    },
    {
    "name": "flow of the black river",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-flow-of-the-black-river.jpeg",
    "initiative": 18,
    "level": 1
    },
    {
    "name": "grave digging",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-grave-digging.jpeg",
    "initiative": 96,
    "level": 3
    },
    {
    "name": "life in death",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-life-in-death.jpeg",
    "initiative": 91,
    "level": 1
    },
    {
    "name": "malicious conversion",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-malicious-conversion.jpeg",
    "initiative": 26,
    "level": 1
    },
    {
    "name": "putrid cloud",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-putrid-cloud.jpeg",
    "initiative": 28,
    "level": 3
    },
    {
    "name": "recycled limbs",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-recycled-limbs.jpeg",
    "initiative": 52,
    "level": 7
    },
    {
    "name": "returned servant",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-returned-servant.jpeg",
    "initiative": 81,
    "level": 1
    },
    {
    "name": "rotting multitude",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-rotting-multitude.jpeg",
    "initiative": 66,
    "level": 6
    },
    {
    "name": "solid bones",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-solid-bones.jpeg",
    "initiative": 32,
    "level": 5
    },
    {
    "name": "soul claim",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-soul-claim.jpeg",
    "initiative": 23,
    "level": 7
    },
    {
    "name": "transfer of essence",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-transfer-of-essence.jpeg",
    "initiative": 62,
    "level": 1
    },
    {
    "name": "twisted decree",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-twisted-decree.jpeg",
    "initiative": 85,
    "level": 6
    },
    {
    "name": "unearthed horror",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-unearthed-horror.jpeg",
    "initiative": 94,
    "level": 2
    },
    {
    "name": "unforgivable methods",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-unforgivable-methods.jpeg",
    "initiative": 98,
    "level": 5
    },
    {
    "name": "unholy prowess",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-unholy-prowess.jpeg",
    "initiative": 97,
    "level": 9
    },
    {
    "name": "wailing from beyond",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-wailing-from-beyond.jpeg",
    "initiative": 73,
    "level": 8
    },
    {
    "name": "wrath of the turned earth",
    "class": "BO",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/BO/fh-wrath-of-the-turned-earth.jpeg",
    "initiative": 80,
    "level": 1.5
    }
],
"CR": [
    {
    "name": "cr-back",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-cr-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "blood in the water",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-blood-in-the-water.jpeg",
    "initiative": 53,
    "level": 2
    },
    {
    "name": "chaotic refraction",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-chaotic-refraction.jpeg",
    "initiative": 26,
    "level": 4
    },
    {
    "name": "cleansing swell",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-cleansing-swell.jpeg",
    "initiative": 45,
    "level": 1
    },
    {
    "name": "clean sweep",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-clean-sweep.jpeg",
    "initiative": 65,
    "level": 4
    },
    {
    "name": "crashing surge",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-crashing-surge.jpeg",
    "initiative": 34,
    "level": 1
    },
    {
    "name": "cresting force",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-cresting-force.jpeg",
    "initiative": 87,
    "level": 1
    },
    {
    "name": "crush armor",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-crush-armor.jpeg",
    "initiative": 42,
    "level": 1.5
    },
    {
    "name": "death on all sides",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-death-on-all-sides.jpeg",
    "initiative": 73,
    "level": 8
    },
    {
    "name": "down to the depths",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-down-to-the-depths.jpeg",
    "initiative": 74,
    "level": 1
    },
    {
    "name": "drown beneath the waves",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-drown-beneath-the-waves.jpeg",
    "initiative": 9,
    "level": 7
    },
    {
    "name": "dug in",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-dug-in.jpeg",
    "initiative": 76,
    "level": 7
    },
    {
    "name": "ebb and flow",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-ebb-and-flow.jpeg",
    "initiative": 24,
    "level": 8
    },
    {
    "name": "endless cycle",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-endless-cycle.jpeg",
    "initiative": 8,
    "level": 3
    },
    {
    "name": "high tide",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-high-tide.jpeg",
    "initiative": 90,
    "level": 9
    },
    {
    "name": "low tide",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-low-tide.jpeg",
    "initiative": 10,
    "level": 9
    },
    {
    "name": "mighty claws",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-mighty-claws.jpeg",
    "initiative": 23,
    "level": 1
    },
    {
    "name": "overwhelming wave",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-overwhelming-wave.jpeg",
    "initiative": 86,
    "level": 1
    },
    {
    "name": "pool of power",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-pool-of-power.jpeg",
    "initiative": 41,
    "level": 1
    },
    {
    "name": "powerful pincer",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-powerful-pincer.jpeg",
    "initiative": 70,
    "level": 6
    },
    {
    "name": "rancid brine",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-rancid-brine.jpeg",
    "initiative": 62,
    "level": 1
    },
    {
    "name": "rising flood",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-rising-flood.jpeg",
    "initiative": 49,
    "level": 1.5
    },
    {
    "name": "sharp chitin",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-sharp-chitin.jpeg",
    "initiative": 25,
    "level": 1
    },
    {
    "name": "shuck",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-shuck.jpeg",
    "initiative": 55,
    "level": 3
    },
    {
    "name": "skitter",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-skitter.jpeg",
    "initiative": 51,
    "level": 1
    },
    {
    "name": "smashing torrent",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-smashing-torrent.jpeg",
    "initiative": 79,
    "level": 2
    },
    {
    "name": "sodden soil",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-sodden-soil.jpeg",
    "initiative": 17,
    "level": 5
    },
    {
    "name": "soft flesh",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-soft-flesh.jpeg",
    "initiative": 75,
    "level": 1
    },
    {
    "name": "submerge",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-submerge.jpeg",
    "initiative": 68,
    "level": 1
    },
    {
    "name": "tidal blast",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-tidal-blast.jpeg",
    "initiative": 71,
    "level": 5
    },
    {
    "name": "twilight grasp",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-twilight-grasp.jpeg",
    "initiative": 33,
    "level": 6
    },
    {
    "name": "undertow",
    "class": "CR",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/CR/fh-undertow.jpeg",
    "initiative": 15,
    "level": 1.5
    }
],
"DF": [
    {
    "name": "df-back",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-df-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "accurate strikes",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-accurate-strikes.jpeg",
    "initiative": 56,
    "level": 6
    },
    {
    "name": "against all odds",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-against-all-odds.jpeg",
    "initiative": 37,
    "level": 8
    },
    {
    "name": "bloodletting",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-bloodletting.jpeg",
    "initiative": 65,
    "level": 1
    },
    {
    "name": "break through",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-break-through.jpeg",
    "initiative": 34,
    "level": 5
    },
    {
    "name": "chunk of flesh",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-chunk-of-flesh.jpeg",
    "initiative": 62,
    "level": 4
    },
    {
    "name": "consume stamina",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-consume-stamina.jpeg",
    "initiative": 21,
    "level": 6
    },
    {
    "name": "continuous health",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-continuous-health.jpeg",
    "initiative": 61,
    "level": 1
    },
    {
    "name": "crushing weight",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-crushing-weight.jpeg",
    "initiative": 71,
    "level": 1
    },
    {
    "name": "deadly shot",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-deadly-shot.jpeg",
    "initiative": 32,
    "level": 1
    },
    {
    "name": "destructive fury",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-destructive-fury.jpeg",
    "initiative": 19,
    "level": 1.5
    },
    {
    "name": "draining arrows",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-draining-arrows.jpeg",
    "initiative": 23,
    "level": 1
    },
    {
    "name": "dual bow",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-dual-bow.jpeg",
    "initiative": 26,
    "level": 3
    },
    {
    "name": "ever forward",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-ever-forward.jpeg",
    "initiative": 67,
    "level": 2
    },
    {
    "name": "everlasting",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-everlasting.jpeg",
    "initiative": 96,
    "level": 9
    },
    {
    "name": "fierce barrage",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-fierce-barrage.jpeg",
    "initiative": 32,
    "level": 3
    },
    {
    "name": "fortitude",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-fortitude.jpeg",
    "initiative": 31,
    "level": 1.5
    },
    {
    "name": "gift of the prey",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-gift-of-the-prey.jpeg",
    "initiative": 40,
    "level": 4
    },
    {
    "name": "inevitable conclusion",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-inevitable-conclusion.jpeg",
    "initiative": 29,
    "level": 8
    },
    {
    "name": "like the wind",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-like-the-wind.jpeg",
    "initiative": 77,
    "level": 7
    },
    {
    "name": "no remorse",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-no-remorse.jpeg",
    "initiative": 20,
    "level": 1.5
    },
    {
    "name": "precision aim",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-precision-aim.jpeg",
    "initiative": 66,
    "level": 1
    },
    {
    "name": "prudent preparation",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-prudent-preparation.jpeg",
    "initiative": 14,
    "level": 1
    },
    {
    "name": "relentless",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-relentless.jpeg",
    "initiative": 89,
    "level": 1
    },
    {
    "name": "shockwave",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-shockwave.jpeg",
    "initiative": 17,
    "level": 2
    },
    {
    "name": "survivalist",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-survivalist.jpeg",
    "initiative": 91,
    "level": 5
    },
    {
    "name": "sustained momentum",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-sustained-momentum.jpeg",
    "initiative": 76,
    "level": 1
    },
    {
    "name": "unbreakable",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-unbreakable.jpeg",
    "initiative": 90,
    "level": 1
    },
    {
    "name": "unending fight",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-unending-fight.jpeg",
    "initiative": 25,
    "level": 7
    },
    {
    "name": "use every part",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-use-every-part.jpeg",
    "initiative": 18,
    "level": 9
    },
    {
    "name": "vile assault",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-vile-assault.jpeg",
    "initiative": 27,
    "level": 1
    },
    {
    "name": "violent inheritance",
    "class": "DF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DF/fh-violent-inheritance.jpeg",
    "initiative": 70,
    "level": 1
    }
],
"DT": [
    {
    "name": "dt-back",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-dt-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "black night of the deep",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-black-night-of-the-deep.jpeg",
    "initiative": 26,
    "level": 9
    },
    {
    "name": "black scythe",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-black-scythe.jpeg",
    "initiative": 45,
    "level": 1
    },
    {
    "name": "claw of doom",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-claw-of-doom.jpeg",
    "initiative": 30,
    "level": 6
    },
    {
    "name": "consume the helpless",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-consume-the-helpless.jpeg",
    "initiative": 12,
    "level": 9
    },
    {
    "name": "crippling terror",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-crippling-terror.jpeg",
    "initiative": 15,
    "level": 3
    },
    {
    "name": "crushing darkness",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-crushing-darkness.jpeg",
    "initiative": 40,
    "level": 4
    },
    {
    "name": "death spiral",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-death-spiral.jpeg",
    "initiative": 48,
    "level": 5
    },
    {
    "name": "dire frenzy",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-dire-frenzy.jpeg",
    "initiative": 26,
    "level": 7
    },
    {
    "name": "extra decoration",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-extra-decoration.jpeg",
    "initiative": 92,
    "level": 5
    },
    {
    "name": "grim trophies",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-grim-trophies.jpeg",
    "initiative": 18,
    "level": 4
    },
    {
    "name": "hasten the end",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-hasten-the-end.jpeg",
    "initiative": 65,
    "level": 7
    },
    {
    "name": "haunting brutality",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-haunting-brutality.jpeg",
    "initiative": 23,
    "level": 1.5
    },
    {
    "name": "hollow aura",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-hollow-aura.jpeg",
    "initiative": 88,
    "level": 1
    },
    {
    "name": "ink cloud",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-ink-cloud.jpeg",
    "initiative": 28,
    "level": 1
    },
    {
    "name": "lacerating stabs",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-lacerating-stabs.jpeg",
    "initiative": 14,
    "level": 1
    },
    {
    "name": "lie in wait",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-lie-in-wait.jpeg",
    "initiative": 98,
    "level": 2
    },
    {
    "name": "mantle of dread",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-mantle-of-dread.jpeg",
    "initiative": 96,
    "level": 1
    },
    {
    "name": "morbid camouflage",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-morbid-camouflage.jpeg",
    "initiative": 31,
    "level": 1.5
    },
    {
    "name": "pinning spines",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-pinning-spines.jpeg",
    "initiative": 25,
    "level": 3
    },
    {
    "name": "rip from the bone",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-rip-from-the-bone.jpeg",
    "initiative": 11,
    "level": 8
    },
    {
    "name": "skewer the flesh",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-skewer-the-flesh.jpeg",
    "initiative": 86,
    "level": 1
    },
    {
    "name": "skull collection",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-skull-collection.jpeg",
    "initiative": 22,
    "level": 1
    },
    {
    "name": "slipping into death",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-slipping-into-death.jpeg",
    "initiative": 89,
    "level": 2
    },
    {
    "name": "soul hunger",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-soul-hunger.jpeg",
    "initiative": 91,
    "level": 1.5
    },
    {
    "name": "staring into the abyss",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-staring-into-the-abyss.jpeg",
    "initiative": 63,
    "level": 1
    },
    {
    "name": "succumb to fear",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-succumb-to-fear.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "the remorseless deep",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-the-remorseless-deep.jpeg",
    "initiative": 22,
    "level": 6
    },
    {
    "name": "tumultuous panic",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-tumultuous-panic.jpeg",
    "initiative": 66,
    "level": 1
    },
    {
    "name": "unseen horror",
    "class": "DT",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DT/fh-unseen-horror.jpeg",
    "initiative": 19,
    "level": 8
    }
],
"DW": [
    {
    "name": "dw-back",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-dw-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "anger of the dead",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-anger-of-the-dead.jpeg",
    "initiative": 14,
    "level": 1
    },
    {
    "name": "black barrage",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-black-barrage.jpeg",
    "initiative": 28,
    "level": 1
    },
    {
    "name": "black lance",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-black-lance.jpeg",
    "initiative": 16,
    "level": 9
    },
    {
    "name": "call of doom",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-call-of-doom.jpeg",
    "initiative": 32,
    "level": 1
    },
    {
    "name": "call to the abyss",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-call-to-the-abyss.jpeg",
    "initiative": 82,
    "level": 1
    },
    {
    "name": "dark fog",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-dark-fog.jpeg",
    "initiative": 46,
    "level": 1
    },
    {
    "name": "dead bolt",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-dead-bolt.jpeg",
    "initiative": 88,
    "level": 3
    },
    {
    "name": "deepening despair",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-deepening-despair.jpeg",
    "initiative": 11,
    "level": 2
    },
    {
    "name": "dominate",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-dominate.jpeg",
    "initiative": 29,
    "level": 5
    },
    {
    "name": "eclipse",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-eclipse.jpeg",
    "initiative": 86,
    "level": 1
    },
    {
    "name": "fleeting dusk",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-fleeting-dusk.jpeg",
    "initiative": 36,
    "level": 4
    },
    {
    "name": "fluid night",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-fluid-night.jpeg",
    "initiative": 24,
    "level": 1
    },
    {
    "name": "forceful spirits",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-forceful-spirits.jpeg",
    "initiative": 34,
    "level": 1.5
    },
    {
    "name": "frozen in fear",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-frozen-in-fear.jpeg",
    "initiative": 21,
    "level": 8
    },
    {
    "name": "hungry grasps",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-hungry-grasps.jpeg",
    "initiative": 25,
    "level": 7
    },
    {
    "name": "lashing tendrils",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-lashing-tendrils.jpeg",
    "initiative": 80,
    "level": 8
    },
    {
    "name": "lingering rot",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-lingering-rot.jpeg",
    "initiative": 64,
    "level": 1
    },
    {
    "name": "medium",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-medium.jpeg",
    "initiative": 55,
    "level": 5
    },
    {
    "name": "proliferation of the abyss",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-proliferation-of-the-abyss.jpeg",
    "initiative": 38,
    "level": 7
    },
    {
    "name": "pulled across",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-pulled-across.jpeg",
    "initiative": 77,
    "level": 4
    },
    {
    "name": "rest in the shade",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-rest-in-the-shade.jpeg",
    "initiative": 26,
    "level": 1.5
    },
    {
    "name": "restless spirits",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-restless-spirits.jpeg",
    "initiative": 20,
    "level": 2
    },
    {
    "name": "ritual sacrifice",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-ritual-sacrifice.jpeg",
    "initiative": 13,
    "level": 3
    },
    {
    "name": "shadow step",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-shadow-step.jpeg",
    "initiative": 19,
    "level": 1
    },
    {
    "name": "strength of the abyss",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-strength-of-the-abyss.jpeg",
    "initiative": 50,
    "level": 1
    },
    {
    "name": "sunless apparition",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-sunless-apparition.jpeg",
    "initiative": 96,
    "level": 1
    },
    {
    "name": "the night takes shape",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-the-night-takes-shape.jpeg",
    "initiative": 94,
    "level": 6
    },
    {
    "name": "vengeful storm",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-vengeful-storm.jpeg",
    "initiative": 18,
    "level": 6
    },
    {
    "name": "wave of anguish",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-wave-of-anguish.jpeg",
    "initiative": 58,
    "level": 1.5
    },
    {
    "name": "when your time comes",
    "class": "DW",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/DW/fh-when-your-time-comes.jpeg",
    "initiative": 72,
    "level": 9
    }
],
"FF": [
    {
    "name": "ff-back",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-ff-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "bring down the mountain",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-bring-down-the-mountain.jpeg",
    "initiative": 9,
    "level": 9
    },
    {
    "name": "cold boulder",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-cold-boulder.jpeg",
    "initiative": 70,
    "level": 1
    },
    {
    "name": "crushing crystals",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-crushing-crystals.jpeg",
    "initiative": 67,
    "level": 2
    },
    {
    "name": "draw of the bedrock",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-draw-of-the-bedrock.jpeg",
    "initiative": 10,
    "level": 2
    },
    {
    "name": "draw strength",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-draw-strength.jpeg",
    "initiative": 28,
    "level": 8
    },
    {
    "name": "encased punch",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-encased-punch.jpeg",
    "initiative": 19,
    "level": 1
    },
    {
    "name": "freezing shell",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-freezing-shell.jpeg",
    "initiative": 17,
    "level": 1.5
    },
    {
    "name": "frost eruption",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-frost-eruption.jpeg",
    "initiative": 61,
    "level": 1
    },
    {
    "name": "frozen over",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-frozen-over.jpeg",
    "initiative": 20,
    "level": 3
    },
    {
    "name": "frozen spike",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-frozen-spike.jpeg",
    "initiative": 33,
    "level": 9
    },
    {
    "name": "fury of the mountain",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-fury-of-the-mountain.jpeg",
    "initiative": 23,
    "level": 1
    },
    {
    "name": "gift of the mountain",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-gift-of-the-mountain.jpeg",
    "initiative": 73,
    "level": 7
    },
    {
    "name": "glacier slam",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-glacier-slam.jpeg",
    "initiative": 84,
    "level": 6
    },
    {
    "name": "ice blast",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-ice-blast.jpeg",
    "initiative": 32,
    "level": 1
    },
    {
    "name": "ice uppercut",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-ice-uppercut.jpeg",
    "initiative": 15,
    "level": 5
    },
    {
    "name": "lacerating eruption",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-lacerating-eruption.jpeg",
    "initiative": 51,
    "level": 3
    },
    {
    "name": "one with the mountain",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-one-with-the-mountain.jpeg",
    "initiative": 83,
    "level": 1
    },
    {
    "name": "packed solid",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-packed-solid.jpeg",
    "initiative": 55,
    "level": 4
    },
    {
    "name": "piercing pummel",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-piercing-pummel.jpeg",
    "initiative": 30,
    "level": 1
    },
    {
    "name": "preserved fury",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-preserved-fury.jpeg",
    "initiative": 49,
    "level": 5
    },
    {
    "name": "primal bellow",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-primal-bellow.jpeg",
    "initiative": 84,
    "level": 1.5
    },
    {
    "name": "seeing stars",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-seeing-stars.jpeg",
    "initiative": 29,
    "level": 7
    },
    {
    "name": "shard launch",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-shard-launch.jpeg",
    "initiative": 52,
    "level": 1.5
    },
    {
    "name": "shattering blow",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-shattering-blow.jpeg",
    "initiative": 18,
    "level": 8
    },
    {
    "name": "the mountain's fist",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-the-mountains-fist.jpeg",
    "initiative": 16,
    "level": 4
    },
    {
    "name": "thick frost",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-thick-frost.jpeg",
    "initiative": 21,
    "level": 6
    },
    {
    "name": "voice from below",
    "class": "FF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/FF/fh-voice-from-below.jpeg",
    "initiative": 22,
    "level": 1
    }
],
"GE": [
    {
    "name": "ge-back",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-ge-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "accelerated metabolism",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-accelerated-metabolism.jpeg",
    "initiative": 85,
    "level": 8
    },
    {
    "name": "alluring pheromones",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-alluring-pheromones.jpeg",
    "initiative": 49,
    "level": 7
    },
    {
    "name": "changeling's boon",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-changelings-boon.jpeg",
    "initiative": 40,
    "level": 1
    },
    {
    "name": "chitinous horde",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-chitinous-horde.jpeg",
    "initiative": 15,
    "level": 5
    },
    {
    "name": "corrosive acids",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-corrosive-acids.jpeg",
    "initiative": 28,
    "level": 6
    },
    {
    "name": "drag down",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-drag-down.jpeg",
    "initiative": 34,
    "level": 1
    },
    {
    "name": "dragonfly surge",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-dragonfly-surge.jpeg",
    "initiative": 50,
    "level": 3
    },
    {
    "name": "draining pincers",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-draining-pincers.jpeg",
    "initiative": 72,
    "level": 1
    },
    {
    "name": "feeding frenzy",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-feeding-frenzy.jpeg",
    "initiative": 62,
    "level": 1.5
    },
    {
    "name": "firefly swarm",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-firefly-swarm.jpeg",
    "initiative": 76,
    "level": 1
    },
    {
    "name": "flailing tendrils",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-flailing-tendrils.jpeg",
    "initiative": 12,
    "level": 1
    },
    {
    "name": "formless grace",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-formless-grace.jpeg",
    "initiative": 75,
    "level": 5
    },
    {
    "name": "hail of thorns",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-hail-of-thorns.jpeg",
    "initiative": 88,
    "level": 1
    },
    {
    "name": "harbinger of ruin",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-harbinger-of-ruin.jpeg",
    "initiative": 11,
    "level": 9
    },
    {
    "name": "harvest the essence",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-harvest-the-essence.jpeg",
    "initiative": 60,
    "level": 1
    },
    {
    "name": "hirudotherapy",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-hirudotherapy.jpeg",
    "initiative": 92,
    "level": 6
    },
    {
    "name": "hornbeetle carapace",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-hornbeetle-carapace.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "hornet stingers",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-hornet-stingers.jpeg",
    "initiative": 23,
    "level": 1
    },
    {
    "name": "icebound quills",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-icebound-quills.jpeg",
    "initiative": 14,
    "level": 1
    },
    {
    "name": "into my embrace",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-into-my-embrace.jpeg",
    "initiative": 36,
    "level": 1
    },
    {
    "name": "locust host",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-locust-host.jpeg",
    "initiative": 23,
    "level": 2
    },
    {
    "name": "luminous descent",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-luminous-descent.jpeg",
    "initiative": 67,
    "level": 4
    },
    {
    "name": "mandible storm",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-mandible-storm.jpeg",
    "initiative": 30,
    "level": 3
    },
    {
    "name": "mind spike",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-mind-spike.jpeg",
    "initiative": 18,
    "level": 1
    },
    {
    "name": "oscillating entity",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-oscillating-entity.jpeg",
    "initiative": 55,
    "level": 8
    },
    {
    "name": "reckless jab",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-reckless-jab.jpeg",
    "initiative": 38,
    "level": 1.5
    },
    {
    "name": "reshape the guise",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-reshape-the-guise.jpeg",
    "initiative": 38,
    "level": 1.5
    },
    {
    "name": "scarab flight",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-scarab-flight.jpeg",
    "initiative": 30,
    "level": 1
    },
    {
    "name": "selfless offering",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-selfless-offering.jpeg",
    "initiative": 27,
    "level": 1
    },
    {
    "name": "smoldering hatred",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-smoldering-hatred.jpeg",
    "initiative": 32,
    "level": 1.5
    },
    {
    "name": "thresh and flail",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-thresh-and-flail.jpeg",
    "initiative": 43,
    "level": 4
    },
    {
    "name": "two-pronged entrapment",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-two-pronged-entrapment.jpeg",
    "initiative": 21,
    "level": 7
    },
    {
    "name": "venomous barbs",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-venomous-barbs.jpeg",
    "initiative": 17,
    "level": 2
    },
    {
    "name": "voice of salvation",
    "class": "GE",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/GE/fh-voice-of-salvation.jpeg",
    "initiative": 39,
    "level": 9
    }
],
"HV": [
    {
    "name": "hv-back",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-hv-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "aimed assault",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-aimed-assault.jpeg",
    "initiative": 88,
    "level": 1
    },
    {
    "name": "burning slash",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-burning-slash.jpeg",
    "initiative": 29,
    "level": 8
    },
    {
    "name": "code geminate",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-code-geminate.jpeg",
    "initiative": 28,
    "level": 5
    },
    {
    "name": "coiled limbs",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-coiled-limbs.jpeg",
    "initiative": 82,
    "level": 1
    },
    {
    "name": "disassemble",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-disassemble.jpeg",
    "initiative": 20,
    "level": 9
    },
    {
    "name": "divergent destruction",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-divergent-destruction.jpeg",
    "initiative": 22,
    "level": 4
    },
    {
    "name": "faceless entity",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-faceless-entity.jpeg",
    "initiative": 12,
    "level": 1
    },
    {
    "name": "force field",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-force-field.jpeg",
    "initiative": 78,
    "level": 2
    },
    {
    "name": "heavy metal",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-heavy-metal.jpeg",
    "initiative": 76,
    "level": 9
    },
    {
    "name": "high impact projectiles",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-high-impact-projectiles.jpeg",
    "initiative": 16,
    "level": 1
    },
    {
    "name": "hijack",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-hijack.jpeg",
    "initiative": 40,
    "level": 3
    },
    {
    "name": "hunter-killer",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-hunter-killer.jpeg",
    "initiative": 84,
    "level": 1
    },
    {
    "name": "interference",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-interference.jpeg",
    "initiative": 21,
    "level": 1
    },
    {
    "name": "launch pod",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-launch-pod.jpeg",
    "initiative": 77,
    "level": 1
    },
    {
    "name": "long-range missile",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-long-range-missile.jpeg",
    "initiative": 19,
    "level": 2
    },
    {
    "name": "mortar shells",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-mortar-shells.jpeg",
    "initiative": 85,
    "level": 7
    },
    {
    "name": "net dispersal",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-net-dispersal.jpeg",
    "initiative": 94,
    "level": 5
    },
    {
    "name": "plague protocol",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-plague-protocol.jpeg",
    "initiative": 98,
    "level": 4
    },
    {
    "name": "plated defense",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-plated-defense.jpeg",
    "initiative": 80,
    "level": 1
    },
    {
    "name": "prepare for deployment",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-prepare-for-deployment.jpeg",
    "initiative": 64,
    "level": 1
    },
    {
    "name": "rapid fire",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-rapid-fire.jpeg",
    "initiative": 92,
    "level": 3
    },
    {
    "name": "reaper function",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-reaper-function.jpeg",
    "initiative": 32,
    "level": 1
    },
    {
    "name": "reassemble",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-reassemble.jpeg",
    "initiative": 27,
    "level": 1.5
    },
    {
    "name": "recall",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-recall.jpeg",
    "initiative": 91,
    "level": 7
    },
    {
    "name": "reconstructive aid",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-reconstructive-aid.jpeg",
    "initiative": 90,
    "level": 1
    },
    {
    "name": "remote control",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-remote-control.jpeg",
    "initiative": 48,
    "level": 1.5
    },
    {
    "name": "shocking pulse",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-shocking-pulse.jpeg",
    "initiative": 86,
    "level": 1.5
    },
    {
    "name": "spinning blades",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-spinning-blades.jpeg",
    "initiative": 79,
    "level": 6
    },
    {
    "name": "swarming bulwark",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-swarming-bulwark.jpeg",
    "initiative": 96,
    "level": 8
    },
    {
    "name": "triage program",
    "class": "HV",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/HV/fh-triage-program.jpeg",
    "initiative": 13,
    "level": 6
    }
],
"IF": [
    {
    "name": "if-back",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-if-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "ancient rites of power",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-ancient-rites-of-power.jpeg",
    "initiative": 94,
    "level": 9
    },
    {
    "name": "battle prowess",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-battle-prowess.jpeg",
    "initiative": 78,
    "level": 1.5
    },
    {
    "name": "boon of the tempest",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-boon-of-the-tempest.jpeg",
    "initiative": 28,
    "level": 1
    },
    {
    "name": "bounty of the earth",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-bounty-of-the-earth.jpeg",
    "initiative": 23,
    "level": 1
    },
    {
    "name": "caress of the night",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-caress-of-the-night.jpeg",
    "initiative": 87,
    "level": 1
    },
    {
    "name": "coalescing darkness",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-coalescing-darkness.jpeg",
    "initiative": 85,
    "level": 4
    },
    {
    "name": "crystalline aegis",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-crystalline-aegis.jpeg",
    "initiative": 17,
    "level": 1.5
    },
    {
    "name": "desperate throw",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-desperate-throw.jpeg",
    "initiative": 16,
    "level": 4
    },
    {
    "name": "diamondization",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-diamondization.jpeg",
    "initiative": 10,
    "level": 7
    },
    {
    "name": "emerald edge",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-emerald-edge.jpeg",
    "initiative": 70,
    "level": 1
    },
    {
    "name": "formless bladestorm",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-formless-bladestorm.jpeg",
    "initiative": 33,
    "level": 1
    },
    {
    "name": "gale barrage",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-gale-barrage.jpeg",
    "initiative": 44,
    "level": 6
    },
    {
    "name": "gemstone resonance",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-gemstone-resonance.jpeg",
    "initiative": 30,
    "level": 5
    },
    {
    "name": "guide the flow",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-guide-the-flow.jpeg",
    "initiative": 35,
    "level": 3
    },
    {
    "name": "imbue with life",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-imbue-with-life.jpeg",
    "initiative": 42,
    "level": 1.5
    },
    {
    "name": "malachite shockwave",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-malachite-shockwave.jpeg",
    "initiative": 68,
    "level": 7
    },
    {
    "name": "obsidian spear",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-obsidian-spear.jpeg",
    "initiative": 84,
    "level": 5
    },
    {
    "name": "onyx shards",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-onyx-shards.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "propulsive tailwind",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-propulsive-tailwind.jpeg",
    "initiative": 91,
    "level": 6
    },
    {
    "name": "reinforced riposte",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-reinforced-riposte.jpeg",
    "initiative": 18,
    "level": 3
    },
    {
    "name": "remote impact",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-remote-impact.jpeg",
    "initiative": 72,
    "level": 2
    },
    {
    "name": "rising momentum",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-rising-momentum.jpeg",
    "initiative": 25,
    "level": 1
    },
    {
    "name": "sky-splitting strike",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-sky-splitting-strike.jpeg",
    "initiative": 50,
    "level": 9
    },
    {
    "name": "slashing cyclone",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-slashing-cyclone.jpeg",
    "initiative": 14,
    "level": 1
    },
    {
    "name": "stoic vigilance",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-stoic-vigilance.jpeg",
    "initiative": 12,
    "level": 1
    },
    {
    "name": "swift pivot",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-swift-pivot.jpeg",
    "initiative": 8,
    "level": 8
    },
    {
    "name": "torrential cleave",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-torrential-cleave.jpeg",
    "initiative": 83,
    "level": 1
    },
    {
    "name": "unstoppable impulse",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-unstoppable-impulse.jpeg",
    "initiative": 56,
    "level": 1
    },
    {
    "name": "untether the shackles",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-untether-the-shackles.jpeg",
    "initiative": 61,
    "level": 8
    },
    {
    "name": "veil of protection",
    "class": "IF",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/IF/fh-veil-of-protection.jpeg",
    "initiative": 47,
    "level": 2
    }
],
"ME": [
    {
    "name": "me-back",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-me-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "ancient drill",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-ancient-drill.jpeg",
    "initiative": 90,
    "level": 1
    },
    {
    "name": "beam axe",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-beam-axe.jpeg",
    "initiative": 29,
    "level": 1
    },
    {
    "name": "bronze plating",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-bronze-plating.jpeg",
    "initiative": 18,
    "level": 2
    },
    {
    "name": "cryogenic hibernation",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-cryogenic-hibernation.jpeg",
    "initiative": 19,
    "level": 7
    },
    {
    "name": "curious gear",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-curious-gear.jpeg",
    "initiative": 12,
    "level": 1.5
    },
    {
    "name": "curious machinery",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-curious-machinery.jpeg",
    "initiative": 11,
    "level": 8
    },
    {
    "name": "electrical discharge",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-electrical-discharge.jpeg",
    "initiative": 26,
    "level": 3
    },
    {
    "name": "energy conversion",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-energy-conversion.jpeg",
    "initiative": 23,
    "level": 4
    },
    {
    "name": "heat conduction",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-heat-conduction.jpeg",
    "initiative": 11,
    "level": 5
    },
    {
    "name": "heated drill",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-heated-drill.jpeg",
    "initiative": 80,
    "level": 7
    },
    {
    "name": "magnetic field",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-magnetic-field.jpeg",
    "initiative": 21,
    "level": 4
    },
    {
    "name": "memory drive",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-memory-drive.jpeg",
    "initiative": 64,
    "level": 1
    },
    {
    "name": "piston barrage",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-piston-barrage.jpeg",
    "initiative": 33,
    "level": 8
    },
    {
    "name": "polarity shift",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-polarity-shift.jpeg",
    "initiative": 79,
    "level": 9
    },
    {
    "name": "power core",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-power-core.jpeg",
    "initiative": 83,
    "level": 1
    },
    {
    "name": "pressure build-up",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-pressure-build-up.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "processing",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-processing.jpeg",
    "initiative": 95,
    "level": 1.5
    },
    {
    "name": "radiation",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-radiation.jpeg",
    "initiative": 37,
    "level": 5
    },
    {
    "name": "recursion",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-recursion.jpeg",
    "initiative": 50,
    "level": 1.5
    },
    {
    "name": "release valve",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-release-valve.jpeg",
    "initiative": 30,
    "level": 2
    },
    {
    "name": "rocket boots",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-rocket-boots.jpeg",
    "initiative": 22,
    "level": 1
    },
    {
    "name": "scalding blast",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-scalding-blast.jpeg",
    "initiative": 45,
    "level": 6
    },
    {
    "name": "steam armor",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-steam-armor.jpeg",
    "initiative": 17,
    "level": 1
    },
    {
    "name": "steam core",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-steam-core.jpeg",
    "initiative": 71,
    "level": 6
    },
    {
    "name": "steel piston",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-steel-piston.jpeg",
    "initiative": 40,
    "level": 1
    },
    {
    "name": "stress vents",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-stress-vents.jpeg",
    "initiative": 15,
    "level": 3
    },
    {
    "name": "super heat transfer",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-super-heat-transfer.jpeg",
    "initiative": 25,
    "level": 1
    },
    {
    "name": "unstable core",
    "class": "ME",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/ME/fh-unstable-core.jpeg",
    "initiative": 10,
    "level": 9
    }
],
"PC": [
    {
    "name": "pc-back",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-pc-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "blood ritual",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-blood-ritual.jpeg",
    "initiative": 56,
    "level": 1
    },
    {
    "name": "burned at both ends",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-burned-at-both-ends.jpeg",
    "initiative": 30,
    "level": 3
    },
    {
    "name": "chained by despair",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-chained-by-despair.jpeg",
    "initiative": 15,
    "level": 5
    },
    {
    "name": "chained by spite",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-chained-by-spite.jpeg",
    "initiative": 15,
    "level": 5
    },
    {
    "name": "cleansing fire",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-cleansing-fire.jpeg",
    "initiative": 64,
    "level": 1
    },
    {
    "name": "delayed malady",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-delayed-malady.jpeg",
    "initiative": 90,
    "level": 1.5
    },
    {
    "name": "down to the dirt",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-down-to-the-dirt.jpeg",
    "initiative": 39,
    "level": 4
    },
    {
    "name": "explosive wounds",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-explosive-wounds.jpeg",
    "initiative": 43,
    "level": 1
    },
    {
    "name": "hopelessness",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-hopelessness.jpeg",
    "initiative": 83,
    "level": 6
    },
    {
    "name": "infection purge",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-infection-purge.jpeg",
    "initiative": 45,
    "level": 2
    },
    {
    "name": "line of transference",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-line-of-transference.jpeg",
    "initiative": 25,
    "level": 1
    },
    {
    "name": "mirrored misery",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-mirrored-misery.jpeg",
    "initiative": 72,
    "level": 4
    },
    {
    "name": "penance",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-penance.jpeg",
    "initiative": 12,
    "level": 7
    },
    {
    "name": "phantom limb",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-phantom-limb.jpeg",
    "initiative": 75,
    "level": 6
    },
    {
    "name": "pleasure in pain",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-pleasure-in-pain.jpeg",
    "initiative": 47,
    "level": 1.5
    },
    {
    "name": "redemption",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-redemption.jpeg",
    "initiative": 33,
    "level": 9
    },
    {
    "name": "reject the gift",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-reject-the-gift.jpeg",
    "initiative": 20,
    "level": 7
    },
    {
    "name": "reprisal",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-reprisal.jpeg",
    "initiative": 70,
    "level": 3
    },
    {
    "name": "reversal of fate",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-reversal-of-fate.jpeg",
    "initiative": 23,
    "level": 2
    },
    {
    "name": "scarred effigy",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-scarred-effigy.jpeg",
    "initiative": 19,
    "level": 1
    },
    {
    "name": "shared affliction",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-shared-affliction.jpeg",
    "initiative": 61,
    "level": 1
    },
    {
    "name": "swift vengeance",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-swift-vengeance.jpeg",
    "initiative": 21,
    "level": 1
    },
    {
    "name": "the agony of others",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-the-agony-of-others.jpeg",
    "initiative": 78,
    "level": 1
    },
    {
    "name": "the end of everything",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-the-end-of-everything.jpeg",
    "initiative": 99,
    "level": 9
    },
    {
    "name": "transferred injury",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-transferred-injury.jpeg",
    "initiative": 74,
    "level": 1
    },
    {
    "name": "unending torment",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-unending-torment.jpeg",
    "initiative": 29,
    "level": 1
    },
    {
    "name": "unstable effigy",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-unstable-effigy.jpeg",
    "initiative": 18,
    "level": 1.5
    },
    {
    "name": "wave of anguish",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-wave-of-anguish.jpeg",
    "initiative": 68,
    "level": 8
    },
    {
    "name": "wracked with pain",
    "class": "PC",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PC/fh-wracked-with-pain.jpeg",
    "initiative": 22,
    "level": 8
    }
],
"PY": [
    {
    "name": "py-back",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-py-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "calamity",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-calamity.jpeg",
    "initiative": 35,
    "level": 9
    },
    {
    "name": "cinder lance",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-cinder-lance.jpeg",
    "initiative": 90,
    "level": 8
    },
    {
    "name": "cloud of ash",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-cloud-of-ash.jpeg",
    "initiative": 23,
    "level": 1
    },
    {
    "name": "cooling",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-cooling.jpeg",
    "initiative": 75,
    "level": 1
    },
    {
    "name": "deep fury",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-deep-fury.jpeg",
    "initiative": 38,
    "level": 2
    },
    {
    "name": "erupting rage",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-erupting-rage.jpeg",
    "initiative": 70,
    "level": 7
    },
    {
    "name": "eruption",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-eruption.jpeg",
    "initiative": 47,
    "level": 1
    },
    {
    "name": "feed the beast",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-feed-the-beast.jpeg",
    "initiative": 27,
    "level": 8
    },
    {
    "name": "flowing fire",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-flowing-fire.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "force of the earth",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-force-of-the-earth.jpeg",
    "initiative": 15,
    "level": 1.5
    },
    {
    "name": "hand of flame",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-hand-of-flame.jpeg",
    "initiative": 29,
    "level": 4
    },
    {
    "name": "hardened spike",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-hardened-spike.jpeg",
    "initiative": 80,
    "level": 3
    },
    {
    "name": "heat wave",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-heat-wave.jpeg",
    "initiative": 8,
    "level": 4
    },
    {
    "name": "igneous path",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-igneous-path.jpeg",
    "initiative": 18,
    "level": 1
    },
    {
    "name": "lava bomb",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-lava-bomb.jpeg",
    "initiative": 53,
    "level": 1
    },
    {
    "name": "liquid stone",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-liquid-stone.jpeg",
    "initiative": 28,
    "level": 1
    },
    {
    "name": "living magma",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-living-magma.jpeg",
    "initiative": 22,
    "level": 3
    },
    {
    "name": "magma orbs",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-magma-orbs.jpeg",
    "initiative": 82,
    "level": 5
    },
    {
    "name": "melted armor",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-melted-armor.jpeg",
    "initiative": 62,
    "level": 1
    },
    {
    "name": "metamorphic rock",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-metamorphic-rock.jpeg",
    "initiative": 68,
    "level": 1.5
    },
    {
    "name": "obsidian shield",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-obsidian-shield.jpeg",
    "initiative": 19,
    "level": 6
    },
    {
    "name": "quenched rage",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-quenched-rage.jpeg",
    "initiative": 30,
    "level": 1
    },
    {
    "name": "rain of fire",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-rain-of-fire.jpeg",
    "initiative": 21,
    "level": 5
    },
    {
    "name": "return to the source",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-return-to-the-source.jpeg",
    "initiative": 14,
    "level": 6
    },
    {
    "name": "searing smoke",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-searing-smoke.jpeg",
    "initiative": 45,
    "level": 2
    },
    {
    "name": "stone armor",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-stone-armor.jpeg",
    "initiative": 9,
    "level": 9
    },
    {
    "name": "swelter",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-swelter.jpeg",
    "initiative": 32,
    "level": 7
    },
    {
    "name": "under pressure",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-under-pressure.jpeg",
    "initiative": 85,
    "level": 1
    },
    {
    "name": "wildfire",
    "class": "PY",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/PY/fh-wildfire.jpeg",
    "initiative": 72,
    "level": 1.5
    }
],
"SD": [
    {
    "name": "sd-back",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-sd-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "birds in a tempest",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-birds-in-a-tempest.jpeg",
    "initiative": 18,
    "level": 2
    },
    {
    "name": "biting frost",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-biting-frost.jpeg",
    "initiative": 16,
    "level": 4
    },
    {
    "name": "blinding vortex",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-blinding-vortex.jpeg",
    "initiative": 31,
    "level": 1.5
    },
    {
    "name": "blizzard",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-blizzard.jpeg",
    "initiative": 71,
    "level": 1
    },
    {
    "name": "chilling impact",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-chilling-impact.jpeg",
    "initiative": 31,
    "level": 1
    },
    {
    "name": "cold snap",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-cold-snap.jpeg",
    "initiative": 86,
    "level": 3
    },
    {
    "name": "cold therapy",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-cold-therapy.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "cross winds",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-cross-winds.jpeg",
    "initiative": 32,
    "level": 1
    },
    {
    "name": "enticing breeze",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-enticing-breeze.jpeg",
    "initiative": 76,
    "level": 1
    },
    {
    "name": "freezing storm",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-freezing-storm.jpeg",
    "initiative": 81,
    "level": 7
    },
    {
    "name": "frigid growth",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-frigid-growth.jpeg",
    "initiative": 70,
    "level": 1
    },
    {
    "name": "frozen brand",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-frozen-brand.jpeg",
    "initiative": 33,
    "level": 6
    },
    {
    "name": "gathering force",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-gathering-force.jpeg",
    "initiative": 89,
    "level": 1
    },
    {
    "name": "lifting gust",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-lifting-gust.jpeg",
    "initiative": 27,
    "level": 1
    },
    {
    "name": "nature's breath",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-natures-breath.jpeg",
    "initiative": 90,
    "level": 1
    },
    {
    "name": "polar vortex",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-polar-vortex.jpeg",
    "initiative": 61,
    "level": 3
    },
    {
    "name": "refreshing flurry",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-refreshing-flurry.jpeg",
    "initiative": 95,
    "level": 6
    },
    {
    "name": "shifting snow",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-shifting-snow.jpeg",
    "initiative": 17,
    "level": 5
    },
    {
    "name": "snowball",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-snowball.jpeg",
    "initiative": 23,
    "level": 1
    },
    {
    "name": "snowblind",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-snowblind.jpeg",
    "initiative": 83,
    "level": 9
    },
    {
    "name": "storm wall",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-storm-wall.jpeg",
    "initiative": 30,
    "level": 7
    },
    {
    "name": "surging blow",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-surging-blow.jpeg",
    "initiative": 73,
    "level": 8
    },
    {
    "name": "the endless white",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-the-endless-white.jpeg",
    "initiative": 5,
    "level": 8
    },
    {
    "name": "the spirit's call",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-the-spirits-call.jpeg",
    "initiative": 45,
    "level": 1.5
    },
    {
    "name": "tornado",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-tornado.jpeg",
    "initiative": 59,
    "level": 2
    },
    {
    "name": "whipping gale",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-whipping-gale.jpeg",
    "initiative": 79,
    "level": 5
    },
    {
    "name": "whiteout",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-whiteout.jpeg",
    "initiative": 21,
    "level": 1
    },
    {
    "name": "white winds",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-white-winds.jpeg",
    "initiative": 11,
    "level": 1.5
    },
    {
    "name": "winds of change",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-winds-of-change.jpeg",
    "initiative": 15,
    "level": 9
    },
    {
    "name": "zephyr barrier",
    "class": "SD",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SD/fh-zephyr-barrier.jpeg",
    "initiative": 40,
    "level": 4
    }
],
"SH": [
    {
    "name": "sh-back",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-sh-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "barbaric yawp",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-barbaric-yawp.jpeg",
    "initiative": 66,
    "level": 9
    },
    {
    "name": "befuddling bellow",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-befuddling-bellow.jpeg",
    "initiative": 18,
    "level": 2
    },
    {
    "name": "calamitous yawp",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-calamitous-yawp.jpeg",
    "initiative": 65,
    "level": 1.5
    },
    {
    "name": "cloaking refraction",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-cloaking-refraction.jpeg",
    "initiative": 11,
    "level": 7
    },
    {
    "name": "concentrated blast",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-concentrated-blast.jpeg",
    "initiative": 38,
    "level": 4
    },
    {
    "name": "devastating shout",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-devastating-shout.jpeg",
    "initiative": 68,
    "level": 1
    },
    {
    "name": "din of battle",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-din-of-battle.jpeg",
    "initiative": 14,
    "level": 1.5
    },
    {
    "name": "elemental pulse",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-elemental-pulse.jpeg",
    "initiative": 25,
    "level": 4
    },
    {
    "name": "empowering note",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-empowering-note.jpeg",
    "initiative": 45,
    "level": 5
    },
    {
    "name": "empowering pulse",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-empowering-pulse.jpeg",
    "initiative": 22,
    "level": 1
    },
    {
    "name": "feedback",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-feedback.jpeg",
    "initiative": 24,
    "level": 8
    },
    {
    "name": "forceful vibrations",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-forceful-vibrations.jpeg",
    "initiative": 27,
    "level": 1
    },
    {
    "name": "foreboding tremors",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-foreboding-tremors.jpeg",
    "initiative": 21,
    "level": 1
    },
    {
    "name": "future sense",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-future-sense.jpeg",
    "initiative": 28,
    "level": 6
    },
    {
    "name": "heartening harmony",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-heartening-harmony.jpeg",
    "initiative": 30,
    "level": 1
    },
    {
    "name": "illuminative tone",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-illuminative-tone.jpeg",
    "initiative": 72,
    "level": 1.5
    },
    {
    "name": "lifting voice",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-lifting-voice.jpeg",
    "initiative": 29,
    "level": 1
    },
    {
    "name": "precious gems",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-precious-gems.jpeg",
    "initiative": 10,
    "level": 1
    },
    {
    "name": "resonant frequency",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-resonant-frequency.jpeg",
    "initiative": 88,
    "level": 1
    },
    {
    "name": "shape the path",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-shape-the-path.jpeg",
    "initiative": 40,
    "level": 3
    },
    {
    "name": "shrieking chakram",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-shrieking-chakram.jpeg",
    "initiative": 8,
    "level": 5
    },
    {
    "name": "soft spots",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-soft-spots.jpeg",
    "initiative": 47,
    "level": 8
    },
    {
    "name": "sonic shock",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-sonic-shock.jpeg",
    "initiative": 58,
    "level": 1
    },
    {
    "name": "sound therapy",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-sound-therapy.jpeg",
    "initiative": 73,
    "level": 7
    },
    {
    "name": "stealth vibrations",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-stealth-vibrations.jpeg",
    "initiative": 35,
    "level": 3
    },
    {
    "name": "transparency",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-transparency.jpeg",
    "initiative": 13,
    "level": 2
    },
    {
    "name": "unrelenting wail",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-unrelenting-wail.jpeg",
    "initiative": 26,
    "level": 1
    },
    {
    "name": "unsustainable wave",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-unsustainable-wave.jpeg",
    "initiative": 36,
    "level": 6
    },
    {
    "name": "violent vibrations",
    "class": "SH",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/SH/fh-violent-vibrations.jpeg",
    "initiative": 5,
    "level": 9
    }
],
"TA": [
    {
    "name": "ta-back",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-ta-back.jpeg",
    "initiative": 0,
    "level": 0
    },
    {
    "name": "boar catcher",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-boar-catcher.jpeg",
    "initiative": 20,
    "level": 1
    },
    {
    "name": "cage of thorns",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-cage-of-thorns.jpeg",
    "initiative": 55,
    "level": 6
    },
    {
    "name": "caltrops",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-caltrops.jpeg",
    "initiative": 25,
    "level": 1
    },
    {
    "name": "dangerous cargo",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-dangerous-cargo.jpeg",
    "initiative": 23,
    "level": 9
    },
    {
    "name": "dangerous ground",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-dangerous-ground.jpeg",
    "initiative": 31,
    "level": 4
    },
    {
    "name": "dismantle",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-dismantle.jpeg",
    "initiative": 72,
    "level": 1.5
    },
    {
    "name": "electrified net",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-electrified-net.jpeg",
    "initiative": 53,
    "level": 1
    },
    {
    "name": "enticing bait",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-enticing-bait.jpeg",
    "initiative": 30,
    "level": 1
    },
    {
    "name": "exploding decoy",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-exploding-decoy.jpeg",
    "initiative": 62,
    "level": 1
    },
    {
    "name": "extra teeth",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-extra-teeth.jpeg",
    "initiative": 22,
    "level": 3
    },
    {
    "name": "flurry of nails",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-flurry-of-nails.jpeg",
    "initiative": 68,
    "level": 1
    },
    {
    "name": "foxhole",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-foxhole.jpeg",
    "initiative": 90,
    "level": 7
    },
    {
    "name": "furry facade",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-furry-facade.jpeg",
    "initiative": 85,
    "level": 1
    },
    {
    "name": "grasping hazards",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-grasping-hazards.jpeg",
    "initiative": 8,
    "level": 7
    },
    {
    "name": "honeypot",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-honeypot.jpeg",
    "initiative": 18,
    "level": 1
    },
    {
    "name": "improvised improvement",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-improvised-improvement.jpeg",
    "initiative": 58,
    "level": 1.5
    },
    {
    "name": "lure of the snare",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-lure-of-the-snare.jpeg",
    "initiative": 59,
    "level": 5
    },
    {
    "name": "magnetic shards",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-magnetic-shards.jpeg",
    "initiative": 37,
    "level": 8
    },
    {
    "name": "mother of all traps",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-mother-of-all-traps.jpeg",
    "initiative": 86,
    "level": 9
    },
    {
    "name": "path of pain",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-path-of-pain.jpeg",
    "initiative": 38,
    "level": 2
    },
    {
    "name": "persistent pitfalls",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-persistent-pitfalls.jpeg",
    "initiative": 13,
    "level": 6
    },
    {
    "name": "proficient hunter",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-proficient-hunter.jpeg",
    "initiative": 26,
    "level": 5
    },
    {
    "name": "pyrotechnics",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-pyrotechnics.jpeg",
    "initiative": 80,
    "level": 3
    },
    {
    "name": "spike pit",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-spike-pit.jpeg",
    "initiative": 47,
    "level": 1
    },
    {
    "name": "spike strip",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-spike-strip.jpeg",
    "initiative": 67,
    "level": 8
    },
    {
    "name": "spring-loaded",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-spring-loaded.jpeg",
    "initiative": 15,
    "level": 1.5
    },
    {
    "name": "stalker's spoils",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-stalkers-spoils.jpeg",
    "initiative": 10,
    "level": 4
    },
    {
    "name": "unavoidable outcome",
    "class": "TA",
    "game": "fh",
    "image": "character-ability-cards/frosthaven/TA/fh-unavoidable-outcome.jpeg",
    "initiative": 45,
    "level": 2
    }
]
}
