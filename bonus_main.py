import os
import glob
import pandas as pd
import numpy as np
import utils.bonus_config as cfg
from utils.helper import TestReader


if __name__ == "__main__":
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
        # add both together
        combined_df = pd.merge(test_df, pra_df, left_index=True, right_index=True, how='outer')
        # add together columns praktika and zwischentest
        combined_df['Bonuspunkte'] = combined_df['Praktikum'] + combined_df['Zwischentest']
        # clip to 5
        combined_df = np.clip(combined_df, 0, 5).fillna(0)
        # combined_df["Summe"] = np.clip(combined_df["Zwischentest"] + combined_df["Praktikum"], 0, 5)

        pass
