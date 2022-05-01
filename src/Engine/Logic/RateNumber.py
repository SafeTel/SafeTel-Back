##
## SAFETEL PROJECT, 2022
## SafeTel-Back
## File description:
## RateNumber
##


# This part of the engine is responsible for rating the score of each number
# TODO: Takes models as arguments
class RateNumber():
    def __init__(self):
        return

    ### PUBLIC

    # TODO: voir si un ajout à au furutr scrappeur peut être logique et interessent ici
    # Evaluate a number, 1 to 10, higher is better
    def EvaNumber(self, number: str, InternalData: dict):
        # TODO: faire un report d'erreur au monitoring si manque de données total

        # 1;1 - Extratct Data
        # 1.2 - Check si tellows pas null,

        # 2.1 - Estimer une note en fonction de données de tellowss avec un coeficient
        # 2.2 - Estimer une note en fonction de données internes avec un coeficient

        # 3 - Merge les 2 notes en fonction des coeficients

        return # return int, 1 to 10


    ### PRIVATE

    def __MergeScores(self, TellowsScore: float, TellowsCoef: float, InternalScore: float, InternalCoef: float):
        return # merged score (final)

    def __EvaInternalData(self, InternalData: dict):
        return # score & coeficient


    def __EvaTellowsData(self, TellowsData: dict):
        return # score & coeficient


    def __ExtInternalData(self, InternalData: dict):
        return # Resume of internal data


    def __ExtTellowsData(self, TellowsData: dict):
        return # Resume of tellows data
