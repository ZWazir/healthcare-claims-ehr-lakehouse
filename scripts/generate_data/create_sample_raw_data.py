from __future__ import annotations

import random
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SYNTHEA_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "synthea"
SYNPuf_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "synpuf"

NUM_PATIENTS = 250
RANDOM_SEED = 42


CITY_PROFILES = [
    {
        "city": "Boston",
        "state": "Massachusetts",
        "county": "Suffolk County",
        "zip": "02108",
        "lat": "42.3601",
        "lon": "-71.0589",
        "state_code": "22",
        "county_code": "001",
    },
    {
        "city": "Springfield",
        "state": "Massachusetts",
        "county": "Hampden County",
        "zip": "01103",
        "lat": "42.1015",
        "lon": "-72.5898",
        "state_code": "22",
        "county_code": "013",
    },
    {
        "city": "Worcester",
        "state": "Massachusetts",
        "county": "Worcester County",
        "zip": "01608",
        "lat": "42.2626",
        "lon": "-71.8023",
        "state_code": "22",
        "county_code": "027",
    },
    {
        "city": "Lowell",
        "state": "Massachusetts",
        "county": "Middlesex County",
        "zip": "01852",
        "lat": "42.6334",
        "lon": "-71.3162",
        "state_code": "22",
        "county_code": "017",
    },
    {
        "city": "Cambridge",
        "state": "Massachusetts",
        "county": "Middlesex County",
        "zip": "02139",
        "lat": "42.3736",
        "lon": "-71.1097",
        "state_code": "22",
        "county_code": "017",
    },
]


MALE_FIRST_NAMES = [
    "James",
    "Robert",
    "Michael",
    "William",
    "David",
    "Joseph",
    "Thomas",
    "Daniel",
    "Matthew",
    "Anthony",
]

FEMALE_FIRST_NAMES = [
    "Maria",
    "Linda",
    "Patricia",
    "Barbara",
    "Elizabeth",
    "Jennifer",
    "Susan",
    "Karen",
    "Nancy",
    "Lisa",
]

LAST_NAMES = [
    "Wilson",
    "Garcia",
    "Johnson",
    "Brown",
    "Davis",
    "Miller",
    "Martinez",
    "Anderson",
    "Taylor",
    "Thomas",
    "Moore",
    "Jackson",
]


CONDITION_CATALOG = [
    {
        "code": "38341003",
        "description": "Hypertension",
        "icd9": "4019",
        "claim_flag": None,
        "med_code": "314076",
        "med_description": "Lisinopril 10 MG Oral Tablet",
        "base_med_cost": 12.50,
    },
    {
        "code": "44054006",
        "description": "Diabetes mellitus type 2",
        "icd9": "25000",
        "claim_flag": "SP_DIABETES",
        "med_code": "860975",
        "med_description": "Metformin hydrochloride 500 MG Oral Tablet",
        "base_med_cost": 9.25,
    },
    {
        "code": "88805009",
        "description": "Chronic congestive heart failure",
        "icd9": "4280",
        "claim_flag": "SP_CHF",
        "med_code": "310798",
        "med_description": "Furosemide 40 MG Oral Tablet",
        "base_med_cost": 11.40,
    },
    {
        "code": "709044004",
        "description": "Chronic kidney disease",
        "icd9": "5859",
        "claim_flag": "SP_CHRNKIDN",
        "med_code": "197361",
        "med_description": "Amlodipine 5 MG Oral Tablet",
        "base_med_cost": 10.75,
    },
    {
        "code": "13645005",
        "description": "Chronic obstructive bronchitis",
        "icd9": "496",
        "claim_flag": "SP_COPD",
        "med_code": "317136",
        "med_description": "Albuterol 0.09 MG/ACTUAT Metered Dose Inhaler",
        "base_med_cost": 38.20,
    },
    {
        "code": "35489007",
        "description": "Major depression disorder",
        "icd9": "311",
        "claim_flag": "SP_DEPRESSN",
        "med_code": "313580",
        "med_description": "Sertraline 50 MG Oral Tablet",
        "base_med_cost": 8.80,
    },
    {
        "code": "414545008",
        "description": "Ischemic heart disease",
        "icd9": "41401",
        "claim_flag": "SP_ISCHMCHT",
        "med_code": "617314",
        "med_description": "Atorvastatin 20 MG Oral Tablet",
        "base_med_cost": 14.10,
    },
    {
        "code": "64859006",
        "description": "Osteoporosis",
        "icd9": "73300",
        "claim_flag": "SP_OSTEOPRS",
        "med_code": "904431",
        "med_description": "Alendronate sodium 70 MG Oral Tablet",
        "base_med_cost": 7.90,
    },
    {
        "code": "69896004",
        "description": "Rheumatoid arthritis",
        "icd9": "7140",
        "claim_flag": "SP_RA_OA",
        "med_code": "308136",
        "med_description": "Methotrexate 2.5 MG Oral Tablet",
        "base_med_cost": 21.40,
    },
    {
        "code": "230690007",
        "description": "Stroke",
        "icd9": "43491",
        "claim_flag": "SP_STRKETIA",
        "med_code": "855332",
        "med_description": "Clopidogrel 75 MG Oral Tablet",
        "base_med_cost": 16.80,
    },
    {
        "code": "363346000",
        "description": "Malignant neoplastic disease",
        "icd9": "1991",
        "claim_flag": "SP_CNCR",
        "med_code": "105585",
        "med_description": "Ondansetron 4 MG Oral Tablet",
        "base_med_cost": 19.60,
    },
    {
        "code": "26929004",
        "description": "Alzheimer's disease",
        "icd9": "3310",
        "claim_flag": "SP_ALZHDMTA",
        "med_code": "135447",
        "med_description": "Donepezil 10 MG Oral Tablet",
        "base_med_cost": 13.30,
    },
]


CLAIM_FLAG_FIELDS = [
    "SP_ALZHDMTA",
    "SP_CHF",
    "SP_CHRNKIDN",
    "SP_CNCR",
    "SP_COPD",
    "SP_DEPRESSN",
    "SP_DIABETES",
    "SP_ISCHMCHT",
    "SP_OSTEOPRS",
    "SP_RA_OA",
    "SP_STRKETIA",
]


_PATIENT_PROFILES: list[dict] | None = None


def ensure_raw_directories_exist() -> None:
    """
    Create the raw data folders if they do not already exist.
    """
    SYNTHEA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    SYNPuf_RAW_DIR.mkdir(parents=True, exist_ok=True)


def format_yyyymmdd(value: date) -> str:
    """
    Format a Python date as a SynPUF-style YYYYMMDD string.
    """
    return value.strftime("%Y%m%d")


def format_synthea_datetime(value: date, hour: int) -> str:
    """
    Format a date as a Synthea-like UTC timestamp.
    """
    return datetime(value.year, value.month, value.day, hour, 30).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def risk_tier_for_patient(patient_number: int) -> str:
    """
    Assign deterministic risk tiers so the synthetic cohort has dashboard-friendly variation.
    """
    remainder = patient_number % 10

    if remainder in {0, 1}:
        return "high"
    if remainder in {2, 3, 4}:
        return "medium"
    return "low"


def choose_conditions(rng: random.Random, risk_tier: str) -> list[dict]:
    """
    Select a realistic number of chronic conditions based on synthetic risk tier.
    """
    if risk_tier == "low":
        condition_count = rng.choices([0, 1], weights=[0.65, 0.35])[0]
        candidate_pool = [
            CONDITION_CATALOG[0],
            CONDITION_CATALOG[5],
            CONDITION_CATALOG[7],
        ]
    elif risk_tier == "medium":
        condition_count = rng.choice([1, 2, 3])
        candidate_pool = CONDITION_CATALOG[:9]
    else:
        condition_count = rng.choice([3, 4, 5, 6])
        candidate_pool = CONDITION_CATALOG

    return rng.sample(candidate_pool, k=min(condition_count, len(candidate_pool)))


def create_claim_amounts(
    rng: random.Random,
    risk_tier: str,
    claim_type: str,
) -> list[dict]:
    """
    Generate synthetic claim amounts and dates for inpatient or outpatient claims.
    """
    if claim_type == "inpatient":
        if risk_tier == "low":
            claim_count = rng.choices([0, 1], weights=[0.94, 0.06])[0]
            amount_range = (2200, 5200)
            day_range = (1, 3)
        elif risk_tier == "medium":
            claim_count = rng.choices([0, 1], weights=[0.70, 0.30])[0]
            amount_range = (4200, 10500)
            day_range = (2, 5)
        else:
            claim_count = rng.choice([1, 1, 2, 3])
            amount_range = (8500, 26000)
            day_range = (3, 9)
    else:
        if risk_tier == "low":
            claim_count = rng.choice([0, 1, 1, 2])
            amount_range = (120, 850)
            day_range = (1, 1)
        elif risk_tier == "medium":
            claim_count = rng.choice([1, 2, 3, 4])
            amount_range = (350, 1800)
            day_range = (1, 1)
        else:
            claim_count = rng.choice([3, 4, 5, 6, 7, 8])
            amount_range = (900, 4500)
            day_range = (1, 2)

    claims = []

    for claim_index in range(1, claim_count + 1):
        service_date = date(2023, 1, 1) + timedelta(
            days=rng.randint(0, 330)
        )
        service_days = rng.randint(*day_range)
        claims.append(
            {
                "amount": rng.randint(*amount_range),
                "service_date": service_date,
                "service_days": service_days,
            }
        )

    return claims


def build_patient_profiles() -> list[dict]:
    """
    Build one deterministic linked EHR + claims cohort.

    The patient and beneficiary IDs intentionally share row order so downstream
    synthetic crosswalk logic can continue using row-number matching.
    """
    rng = random.Random(RANDOM_SEED)
    profiles = []

    for patient_number in range(1, NUM_PATIENTS + 1):
        risk_tier = risk_tier_for_patient(patient_number)
        gender = rng.choice(["M", "F"])
        sex_code = "1" if gender == "M" else "2"

        if rng.random() < 0.18:
            race = "white"
            ethnicity = "hispanic"
            race_code = "5"
        else:
            race, ethnicity, race_code = rng.choice(
                [
                    ("white", "nonhispanic", "1"),
                    ("black", "nonhispanic", "2"),
                    ("asian", "nonhispanic", "3"),
                    ("other", "nonhispanic", "3"),
                ]
            )

        if risk_tier == "low":
            age = rng.randint(28, 68)
            encounter_count = rng.choice([1, 1, 2])
        elif risk_tier == "medium":
            age = rng.randint(45, 78)
            encounter_count = rng.choice([2, 3, 4])
        else:
            age = rng.randint(60, 90)
            encounter_count = rng.choice([4, 5, 6, 7, 8])

        birthdate = date(
            2024 - age,
            rng.randint(1, 12),
            rng.randint(1, 28),
        )

        conditions = choose_conditions(rng, risk_tier)
        inpatient_claims = create_claim_amounts(rng, risk_tier, "inpatient")
        outpatient_claims = create_claim_amounts(rng, risk_tier, "outpatient")

        outpatient_total = sum(claim["amount"] for claim in outpatient_claims)
        inpatient_total = sum(claim["amount"] for claim in inpatient_claims)

        carrier_reimbursement = int(
            outpatient_total * rng.uniform(0.35, 0.80)
            + len(conditions) * rng.randint(75, 425)
        )

        city_profile = rng.choice(CITY_PROFILES)

        first_name = rng.choice(
            MALE_FIRST_NAMES if gender == "M" else FEMALE_FIRST_NAMES
        )
        last_name = rng.choice(LAST_NAMES)

        profiles.append(
            {
                "patient_number": patient_number,
                "ehr_patient_id": f"ehr-patient-{patient_number:03d}",
                "claim_beneficiary_id": f"claim-bene-{patient_number:03d}",
                "risk_tier": risk_tier,
                "gender": gender,
                "sex_code": sex_code,
                "race": race,
                "race_code": race_code,
                "ethnicity": ethnicity,
                "birthdate": birthdate,
                "age": age,
                "first_name": first_name,
                "last_name": last_name,
                "city_profile": city_profile,
                "conditions": conditions,
                "encounter_count": encounter_count,
                "inpatient_claims": inpatient_claims,
                "outpatient_claims": outpatient_claims,
                "inpatient_total": inpatient_total,
                "outpatient_total": outpatient_total,
                "carrier_reimbursement": carrier_reimbursement,
                "esrd_flag": "1"
                if any(c["claim_flag"] == "SP_CHRNKIDN" for c in conditions)
                and risk_tier == "high"
                and rng.random() < 0.25
                else "0",
            }
        )

    return profiles


def get_patient_profiles() -> list[dict]:
    """
    Return cached patient profiles so every generated table stays aligned.
    """
    global _PATIENT_PROFILES

    if _PATIENT_PROFILES is None:
        _PATIENT_PROFILES = build_patient_profiles()

    return _PATIENT_PROFILES


def create_synthea_patients() -> pd.DataFrame:
    """
    Create a Synthea-like patients table with a richer synthetic cohort.
    """
    rows = []

    for profile in get_patient_profiles():
        city_profile = profile["city_profile"]
        is_female = profile["gender"] == "F"

        rows.append(
            {
                "Id": profile["ehr_patient_id"],
                "BIRTHDATE": profile["birthdate"].isoformat(),
                "DEATHDATE": "",
                "SSN": f"999-12-{profile['patient_number']:04d}",
                "DRIVERS": f"S999{profile['patient_number']:05d}",
                "PASSPORT": f"X999{profile['patient_number']:05d}X",
                "PREFIX": "Ms." if is_female else "Mr.",
                "FIRST": profile["first_name"],
                "LAST": profile["last_name"],
                "SUFFIX": "",
                "MAIDEN": rng_maiden_name(profile) if is_female else "",
                "MARITAL": "M"
                if profile["patient_number"] % 3 != 0
                else "S",
                "RACE": profile["race"],
                "ETHNICITY": profile["ethnicity"],
                "GENDER": profile["gender"],
                "BIRTHPLACE": f"{city_profile['city']} {city_profile['state']} US",
                "ADDRESS": f"{100 + profile['patient_number']} Main St",
                "CITY": city_profile["city"],
                "STATE": city_profile["state"],
                "COUNTY": city_profile["county"],
                "ZIP": city_profile["zip"],
                "LAT": city_profile["lat"],
                "LON": city_profile["lon"],
            }
        )

    return pd.DataFrame(rows)


def rng_maiden_name(profile: dict) -> str:
    """
    Provide deterministic maiden-name variation for Synthea-like demographics.
    """
    if profile["patient_number"] % 4 == 0:
        return LAST_NAMES[profile["patient_number"] % len(LAST_NAMES)]

    return ""


def create_synthea_encounters() -> pd.DataFrame:
    """
    Create a Synthea-like encounters table with utilization variation.
    """
    rows = []

    for profile in get_patient_profiles():
        patient_number = profile["patient_number"]
        conditions = profile["conditions"]

        for encounter_number in range(1, profile["encounter_count"] + 1):
            encounter_date = date(2023, 1, 1) + timedelta(
                days=((patient_number * 7) + (encounter_number * 23)) % 335
            )

            if profile["risk_tier"] == "high" and encounter_number % 4 == 0:
                encounter_class = "emergency"
                base_cost = 650
                total_cost = random.Random(
                    RANDOM_SEED + patient_number + encounter_number
                ).randint(2200, 7500)
            elif encounter_number % 3 == 0:
                encounter_class = "outpatient"
                base_cost = 240
                total_cost = random.Random(
                    RANDOM_SEED + patient_number + encounter_number
                ).randint(500, 1800)
            else:
                encounter_class = "ambulatory"
                base_cost = 130
                total_cost = random.Random(
                    RANDOM_SEED + patient_number + encounter_number
                ).randint(125, 700)

            reason = (
                conditions[(encounter_number - 1) % len(conditions)]
                if conditions
                else None
            )

            rows.append(
                {
                    "Id": f"enc-{patient_number:03d}-{encounter_number:02d}",
                    "START": format_synthea_datetime(encounter_date, 9),
                    "STOP": format_synthea_datetime(encounter_date, 10),
                    "PATIENT": profile["ehr_patient_id"],
                    "ORGANIZATION": f"org-{(patient_number % 5) + 1:03d}",
                    "PROVIDER": f"provider-{(patient_number % 25) + 1:03d}",
                    "PAYER": f"payer-{(patient_number % 3) + 1:03d}",
                    "ENCOUNTERCLASS": encounter_class,
                    "CODE": "185349003"
                    if encounter_class == "ambulatory"
                    else "308335008"
                    if encounter_class == "outpatient"
                    else "50849002",
                    "DESCRIPTION": "Encounter for check up"
                    if encounter_class == "ambulatory"
                    else "Patient encounter procedure"
                    if encounter_class == "outpatient"
                    else "Emergency room admission",
                    "BASE_ENCOUNTER_COST": f"{base_cost:.2f}",
                    "TOTAL_CLAIM_COST": f"{total_cost:.2f}",
                    "PAYER_COVERAGE": f"{total_cost * 0.78:.2f}",
                    "REASONCODE": reason["code"] if reason else "",
                    "REASONDESCRIPTION": reason["description"] if reason else "",
                }
            )

    return pd.DataFrame(rows)


def create_synthea_conditions() -> pd.DataFrame:
    """
    Create a Synthea-like conditions table with varied chronic burden.
    """
    rows = []

    for profile in get_patient_profiles():
        patient_number = profile["patient_number"]

        for condition_index, condition in enumerate(profile["conditions"], start=1):
            start_date = date(2020, 1, 1) + timedelta(
                days=((patient_number * 17) + (condition_index * 41)) % 900
            )

            rows.append(
                {
                    "START": start_date.isoformat(),
                    "STOP": "",
                    "PATIENT": profile["ehr_patient_id"],
                    "ENCOUNTER": f"enc-{patient_number:03d}-01",
                    "CODE": condition["code"],
                    "DESCRIPTION": condition["description"],
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "START",
            "STOP",
            "PATIENT",
            "ENCOUNTER",
            "CODE",
            "DESCRIPTION",
        ],
    )


def create_synthea_medications() -> pd.DataFrame:
    """
    Create a Synthea-like medications table tied to diagnosed conditions.
    """
    rows = []

    for profile in get_patient_profiles():
        patient_number = profile["patient_number"]

        for med_index, condition in enumerate(profile["conditions"], start=1):
            start_date = date(2021, 1, 1) + timedelta(
                days=((patient_number * 13) + (med_index * 29)) % 700
            )
            dispenses = 6 if profile["risk_tier"] == "low" else 12
            total_cost = condition["base_med_cost"] * dispenses

            rows.append(
                {
                    "START": start_date.isoformat(),
                    "STOP": "",
                    "PATIENT": profile["ehr_patient_id"],
                    "PAYER": f"payer-{(patient_number % 3) + 1:03d}",
                    "ENCOUNTER": f"enc-{patient_number:03d}-01",
                    "CODE": condition["med_code"],
                    "DESCRIPTION": condition["med_description"],
                    "BASE_COST": f"{condition['base_med_cost']:.2f}",
                    "PAYER_COVERAGE": f"{condition['base_med_cost'] * 0.70:.2f}",
                    "DISPENSES": str(dispenses),
                    "TOTALCOST": f"{total_cost:.2f}",
                    "REASONCODE": condition["code"],
                    "REASONDESCRIPTION": condition["description"],
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "START",
            "STOP",
            "PATIENT",
            "PAYER",
            "ENCOUNTER",
            "CODE",
            "DESCRIPTION",
            "BASE_COST",
            "PAYER_COVERAGE",
            "DISPENSES",
            "TOTALCOST",
            "REASONCODE",
            "REASONDESCRIPTION",
        ],
    )


def create_synthea_observations() -> pd.DataFrame:
    """
    Create a Synthea-like observations table with basic clinical measurements.
    """
    rows = []

    for profile in get_patient_profiles():
        patient_number = profile["patient_number"]
        observation_date = date(2023, 6, 1) + timedelta(days=patient_number % 120)
        condition_descriptions = {
            condition["description"] for condition in profile["conditions"]
        }

        if profile["risk_tier"] == "high":
            systolic_bp = 138 + (patient_number % 28)
            bmi = 29 + (patient_number % 9)
        elif profile["risk_tier"] == "medium":
            systolic_bp = 122 + (patient_number % 22)
            bmi = 25 + (patient_number % 7)
        else:
            systolic_bp = 106 + (patient_number % 20)
            bmi = 21 + (patient_number % 6)

        rows.append(
            {
                "DATE": observation_date.isoformat(),
                "PATIENT": profile["ehr_patient_id"],
                "ENCOUNTER": f"enc-{patient_number:03d}-01",
                "CODE": "8480-6",
                "DESCRIPTION": "Systolic Blood Pressure",
                "VALUE": str(systolic_bp),
                "UNITS": "mmHg",
                "TYPE": "numeric",
            }
        )

        rows.append(
            {
                "DATE": observation_date.isoformat(),
                "PATIENT": profile["ehr_patient_id"],
                "ENCOUNTER": f"enc-{patient_number:03d}-01",
                "CODE": "39156-5",
                "DESCRIPTION": "Body Mass Index",
                "VALUE": str(bmi),
                "UNITS": "kg/m2",
                "TYPE": "numeric",
            }
        )

        if "Diabetes mellitus type 2" in condition_descriptions:
            rows.append(
                {
                    "DATE": observation_date.isoformat(),
                    "PATIENT": profile["ehr_patient_id"],
                    "ENCOUNTER": f"enc-{patient_number:03d}-01",
                    "CODE": "4548-4",
                    "DESCRIPTION": "Hemoglobin A1c/Hemoglobin.total in Blood",
                    "VALUE": f"{6.4 + (patient_number % 25) / 10:.1f}",
                    "UNITS": "%",
                    "TYPE": "numeric",
                }
            )

        if "Chronic congestive heart failure" in condition_descriptions:
            rows.append(
                {
                    "DATE": observation_date.isoformat(),
                    "PATIENT": profile["ehr_patient_id"],
                    "ENCOUNTER": f"enc-{patient_number:03d}-01",
                    "CODE": "33762-6",
                    "DESCRIPTION": "Natriuretic peptide.B prohormone N-Terminal",
                    "VALUE": str(480 + (patient_number % 900)),
                    "UNITS": "pg/mL",
                    "TYPE": "numeric",
                }
            )

        if "Chronic kidney disease" in condition_descriptions:
            rows.append(
                {
                    "DATE": observation_date.isoformat(),
                    "PATIENT": profile["ehr_patient_id"],
                    "ENCOUNTER": f"enc-{patient_number:03d}-01",
                    "CODE": "33914-3",
                    "DESCRIPTION": "Glomerular filtration rate/1.73 sq M.predicted",
                    "VALUE": str(30 + (patient_number % 45)),
                    "UNITS": "mL/min",
                    "TYPE": "numeric",
                }
            )

    return pd.DataFrame(rows)


def create_synpuf_beneficiary_summary() -> pd.DataFrame:
    """
    Create a SynPUF-like beneficiary summary table aligned to EHR patients.
    """
    rows = []

    for profile in get_patient_profiles():
        flags = {flag: "0" for flag in CLAIM_FLAG_FIELDS}

        for condition in profile["conditions"]:
            if condition["claim_flag"]:
                flags[condition["claim_flag"]] = "1"

        inpatient_total = profile["inpatient_total"]
        outpatient_total = profile["outpatient_total"]
        carrier_total = profile["carrier_reimbursement"]

        city_profile = profile["city_profile"]

        rows.append(
            {
                "DESYNPUF_ID": profile["claim_beneficiary_id"],
                "BENE_BIRTH_DT": format_yyyymmdd(profile["birthdate"]),
                "BENE_DEATH_DT": "",
                "BENE_SEX_IDENT_CD": profile["sex_code"],
                "BENE_RACE_CD": profile["race_code"],
                "BENE_ESRD_IND": profile["esrd_flag"],
                "SP_STATE_CODE": city_profile["state_code"],
                "BENE_COUNTY_CD": city_profile["county_code"],
                "BENE_HI_CVRAGE_TOT_MONS": "12",
                "BENE_SMI_CVRAGE_TOT_MONS": "12",
                "BENE_HMO_CVRAGE_TOT_MONS": "0",
                "PLAN_CVRG_MOS_NUM": "12",
                "SP_ALZHDMTA": flags["SP_ALZHDMTA"],
                "SP_CHF": flags["SP_CHF"],
                "SP_CHRNKIDN": flags["SP_CHRNKIDN"],
                "SP_CNCR": flags["SP_CNCR"],
                "SP_COPD": flags["SP_COPD"],
                "SP_DEPRESSN": flags["SP_DEPRESSN"],
                "SP_DIABETES": flags["SP_DIABETES"],
                "SP_ISCHMCHT": flags["SP_ISCHMCHT"],
                "SP_OSTEOPRS": flags["SP_OSTEOPRS"],
                "SP_RA_OA": flags["SP_RA_OA"],
                "SP_STRKETIA": flags["SP_STRKETIA"],
                "MEDREIMB_IP": str(inpatient_total),
                "BENRES_IP": str(int(inpatient_total * 0.13)),
                "PPPYMT_IP": "0",
                "MEDREIMB_OP": str(outpatient_total),
                "BENRES_OP": str(int(outpatient_total * 0.12)),
                "PPPYMT_OP": "0",
                "MEDREIMB_CAR": str(carrier_total),
                "BENRES_CAR": str(int(carrier_total * 0.10)),
                "PPPYMT_CAR": "0",
            }
        )

    return pd.DataFrame(rows)


def create_synpuf_inpatient_claims() -> pd.DataFrame:
    """
    Create a SynPUF-like inpatient claims table with high-cost utilization variation.
    """
    rows = []

    for profile in get_patient_profiles():
        patient_number = profile["patient_number"]
        primary_condition = (
            profile["conditions"][0] if profile["conditions"] else CONDITION_CATALOG[0]
        )

        for claim_index, claim in enumerate(profile["inpatient_claims"], start=1):
            from_date = claim["service_date"]
            thru_date = from_date + timedelta(days=claim["service_days"])

            rows.append(
                {
                    "DESYNPUF_ID": profile["claim_beneficiary_id"],
                    "CLM_ID": f"ip-claim-{patient_number:03d}-{claim_index:02d}",
                    "SEGMENT": "1",
                    "CLM_FROM_DT": format_yyyymmdd(from_date),
                    "CLM_THRU_DT": format_yyyymmdd(thru_date),
                    "PRVDR_NUM": f"provider-{(patient_number % 25) + 1:03d}",
                    "CLM_PMT_AMT": str(claim["amount"]),
                    "NCH_PRMRY_PYR_CLM_PD_AMT": "0",
                    "AT_PHYSN_NPI": f"npi-{patient_number:03d}",
                    "OP_PHYSN_NPI": f"npi-{patient_number + 100:03d}",
                    "OT_PHYSN_NPI": "",
                    "CLM_ADMSN_DT": format_yyyymmdd(from_date),
                    "ADMTNG_ICD9_DGNS_CD": primary_condition["icd9"],
                    "CLM_PASS_THRU_PER_DIEM_AMT": "0",
                    "NCH_BENE_IP_DDCTBL_AMT": str(int(claim["amount"] * 0.13)),
                    "NCH_BENE_PTA_COINSRNC_LBLTY_AM": "0",
                    "NCH_BENE_BLOOD_DDCTBL_LBLTY_AM": "0",
                    "CLM_UTLZTN_DAY_CNT": str(claim["service_days"]),
                    "NCH_BENE_DSCHRG_DT": format_yyyymmdd(thru_date),
                    "CLM_DRG_CD": str(280 + (patient_number % 35)),
                    "ICD9_DGNS_CD_1": primary_condition["icd9"],
                    "ICD9_DGNS_CD_2": profile["conditions"][1]["icd9"]
                    if len(profile["conditions"]) > 1
                    else "",
                    "ICD9_DGNS_CD_3": profile["conditions"][2]["icd9"]
                    if len(profile["conditions"]) > 2
                    else "",
                    "ICD9_PRCDR_CD_1": "3893",
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "DESYNPUF_ID",
            "CLM_ID",
            "SEGMENT",
            "CLM_FROM_DT",
            "CLM_THRU_DT",
            "PRVDR_NUM",
            "CLM_PMT_AMT",
            "NCH_PRMRY_PYR_CLM_PD_AMT",
            "AT_PHYSN_NPI",
            "OP_PHYSN_NPI",
            "OT_PHYSN_NPI",
            "CLM_ADMSN_DT",
            "ADMTNG_ICD9_DGNS_CD",
            "CLM_PASS_THRU_PER_DIEM_AMT",
            "NCH_BENE_IP_DDCTBL_AMT",
            "NCH_BENE_PTA_COINSRNC_LBLTY_AM",
            "NCH_BENE_BLOOD_DDCTBL_LBLTY_AM",
            "CLM_UTLZTN_DAY_CNT",
            "NCH_BENE_DSCHRG_DT",
            "CLM_DRG_CD",
            "ICD9_DGNS_CD_1",
            "ICD9_DGNS_CD_2",
            "ICD9_DGNS_CD_3",
            "ICD9_PRCDR_CD_1",
        ],
    )


def create_synpuf_outpatient_claims() -> pd.DataFrame:
    """
    Create a SynPUF-like outpatient claims table with varied ambulatory utilization.
    """
    rows = []

    for profile in get_patient_profiles():
        patient_number = profile["patient_number"]
        primary_condition = (
            profile["conditions"][0] if profile["conditions"] else CONDITION_CATALOG[0]
        )

        for claim_index, claim in enumerate(profile["outpatient_claims"], start=1):
            from_date = claim["service_date"]
            thru_date = from_date + timedelta(days=claim["service_days"] - 1)

            rows.append(
                {
                    "DESYNPUF_ID": profile["claim_beneficiary_id"],
                    "CLM_ID": f"op-claim-{patient_number:03d}-{claim_index:02d}",
                    "SEGMENT": "1",
                    "CLM_FROM_DT": format_yyyymmdd(from_date),
                    "CLM_THRU_DT": format_yyyymmdd(thru_date),
                    "PRVDR_NUM": f"provider-{(patient_number % 25) + 1:03d}",
                    "CLM_PMT_AMT": str(claim["amount"]),
                    "NCH_PRMRY_PYR_CLM_PD_AMT": "0",
                    "AT_PHYSN_NPI": f"npi-{patient_number:03d}",
                    "OP_PHYSN_NPI": "",
                    "OT_PHYSN_NPI": "",
                    "ICD9_DGNS_CD_1": primary_condition["icd9"],
                }
            )

    return pd.DataFrame(
        rows,
        columns=[
            "DESYNPUF_ID",
            "CLM_ID",
            "SEGMENT",
            "CLM_FROM_DT",
            "CLM_THRU_DT",
            "PRVDR_NUM",
            "CLM_PMT_AMT",
            "NCH_PRMRY_PYR_CLM_PD_AMT",
            "AT_PHYSN_NPI",
            "OP_PHYSN_NPI",
            "OT_PHYSN_NPI",
            "ICD9_DGNS_CD_1",
        ],
    )


def write_csv(df: pd.DataFrame, output_path: Path) -> None:
    """
    Write a DataFrame to CSV and print a simple confirmation.
    """
    df.to_csv(output_path, index=False)
    print(f"Wrote {output_path} with {len(df):,} rows")


def main() -> None:
    ensure_raw_directories_exist()

    synthea_tables = {
        "patients.csv": create_synthea_patients(),
        "encounters.csv": create_synthea_encounters(),
        "conditions.csv": create_synthea_conditions(),
        "medications.csv": create_synthea_medications(),
        "observations.csv": create_synthea_observations(),
    }

    synpuf_tables = {
        "beneficiary_summary.csv": create_synpuf_beneficiary_summary(),
        "inpatient_claims.csv": create_synpuf_inpatient_claims(),
        "outpatient_claims.csv": create_synpuf_outpatient_claims(),
    }

    for file_name, df in synthea_tables.items():
        write_csv(df, SYNTHEA_RAW_DIR / file_name)

    for file_name, df in synpuf_tables.items():
        write_csv(df, SYNPuf_RAW_DIR / file_name)


if __name__ == "__main__":
    main()