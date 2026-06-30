#!/usr/bin/env python3
"""Calculate LES for Knesset 25 only, using freshly fetched data."""

import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

RAW_DIR = Path(__file__).parent / "data" / "raw"
OUTPUT_DIR = Path(__file__).parent / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STATUS_TO_LES_WEIGHT = {
    122: 0, 124: 0, 177: 0,
    104: 1, 106: 1, 110: 1, 111: 1, 120: 1, 126: 1, 140: 1, 142: 1, 143: 1,
    150: 1, 158: 1, 161: 1, 162: 1, 165: 1, 169: 1, 175: 1, 176: 1, 181: 1,
    101: 2, 108: 2, 141: 2,
    109: 3, 167: 3, 114: 3, 117: 3, 130: 3, 131: 3,
    113: 4, 115: 4, 178: 4, 179: 4,
    118: 5,
}

def main():
    bills = pd.read_csv(RAW_DIR / "bills_knesset_25.csv")
    initiators = pd.read_csv(RAW_DIR / "initiators_knesset_25.csv")
    persons = pd.read_csv(RAW_DIR / "persons_knesset_25.csv")

    logger.info(f"Loaded: {len(bills)} bills, {len(initiators)} initiators, {len(persons)} persons")

    bill_id_col = 'BillID' if 'BillID' in bills.columns else 'Id'

    merged = initiators.merge(
        bills[[bill_id_col, 'StatusID']],
        left_on='BillID', right_on=bill_id_col,
        how='left', suffixes=('', '_bill')
    )

    merged['LES_weight'] = merged['StatusID'].map(
        lambda x: STATUS_TO_LES_WEIGHT.get(int(x) if pd.notna(x) else -1, 1)
    )

    main_init = merged[merged['IsInitiator'] == True].copy()
    logger.info(f"Main initiators: {len(main_init)}")

    les = main_init.groupby('PersonID').agg(
        LES=('LES_weight', 'sum'),
        Bills_Initiated=('BillID', 'count'),
        Bills_Failed=('LES_weight', lambda x: (x == 0).sum()),
        Bills_Introduced=('LES_weight', lambda x: (x == 1).sum()),
        Bills_Stage2=('LES_weight', lambda x: (x == 2).sum()),
        Bills_Stage3=('LES_weight', lambda x: (x == 3).sum()),
        Bills_Stage4=('LES_weight', lambda x: (x == 4).sum()),
        Bills_Passed=('LES_weight', lambda x: (x == 5).sum()),
    ).reset_index()

    person_id_col = 'PersonID' if 'PersonID' in persons.columns else 'Id'
    person_cols = [c for c in persons.columns if c in [
        person_id_col, 'FirstName', 'LastName', 'GenderID', 'GenderDesc',
        'FactionName', 'FactionID', 'Email', 'IsCurrent'
    ]]
    persons_clean = persons[person_cols].drop_duplicates(subset=[person_id_col])

    result = persons_clean.merge(les, left_on=person_id_col, right_on='PersonID', how='left')
    result['LES'] = result['LES'].fillna(0).astype(int)
    for col in ['Bills_Initiated', 'Bills_Failed', 'Bills_Introduced', 'Bills_Stage2',
                'Bills_Stage3', 'Bills_Stage4', 'Bills_Passed']:
        result[col] = result[col].fillna(0).astype(int)

    result['FullName'] = result['FirstName'].astype(str) + ' ' + result['LastName'].astype(str)
    result['Gender'] = result['GenderID'].map({250: 'Female', 251: 'Male'})
    result = result.sort_values('LES', ascending=False)

    out_path = OUTPUT_DIR / "knesset25_les.csv"
    result.to_csv(out_path, index=False, encoding='utf-8-sig')
    logger.info(f"Saved {len(result)} MKs to {out_path}")

    print(f"\n{'='*60}")
    print(f"כנסת 25 - סיכום LES מעודכן")
    print(f"{'='*60}")
    print(f"סה\"כ ח\"כים: {len(result)}")
    print(f"סה\"כ הצעות חוק: {len(bills)}")
    print(f"ממוצע LES: {result['LES'].mean():.1f}")
    print(f"חציון LES: {result['LES'].median():.1f}")
    print(f"\nTop 10:")
    for _, row in result.head(10).iterrows():
        print(f"  {row['FullName']:25s}  LES={row['LES']:>4d}  bills={row['Bills_Initiated']:>3d}  passed={row['Bills_Passed']:>2d}")

    print(f"\nלפי מגדר:")
    for g in ['Female', 'Male']:
        subset = result[result['Gender'] == g]
        print(f"  {g}: n={len(subset)}, mean LES={subset['LES'].mean():.1f}, median={subset['LES'].median():.1f}")

if __name__ == "__main__":
    main()
