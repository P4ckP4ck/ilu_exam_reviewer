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
        test_df = np.floor(np.clip(pd.DataFrame(test_results).T / 3, 0, 3))

        # read in second set of bonus points (Praktika)
        pra_files = glob.glob(os.path.join(cfg.pra_path, '**/*.xlsx'), recursive=True)
        pra_results = {}
        for pra_file in pra_files:
            test = TestReader(pra_file)
            for member in test.member.values():
                if member.id in pra_results.keys():
                    pra_results[member.id]['Praktikum'] += member.bonus_points
                else:
                    pra_results[member.id] = {'Praktikum': member.bonus_points}
        pra_df = pd.DataFrame(pra_results).T


        # Additionally, old bonus points are added to the new ones
        old_pra_bonus = pd.read_excel(os.path.join(cfg.base_path, '2023s_ETG_bonus_fixed.xlsx'))
        old_pra_bonus.index = old_pra_bonus["Matrikelnummer"]
        pra_df = pd.merge(pra_df, old_pra_bonus["Boni durch Praktika"], left_index=True, right_index=True, how="outer")
        pra_df.fillna(0, inplace=True)
        pra_df["Praktika gesamt"] = np.clip(pra_df["Boni durch Praktika"] + pra_df["Praktikum"], 0, 3)

        ### Nachgeschriebene Klausurauswertung, nur gültig für dieses Semester
        nach_klausur = pd.read_csv(os.path.join(cfg.base_path, 'Noten ETG Nachholklausur 2023-11-28.csv'))
        # remove bonus points from students that took the exam
        pra_df = pra_df[~pra_df.index.isin(nach_klausur['Mat.Nr.'])]

        # add both together
        combined_df = pd.merge(test_df, pra_df["Praktika gesamt"], left_index=True, right_index=True, how='outer').fillna(0)
        # add together columns praktika and zwischentest
        combined_df['Bonuspunkte'] = combined_df['Praktika gesamt'] + combined_df['Zwischentest']
        # clip to 5
        combined_df = np.clip(combined_df, 0, 5)
        combined_df.columns = ["Boni durch Zwischentest", "Boni durch Praktika", "Summe"]
        combined_df.index.name = "Matrikelnummer"
        combined_df.to_excel("Bonuspunkte_WiSe_2024.xlsx")
        pass
