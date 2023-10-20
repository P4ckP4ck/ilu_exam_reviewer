import pandas as pd
import utils.config as cfg
from math import *


class Frage:

    def __init__(self, answer, detailed_ilias, correct_ilias):
        self._answer = answer
        self._detailed_ilias = detailed_ilias
        self._database = None
        self.correct_ilias = bool(correct_ilias) if not pd.isna(correct_ilias) else False
        self.correct = False
        self._question_description_main = "Bitte ignorieren!"


class Formelfrage(Frage):

    def __init__(self, answer, detailed_ilias, correct_ilias):
        super().__init__(answer, detailed_ilias, correct_ilias)
        self._database = cfg.cache.formelfragen_pool
        formelfrage = self._database.loc[answer.ID]
        for column in self._database.columns:
            setattr(self, "_" + column, formelfrage[column])
        self._user_entry = detailed_ilias.iloc[answer.idx_from:answer.idx_to, :][1:]
        for idx, row in self._user_entry.iterrows():
            if not pd.isna(row.iloc[0]):
                setattr(self, "_" + row.iloc[0][1:], row.iloc[1])
        self.check_consistency()

    @property
    def result_tool(self):
        if "_v1" not in self.__dict__.keys():
            # Question not initialised by student!
            return None
        return eval(self.formula)

    @property
    def result_user(self):
        if "_r1" in self.__dict__.keys():
            if pd.isna(self._r1):
               return None
            # if _r1 is a string e.g. a fraction
            if type(self._r1) == str:
                result = eval(self._r1)
            else:
                result = self._r1
            result = floor(result * 10 ** self._res1_prec) / 10 ** self._res1_prec
        else:
            result = None
        return result

    @property
    def formula(self):
        return self._translate_formula(self._res1_formula)

    @property
    def correct_tool(self):
        if "_v1" not in self.__dict__.keys():
            # Question not initialised by student!
            return False

        r_min = min(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))
        r_max = max(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))

        r_min = min(floor(r_min * 10 ** self._res1_prec) / 10 ** self._res1_prec, r_min)
        r_max = max(round(r_max, self._res1_prec), r_max)
        if self.result_user is not None:
            if (self.result_user >= r_min) and (self.result_user <= r_max):
                return True
        return False

    def _translate_formula(self, formula_string):
        ### TODO copied from source, translation dict would be better
        formula_string = formula_string.replace(",", ".")
        formula_string = formula_string.replace("^", "**")
        formula_string = formula_string.replace("arcsin", "asin")
        formula_string = formula_string.replace("arcsinh", "asinh")
        formula_string = formula_string.replace("arccos", "acos")
        formula_string = formula_string.replace("arccosh", "acosh")
        formula_string = formula_string.replace("arctan", "atan")
        formula_string = formula_string.replace("arctanh", "atanh")
        formula_string = formula_string.replace("ln", "log")
        formula_string = formula_string.replace("log", "log10")
        formula_string = formula_string.replace("$", "self._")
        return formula_string

    def check_consistency(self):
        if not self.correct_ilias == self.correct_tool:
            print(f"Difference in {self._answer.ID}!")
        self.correct = max(self.correct_ilias, self.correct_tool)


class SingleChoice(Frage):

    def __init__(self, answer, detailed_ilias, correct_ilias):
        super().__init__(answer, detailed_ilias, correct_ilias)
        self._database = cfg.cache.single_choice_pool
        single_choice = self._database.loc[answer.ID]
        for column in self._database.columns:
            setattr(self, "_" + column, single_choice[column])

        self._user_entry = detailed_ilias.iloc[answer.idx_from:answer.idx_to, :][1:]
        self.result_user = []
        for _, row in self._user_entry.iterrows():
            if not pd.isna(row.iloc[0]):
                self.result_user += [row.iloc[1]]

        self.result_tool = []
        for key, value in single_choice.items():
            if "pts" in str(key):
                if pd.isna(value):
                    continue
                self.result_tool += [value]

        self.correct = self.correct_ilias


class FormelfrageExceptions(Formelfrage):

    def __init__(self, answer, detailed_ilias, correct_ilias):
        super().__init__(answer, detailed_ilias, correct_ilias)

    def check_consistency(self):
        if not self.correct_ilias == self.correct_tool:
            print(f"Difference in {self._answer.ID}!")
        self.correct = max(self.correct_ilias, self.correct_tool)

        # Checking for exceptions
        self.correct = self.check_exceptions(self._answer.ID)

    def check_exceptions(self, question_id):
        instruction = None
        for exception_key, exception_list in cfg.exceptions.items():
            if question_id in exception_list:
                instruction = exception_key
                break

        if instruction == "1_point":
            return True

        elif instruction == "int":
            if "_v1" not in self.__dict__.keys():
                # Question not initialised by student!
                return False

            r_min = min(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))
            r_max = max(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))

            r_min = min(floor(r_min * 10 ** self._res1_prec) / 10 ** self._res1_prec, r_min)
            r_max = max(round(r_max, self._res1_prec), r_max)
            if self.result_user is not None:
                if self.result_user == r_min:
                    return True
            return False

        elif instruction == "swap_sign":
            if "_v1" not in self.__dict__.keys():
                # Question not initialised by student!
                return False

            r_min = min(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))
            r_max = max(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))

            r_min = min(floor(r_min * 10 ** self._res1_prec) / 10 ** self._res1_prec, r_min)
            r_max = max(round(r_max, self._res1_prec), r_max)
            if self.result_user is not None:
                if (-self.result_user >= r_min) and (-self.result_user <= r_max):
                    return True
            return False

        elif instruction == "1e6":
            if "_v1" not in self.__dict__.keys():
                # Question not initialised by student!
                return False

            r_min = min(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))
            r_max = max(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))

            r_min = min(floor(r_min * 10 ** self._res1_prec) / 10 ** self._res1_prec, r_min)
            r_max = max(round(r_max, self._res1_prec), r_max)
            if self.result_user is not None:
                if (self.result_user >= r_min * 1e-6) and (self.result_user <= r_max * 1e-6):
                    return True
            return False

        elif instruction == "1e3":
            if "_v1" not in self.__dict__.keys():
                # Question not initialised by student!
                return False

            r_min = min(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))
            r_max = max(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))

            r_min = min(floor(r_min * 10 ** self._res1_prec) / 10 ** self._res1_prec, r_min)
            r_max = max(round(r_max, self._res1_prec), r_max)
            if self.result_user is not None:
                if (self.result_user >= r_min * 1e-3) and (self.result_user <= r_max * 1e-3):
                    return True
            return False

        elif instruction == "both_signs":
            if "_v1" not in self.__dict__.keys():
                # Question not initialised by student!
                return False

            r_min = min(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))
            r_max = max(self.result_tool * (1 + self._res1_tol / 100), self.result_tool * (1 - self._res1_tol / 100))

            r_min = min(floor(r_min * 10 ** self._res1_prec) / 10 ** self._res1_prec, r_min)
            r_max = max(round(r_max, self._res1_prec), r_max)
            if self.result_user is not None:
                if ((self.result_user >= r_min) and (self.result_user <= r_max)) or (
                        (-self.result_user >= r_min) and (-self.result_user <= r_max)):
                    return True
            return False

        else:
            return self.correct