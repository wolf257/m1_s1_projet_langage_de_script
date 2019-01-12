#!/usr/bin/env python3
# -*- coding : utf8 -*-

import csv
import pprint

from modules import champs

# VarFichiers
fic0 = '../2_resultats_intermediaires/0_effectifs-etudiants.csv'
fic1 = '../2_resultats_intermediaires/1_insertion_parEtabl.csv'
fic2 = '../2_resultats_intermediaires/2_pop_parDept.csv'

ficFinal = '../3_resultats_finaux/final.csv'

# VarChamps
champsOusseynou = champs.champsOusseynou
champsAndrea = champs.champsAndrea
champsLucia = champs.champsLucia

def selection_des_etablissements_pertinents():
    # pass

    with open(fic0, mode='r', encoding='utf8') as filein:
        # fic OG : (idEtabl, annee, idDept)
        infoEtabl0 = []
        for line in filein:
            annee = line.split(',')[0].strip()
            idEtabl = line.split(',')[1].strip()
            idDept = line.split(',')[9].strip()

            infoEtabl0.append((idEtabl, annee, idDept))
        # infoEtabl0 = [(idEtabl, annee, idDept) for line in fic0]

        print(f"Nbre tuple OG: {len(infoEtabl0)}")


    with open(fic1, mode='r', encoding='utf8') as filein:
    # fic andrea : (idEtabl, annee)
        infoEtabl1 = []
        for line in filein:
            idEtabl = (line.split(';')[1].strip())
            annee = (line.split(';')[0].strip())
            # print(f"{idEtabl1}, {annee}")

            infoEtabl1.append((idEtabl, annee))

        print(f"Nbre Etabl Andrea: {len(infoEtabl1)}")
        # pprint.pprint(idEtabl1)

    with open(fic2, mode='r', encoding='utf8') as filein:
    # fic lucia : idDept
        idDept2 = set([line.split(',')[0].strip() for line in filein])
        print(f"Nbre Dept Lucia (set): {len(idDept2)}")

    # =================================================

    listeEtablRetenue = []
    listeDeptRetenue = set()

    for couple in infoEtabl0:
        idEtabl = couple[0]
        annee = couple[1]
        idDept = couple[2]

        if ((idEtabl, annee) in infoEtabl1) and (idDept in idDept2):
            listeEtablRetenue.append((idEtabl, annee))
            listeDeptRetenue.add(idDept)

    print(f"Nbre d'établissement retenus (og - Andrea) : {len(listeEtablRetenue)}")
    print(f"Nbre de départements retenus (og - Lucia): {len(listeDeptRetenue)}")

    return listeEtablRetenue, listeDeptRetenue


def remplissage_dico_donnees(listeEtablRetenue, listeDeptRetenue):

    dicoDonneesEtablissements = {}

    with open(fic0, mode='r', encoding='utf8') as filein:
        for line in filein:
            idEtabl = line.split(',')[1].strip()
            annee = line.split(',')[0].strip()

            # c-a-d que c'est un bon établissement
            if (idEtabl, annee) in listeEtablRetenue:
                dicoDonneesEtablissements.setdefault((idEtabl, annee), {})

                # remplissage des infos de filein sur école
                for index, champs in enumerate(champsOusseynou):
                    idChamp = champs[0]
                    dicoDonneesEtablissements[(idEtabl, annee)][idChamp] = line.split(',')[index].strip()

            # pprint.pprint(dicoDonneesEtablissements)

    with open(fic1, mode='r', encoding='utf8') as filein:
        for line in filein:
            idEtabl = line.split(';')[1].strip()
            annee = line.split(';')[0].strip()

            if (idEtabl, annee) in listeEtablRetenue:

                # remplissage des infos de fic1 sur insertionPro
                for index, champs in enumerate(champsAndrea):
                    idChamp = champs.strip()

                    if (idChamp == 'numero_de_l_etablissement' or idChamp == 'annee'):
                        continue

                    dicoDonneesEtablissements[(idEtabl, annee)][idChamp] = line.split(';')[index].strip()

    # pprint.pprint(dicoDonneesEtablissements)

    dicoDonneesDepartements = {}

    with open(fic2, mode='r', encoding='utf8') as filein:
        for line in filein:
            idDept = line.split(',')[0].strip()

            # c-a-d que c'est un bon établissement
            if idDept in listeDeptRetenue:
                dicoDonneesDepartements.setdefault(idDept, {})

                # remplissage des infos de fic2 sur dept
                for index, champs in enumerate(['2010', '2011', '2012', '2013', '2014', '2015']):
                    idChamp = champs
                    dicoDonneesDepartements[idDept][idChamp] = line.split(',')[index+2].strip()

            # pprint.pprint(dicoDonneesDepartements)

    return dicoDonneesEtablissements, dicoDonneesDepartements

def generation_fichier_final(dicoDonneesEtablissements, dicoDonneesDepartements):

    f = csv.writer(open(ficFinal, "w+"))

    # en-tete
    listChamps1 = [elt[0] for elt in champsOusseynou]
    listChamps1Nommes = [elt[1] for elt in champsOusseynou]

    listChamps2 = [elt for elt in champsAndrea if not (elt == 'numero_de_l_etablissement' or elt == 'annee')]

    listChamps3 = [elt[0] for elt in champsLucia]
    listChamps3Nommes = [elt[1] for elt in champsLucia]

    listSousTotal = listChamps1 + listChamps2

    listTotal = listChamps1Nommes + listChamps2 + listChamps3Nommes

    f.writerow(listTotal)

    # données
    for elt in dicoDonneesEtablissements.keys():
        idDept = dicoDonneesEtablissements[elt]['dep_etab_lib'].strip()

        datas0 = [dicoDonneesEtablissements[elt].get(arg, 'na') for arg in listSousTotal]
        datas1 = [dicoDonneesDepartements[idDept].get(arg, 'na') for arg in listChamps3]
        datas = datas0 + datas1

        f.writerow(datas)

    print(f"Les données ont été écrites dans le fichier : {ficFinal.split('/')[-1]}")


if __name__ == '__main__':
    print("Je ne sers pas à grand chose seul :-). Go to main.py")