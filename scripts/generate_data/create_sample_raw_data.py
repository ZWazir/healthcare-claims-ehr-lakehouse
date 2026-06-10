from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SYNTHEA_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "synthea"
SYNPuf_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "synpuf"


def ensure_raw_directories_exist() -> None:
    """
    Create the raw data folders if they do not already exist.
    """
    SYNTHEA_RAW_DIR.mkdir(parents=True, exist_ok=True)
    SYNPuf_RAW_DIR.mkdir(parents=True, exist_ok=True)


def create_synthea_patients() -> pd.DataFrame:
    """
    Create a small Synthea-like patients table.

    This represents the EHR patient demographic source.
    """
    return pd.DataFrame(
        [
            {
                "Id": "ehr-patient-001",
                "BIRTHDATE": "1952-04-12",
                "DEATHDATE": "",
                "SSN": "999-12-0001",
                "DRIVERS": "S99900001",
                "PASSPORT": "X99900001X",
                "PREFIX": "Mr.",
                "FIRST": "James",
                "LAST": "Wilson",
                "SUFFIX": "",
                "MAIDEN": "",
                "MARITAL": "M",
                "RACE": "white",
                "ETHNICITY": "nonhispanic",
                "GENDER": "M",
                "BIRTHPLACE": "Boston Massachusetts US",
                "ADDRESS": "100 Main St",
                "CITY": "Boston",
                "STATE": "Massachusetts",
                "COUNTY": "Suffolk County",
                "ZIP": "02108",
                "LAT": "42.3601",
                "LON": "-71.0589",
            },
            {
                "Id": "ehr-patient-002",
                "BIRTHDATE": "1960-09-25",
                "DEATHDATE": "",
                "SSN": "999-12-0002",
                "DRIVERS": "S99900002",
                "PASSPORT": "X99900002X",
                "PREFIX": "Mrs.",
                "FIRST": "Maria",
                "LAST": "Garcia",
                "SUFFIX": "",
                "MAIDEN": "Lopez",
                "MARITAL": "M",
                "RACE": "white",
                "ETHNICITY": "hispanic",
                "GENDER": "F",
                "BIRTHPLACE": "Springfield Massachusetts US",
                "ADDRESS": "200 Oak Ave",
                "CITY": "Springfield",
                "STATE": "Massachusetts",
                "COUNTY": "Hampden County",
                "ZIP": "01103",
                "LAT": "42.1015",
                "LON": "-72.5898",
            },
            {
                "Id": "ehr-patient-003",
                "BIRTHDATE": "1948-01-03",
                "DEATHDATE": "",
                "SSN": "999-12-0003",
                "DRIVERS": "S99900003",
                "PASSPORT": "X99900003X",
                "PREFIX": "Ms.",
                "FIRST": "Linda",
                "LAST": "Johnson",
                "SUFFIX": "",
                "MAIDEN": "",
                "MARITAL": "S",
                "RACE": "black",
                "ETHNICITY": "nonhispanic",
                "GENDER": "F",
                "BIRTHPLACE": "Worcester Massachusetts US",
                "ADDRESS": "300 Pine Rd",
                "CITY": "Worcester",
                "STATE": "Massachusetts",
                "COUNTY": "Worcester County",
                "ZIP": "01608",
                "LAT": "42.2626",
                "LON": "-71.8023",
            },
        ]
    )


def create_synthea_encounters() -> pd.DataFrame:
    """
    Create a small Synthea-like encounters table.

    This represents clinical visits in the EHR.
    """
    return pd.DataFrame(
        [
            {
                "Id": "enc-001",
                "START": "2023-01-10T09:30:00Z",
                "STOP": "2023-01-10T10:10:00Z",
                "PATIENT": "ehr-patient-001",
                "ORGANIZATION": "org-001",
                "PROVIDER": "provider-001",
                "PAYER": "payer-001",
                "ENCOUNTERCLASS": "ambulatory",
                "CODE": "185349003",
                "DESCRIPTION": "Encounter for check up",
                "BASE_ENCOUNTER_COST": "129.16",
                "TOTAL_CLAIM_COST": "129.16",
                "PAYER_COVERAGE": "89.16",
                "REASONCODE": "",
                "REASONDESCRIPTION": "",
            },
            {
                "Id": "enc-002",
                "START": "2023-02-14T14:00:00Z",
                "STOP": "2023-02-14T15:00:00Z",
                "PATIENT": "ehr-patient-002",
                "ORGANIZATION": "org-001",
                "PROVIDER": "provider-002",
                "PAYER": "payer-001",
                "ENCOUNTERCLASS": "outpatient",
                "CODE": "308335008",
                "DESCRIPTION": "Patient encounter procedure",
                "BASE_ENCOUNTER_COST": "212.45",
                "TOTAL_CLAIM_COST": "415.30",
                "PAYER_COVERAGE": "320.30",
                "REASONCODE": "44054006",
                "REASONDESCRIPTION": "Diabetes mellitus type 2",
            },
            {
                "Id": "enc-003",
                "START": "2023-03-19T20:15:00Z",
                "STOP": "2023-03-20T02:45:00Z",
                "PATIENT": "ehr-patient-003",
                "ORGANIZATION": "org-002",
                "PROVIDER": "provider-003",
                "PAYER": "payer-002",
                "ENCOUNTERCLASS": "emergency",
                "CODE": "50849002",
                "DESCRIPTION": "Emergency room admission",
                "BASE_ENCOUNTER_COST": "598.22",
                "TOTAL_CLAIM_COST": "2750.00",
                "PAYER_COVERAGE": "2100.00",
                "REASONCODE": "88805009",
                "REASONDESCRIPTION": "Chronic congestive heart failure",
            },
        ]
    )


def create_synthea_conditions() -> pd.DataFrame:
    """
    Create a small Synthea-like conditions table.

    This represents diagnoses and chronic conditions.
    """
    return pd.DataFrame(
        [
            {
                "START": "2022-05-01",
                "STOP": "",
                "PATIENT": "ehr-patient-001",
                "ENCOUNTER": "enc-001",
                "CODE": "38341003",
                "DESCRIPTION": "Hypertension",
            },
            {
                "START": "2021-08-13",
                "STOP": "",
                "PATIENT": "ehr-patient-002",
                "ENCOUNTER": "enc-002",
                "CODE": "44054006",
                "DESCRIPTION": "Diabetes mellitus type 2",
            },
            {
                "START": "2020-11-20",
                "STOP": "",
                "PATIENT": "ehr-patient-003",
                "ENCOUNTER": "enc-003",
                "CODE": "88805009",
                "DESCRIPTION": "Chronic congestive heart failure",
            },
        ]
    )


def create_synthea_medications() -> pd.DataFrame:
    """
    Create a small Synthea-like medications table.

    This represents prescribed medications from the EHR.
    """
    return pd.DataFrame(
        [
            {
                "START": "2022-05-01",
                "STOP": "",
                "PATIENT": "ehr-patient-001",
                "PAYER": "payer-001",
                "ENCOUNTER": "enc-001",
                "CODE": "314076",
                "DESCRIPTION": "Lisinopril 10 MG Oral Tablet",
                "BASE_COST": "12.50",
                "PAYER_COVERAGE": "8.00",
                "DISPENSES": "12",
                "TOTALCOST": "150.00",
                "REASONCODE": "38341003",
                "REASONDESCRIPTION": "Hypertension",
            },
            {
                "START": "2021-08-13",
                "STOP": "",
                "PATIENT": "ehr-patient-002",
                "PAYER": "payer-001",
                "ENCOUNTER": "enc-002",
                "CODE": "860975",
                "DESCRIPTION": "Metformin hydrochloride 500 MG Oral Tablet",
                "BASE_COST": "9.25",
                "PAYER_COVERAGE": "6.25",
                "DISPENSES": "12",
                "TOTALCOST": "111.00",
                "REASONCODE": "44054006",
                "REASONDESCRIPTION": "Diabetes mellitus type 2",
            },
            {
                "START": "2020-11-20",
                "STOP": "",
                "PATIENT": "ehr-patient-003",
                "PAYER": "payer-002",
                "ENCOUNTER": "enc-003",
                "CODE": "310798",
                "DESCRIPTION": "Furosemide 40 MG Oral Tablet",
                "BASE_COST": "11.40",
                "PAYER_COVERAGE": "7.40",
                "DISPENSES": "12",
                "TOTALCOST": "136.80",
                "REASONCODE": "88805009",
                "REASONDESCRIPTION": "Chronic congestive heart failure",
            },
        ]
    )


def create_synthea_observations() -> pd.DataFrame:
    """
    Create a small Synthea-like observations table.

    This represents lab results and clinical measurements.
    """
    return pd.DataFrame(
        [
            {
                "DATE": "2023-01-10",
                "PATIENT": "ehr-patient-001",
                "ENCOUNTER": "enc-001",
                "CODE": "8480-6",
                "DESCRIPTION": "Systolic Blood Pressure",
                "VALUE": "145",
                "UNITS": "mmHg",
                "TYPE": "numeric",
            },
            {
                "DATE": "2023-02-14",
                "PATIENT": "ehr-patient-002",
                "ENCOUNTER": "enc-002",
                "CODE": "4548-4",
                "DESCRIPTION": "Hemoglobin A1c/Hemoglobin.total in Blood",
                "VALUE": "8.1",
                "UNITS": "%",
                "TYPE": "numeric",
            },
            {
                "DATE": "2023-03-19",
                "PATIENT": "ehr-patient-003",
                "ENCOUNTER": "enc-003",
                "CODE": "33762-6",
                "DESCRIPTION": "Natriuretic peptide.B prohormone N-Terminal",
                "VALUE": "950",
                "UNITS": "pg/mL",
                "TYPE": "numeric",
            },
        ]
    )


def create_synpuf_beneficiary_summary() -> pd.DataFrame:
    """
    Create a small SynPUF-like beneficiary summary table.

    This represents the claims-side beneficiary demographics.
    """
    return pd.DataFrame(
        [
            {
                "DESYNPUF_ID": "claim-bene-001",
                "BENE_BIRTH_DT": "19520412",
                "BENE_DEATH_DT": "",
                "BENE_SEX_IDENT_CD": "1",
                "BENE_RACE_CD": "1",
                "BENE_ESRD_IND": "0",
                "SP_STATE_CODE": "22",
                "BENE_COUNTY_CD": "001",
                "BENE_HI_CVRAGE_TOT_MONS": "12",
                "BENE_SMI_CVRAGE_TOT_MONS": "12",
                "BENE_HMO_CVRAGE_TOT_MONS": "0",
                "PLAN_CVRG_MOS_NUM": "12",
                "SP_ALZHDMTA": "0",
                "SP_CHF": "0",
                "SP_CHRNKIDN": "0",
                "SP_CNCR": "0",
                "SP_COPD": "0",
                "SP_DEPRESSN": "0",
                "SP_DIABETES": "0",
                "SP_ISCHMCHT": "0",
                "SP_OSTEOPRS": "0",
                "SP_RA_OA": "0",
                "SP_STRKETIA": "0",
                "MEDREIMB_IP": "0",
                "BENRES_IP": "0",
                "PPPYMT_IP": "0",
                "MEDREIMB_OP": "550",
                "BENRES_OP": "70",
                "PPPYMT_OP": "0",
                "MEDREIMB_CAR": "320",
                "BENRES_CAR": "40",
                "PPPYMT_CAR": "0",
            },
            {
                "DESYNPUF_ID": "claim-bene-002",
                "BENE_BIRTH_DT": "19600925",
                "BENE_DEATH_DT": "",
                "BENE_SEX_IDENT_CD": "2",
                "BENE_RACE_CD": "5",
                "BENE_ESRD_IND": "0",
                "SP_STATE_CODE": "22",
                "BENE_COUNTY_CD": "013",
                "BENE_HI_CVRAGE_TOT_MONS": "12",
                "BENE_SMI_CVRAGE_TOT_MONS": "12",
                "BENE_HMO_CVRAGE_TOT_MONS": "0",
                "PLAN_CVRG_MOS_NUM": "12",
                "SP_ALZHDMTA": "0",
                "SP_CHF": "0",
                "SP_CHRNKIDN": "0",
                "SP_CNCR": "0",
                "SP_COPD": "0",
                "SP_DEPRESSN": "0",
                "SP_DIABETES": "1",
                "SP_ISCHMCHT": "0",
                "SP_OSTEOPRS": "0",
                "SP_RA_OA": "0",
                "SP_STRKETIA": "0",
                "MEDREIMB_IP": "0",
                "BENRES_IP": "0",
                "PPPYMT_IP": "0",
                "MEDREIMB_OP": "900",
                "BENRES_OP": "110",
                "PPPYMT_OP": "0",
                "MEDREIMB_CAR": "480",
                "BENRES_CAR": "60",
                "PPPYMT_CAR": "0",
            },
            {
                "DESYNPUF_ID": "claim-bene-003",
                "BENE_BIRTH_DT": "19480103",
                "BENE_DEATH_DT": "",
                "BENE_SEX_IDENT_CD": "2",
                "BENE_RACE_CD": "2",
                "BENE_ESRD_IND": "0",
                "SP_STATE_CODE": "22",
                "BENE_COUNTY_CD": "027",
                "BENE_HI_CVRAGE_TOT_MONS": "12",
                "BENE_SMI_CVRAGE_TOT_MONS": "12",
                "BENE_HMO_CVRAGE_TOT_MONS": "0",
                "PLAN_CVRG_MOS_NUM": "12",
                "SP_ALZHDMTA": "0",
                "SP_CHF": "1",
                "SP_CHRNKIDN": "1",
                "SP_CNCR": "0",
                "SP_COPD": "1",
                "SP_DEPRESSN": "1",
                "SP_DIABETES": "1",
                "SP_ISCHMCHT": "1",
                "SP_OSTEOPRS": "0",
                "SP_RA_OA": "1",
                "SP_STRKETIA": "0",
                "MEDREIMB_IP": "8500",
                "BENRES_IP": "1100",
                "PPPYMT_IP": "0",
                "MEDREIMB_OP": "2400",
                "BENRES_OP": "310",
                "PPPYMT_OP": "0",
                "MEDREIMB_CAR": "1800",
                "BENRES_CAR": "260",
                "PPPYMT_CAR": "0",
            },
        ]
    )


def create_synpuf_inpatient_claims() -> pd.DataFrame:
    """
    Create a small SynPUF-like inpatient claims table.
    """
    return pd.DataFrame(
        [
            {
                "DESYNPUF_ID": "claim-bene-003",
                "CLM_ID": "ip-claim-001",
                "SEGMENT": "1",
                "CLM_FROM_DT": "20230319",
                "CLM_THRU_DT": "20230322",
                "PRVDR_NUM": "provider-003",
                "CLM_PMT_AMT": "8500",
                "NCH_PRMRY_PYR_CLM_PD_AMT": "0",
                "AT_PHYSN_NPI": "npi-003",
                "OP_PHYSN_NPI": "npi-103",
                "OT_PHYSN_NPI": "",
                "CLM_ADMSN_DT": "20230319",
                "ADMTNG_ICD9_DGNS_CD": "4280",
                "CLM_PASS_THRU_PER_DIEM_AMT": "0",
                "NCH_BENE_IP_DDCTBL_AMT": "1100",
                "NCH_BENE_PTA_COINSRNC_LBLTY_AM": "0",
                "NCH_BENE_BLOOD_DDCTBL_LBLTY_AM": "0",
                "CLM_UTLZTN_DAY_CNT": "3",
                "NCH_BENE_DSCHRG_DT": "20230322",
                "CLM_DRG_CD": "291",
                "ICD9_DGNS_CD_1": "4280",
                "ICD9_DGNS_CD_2": "25000",
                "ICD9_DGNS_CD_3": "496",
                "ICD9_PRCDR_CD_1": "3893",
            }
        ]
    )


def create_synpuf_outpatient_claims() -> pd.DataFrame:
    """
    Create a small SynPUF-like outpatient claims table.
    """
    return pd.DataFrame(
        [
            {
                "DESYNPUF_ID": "claim-bene-001",
                "CLM_ID": "op-claim-001",
                "SEGMENT": "1",
                "CLM_FROM_DT": "20230110",
                "CLM_THRU_DT": "20230110",
                "PRVDR_NUM": "provider-001",
                "CLM_PMT_AMT": "550",
                "NCH_PRMRY_PYR_CLM_PD_AMT": "0",
                "AT_PHYSN_NPI": "npi-001",
                "OP_PHYSN_NPI": "",
                "OT_PHYSN_NPI": "",
                "ICD9_DGNS_CD_1": "4019",
            },
            {
                "DESYNPUF_ID": "claim-bene-002",
                "CLM_ID": "op-claim-002",
                "SEGMENT": "1",
                "CLM_FROM_DT": "20230214",
                "CLM_THRU_DT": "20230214",
                "PRVDR_NUM": "provider-002",
                "CLM_PMT_AMT": "900",
                "NCH_PRMRY_PYR_CLM_PD_AMT": "0",
                "AT_PHYSN_NPI": "npi-002",
                "OP_PHYSN_NPI": "",
                "OT_PHYSN_NPI": "",
                "ICD9_DGNS_CD_1": "25000",
            },
        ]
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