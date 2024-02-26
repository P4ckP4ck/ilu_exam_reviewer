import pandas as pd


# 1. Enter the correct filepaths and set the current exam folder:
current_exam_path = "SoSe2023_ETG/"
formelfragen_database_path = "SoSe2023_ETG/ZN41/Formelfrage_DB_export_file.xlsx"
single_choice_database_path = "SoSe2023_ETG/ZN41/SingleChoice_DB_export_file.xlsx"
bonuspunkte_path = "SoSe2023_ETG/2023s_ETG_bonus_fixed.xlsx"
ilias_member_export = "SoSe2023_ETG/2023_09_12_09-571694505447_member_export_61319.xlsx"
ilias_files = ["SoSe2023_ETG/ZN41/ETG_-_Klausur-Pruefung_2023-09-11,_Raum_ZN4-1_results.xlsx",
               "SoSe2023_ETG/ZN42/ETG_-_Klausur-Pruefung_2023-09-11,_Raum_ZN4-2_results.xlsx",
               "SoSe2023_ETG/ZN43/ETG_-_Klausur-Pruefung_2023-09-11,_Raum_ZN4-3_4_results.xlsx",
               "SoSe2023_ETG/ZW51/ETG_-_Klausur-Pruefung_2023-09-11,_Raum_ZW5-1_results.xlsx",
               "SoSe2023_ETG/ZW55/ETG_-_Klausur-Pruefung_2023-09-11,_Raum_ZW5-5_results.xlsx"]

# 2. Are there any exceptions while evaluating the correct result?
use_exceptions = True

# 3. If yes, define the exceptions:
exceptions_one_point = ["08.2.795", "05.3.704", "05.3.703", "05.3.705", "27.120.33"]
exceptions_int = ["40.12.977", "40.12.978", "40.12.979"]
exceptions_swap_sign = ["01.1.171", "01.1.172"]
exceptions_1e6 = ["05.2.681"]
exceptions_1e3 = ["08.2.801", "08.2.813", "8.2.813"]
exceptions_both_signs = ["09.2.856", "09.2.857", "09.2.858", "09.2.859", "09.2.860", "09.2.861",
                         "09.2.862", "09.2.863", "09.2.864", "09.2.865", "09.2.866", "09.2.867",
                         "09.2.868", "09.2.869", "09.2.870", "09.2.871", "09.2.872", "09.2.873"]

exceptions = {"1_point": exceptions_one_point, "int": exceptions_int, "swap_sign": exceptions_swap_sign,
              "1e6": exceptions_1e6, "1e3": exceptions_1e3, "both_signs": exceptions_both_signs}

# 3. The following entries only need to be changed when there are bigger changes in the ilias export format etc.
# Excel Sheet names can only have a fixed number of characters
max_excel_sheet_characters = 26
num_ilias_overview_general_columns = 21
question_identifiers = ["Formelfrage", "Single Choice", "Freitext eingeben"]

#evaluation data
max_points = 40
grading_scheme = pd.Series(data=[0, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95],
                   index=["5,0", "4,0", "3,7", "3,3", "3,0", "2,7", "2,3", "2,0", "1,7", "1,3", "1,0"])
cache = None




