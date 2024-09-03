import os
import glob
import pandas as pd
import numpy as np
import utils.bonus_config as cfg
from utils.helper import TestReader


if __name__ == "__main__":
        # read in first set of bonus points (Zwischentest)
        test_results = {}
        test_files = glob.glob(os.path.join(cfg.test_path, '**/*.xlsx'), recursive=True)
        for test_file in test_files:
            test = TestReader(test_file)
            for member in test.member.values():
                if member.id in test_results.keys():
                    test_results[member.id]['Zwischentest'] += member.bonus_points
                else:
                    test_results[member.id] = {'Zwischentest': member.bonus_points}
        test_df = np.floor(np.clip(pd.DataFrame(test_results).T / 3, 0, 4))

        # read in second set of bonus points (Praktika)
        # needs to be in format: cfg.pra_path // P1 (or P2 or P3) // file to count points per practicum
        pra_files = glob.glob(os.path.join(cfg.pra_path, '**/*.xlsx'), recursive=True)
        pra_results = {}
        for pra_file in pra_files:
            pra_num = pra_file.split("\\")[-2]
            assert pra_num in ["P1", "P2", "P3"]
            test = TestReader(pra_file)
            for member in test.member.values():
                if member.id not in pra_results.keys():
                    pra_results[member.id] = {p_id: 0 for p_id in ["P1", "P2", "P3"]}
                pra_results[member.id][pra_num] += member.bonus_points
        pra_df = pd.DataFrame(pra_results).T
        pra_df["Summe"] = pra_df.sum(axis=1)
        pra_df.to_excel(os.path.join(cfg.base_path, "Bonuspunkte/2024s_ETG_Pra_Bonus.xlsx"))

        # Additionally, old bonus points are added to the new ones
        bonus_files = glob.glob(os.path.join(cfg.base_path, 'Bonuspunkte\\*.xlsx'), recursive=True)
        bonus_results = {}
        for bonus_file in bonus_files:
            bonus = pd.read_excel(bonus_file, index_col="Unnamed: 0")
            for member in bonus.iterrows():
                if member[0] not in bonus_results.keys():
                    bonus_results[member[0]] = {p_id: 0 for p_id in ["P1", "P2", "P3"]}
                for p_id in ["P1", "P2", "P3"]:
                    bonus_results[member[0]][p_id] = member[1][p_id]

        bonus_df = pd.DataFrame(bonus_results).T
        bonus_df["Summe"] = bonus_df.sum(axis=1)
        bonus_df.to_excel(os.path.join(cfg.base_path, "2024s_ETG_Pra_Bonuspunkte_Gesamt.xlsx"))

        # Sanity Check Bonus Points
        assert max(bonus_df["P1"]) == 1
        assert max(bonus_df["P2"]) == 1
        assert max(bonus_df["P3"]) == 1
        assert max(bonus_df["Summe"]) == 3

        # add Zwischentest and Praktika together
        combined_df = pd.merge(test_df, bonus_df["Summe"], left_index=True, right_index=True, how='outer').fillna(0)
        combined_df.rename(columns={"Summe": "Praktika"}, inplace=True)
        # add together columns praktika and zwischentest
        combined_df['Bonuspunkte'] = combined_df['Praktika'] + combined_df['Zwischentest']
        # clip to 5
        combined_df = np.clip(combined_df, 0, 5)
        combined_df.columns = ["Boni durch Zwischentest", "Boni durch Praktika", "Summe"]
        combined_df.index.name = "Matrikelnummer"
        combined_df.to_excel("Bonuspunkte_WiSe_2024.xlsx")
        pass
