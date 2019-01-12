#!/usr/bin/env/ python3
# -*- coding : utf-8 -*-

import pprint
import csv

from modules import collecte_donnees
from modules import production_finale
from modules import autres


def main():
    """docstring for main"""

    print(f"\n======= 0: PHASE VERIFICATION ARBORESCENCE =======\n")
    autres.generation_arborescence()

    print(f"\n======= 1: PHASE DE COLLECTE DES DONNEES =======\n")
    collecte_donnees.generation_tableau_intermediaire_sur_demographie()
    collecte_donnees.generation_tableau_intermediaire_sur_insertionPro()
    collecte_donnees.generation_tableau_intermediaire_sur_Univ()

    print(f"\n======= 2: PHASE DE TRAVAIL SUR LES DONNEES =======\n")
    listeEtabl, listeDept = production_finale.selection_des_etablissements_pertinents()

    dicoEtablissements, dicoDepartements = production_finale.remplissage_dico_donnees(listeEtabl, listeDept)

    print(f"\n======= 3: PHASE DE PRODUCTION FINALE =======\n")
    production_finale.generation_fichier_final(dicoEtablissements, dicoDepartements)

if __name__ == '__main__':
    main()
