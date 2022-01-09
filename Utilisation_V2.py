from codeV2 import*
from datatest import users
from datatest import id_product
from time import time
import matplotlib.pyplot as plt




h = input("\n VOULEZ-VOUS GENERER DES UTILISATEURS ALEATOIREMENT ? \n \n           TAPEZ Y SI VOUS LE SOUHAITEZ \n \n           TAPEZ N SINON  \n \n           VOTRE CHOIX : ")


if h == 'Y' or h == 'y':
    semaine = int(input("\n \n SUR COMBIEN DE TEMPS VOULEZ-VOUS TRAVAILLER?\n \n           1 : CHAQUE SEMAINE\n           2 : TOUTES LES 2 SEMAINES\n           ETC...\n \n           VOTRE CHOIX : "))

    number_of_users = int(input("\n \n \n COMBIEN D'UTILISATEURS VOULEZ-VOUS CREER? \n \n           VOTRE CHOIX : "))

    proba_connexion = float(input("\n \n \n CHOISISSEZ LA PROBABILITE AVEC LAQUELLE UN UTILISATEUR SE CONNECTE CHAQUE SEMAINE \n \n           VOTRE CHOIX : "))

    users = generate_k_random_users(semaine, id_product, number_of_users, proba_connexion)

    print("\n \n \n SUR COMBIEN DE SEMAINES VOULEZ-VOUS REGARDER LES SEQUENCES?\n \n ATTENTION CE NOMBRE NE DOIT PAS ETRE SUPERIEUR A :", semaine)
    nbre_listes_a_combiner = int(input("\n \n           VOTRE CHOIX : "))

else:
    nbre_listes_a_combiner = int(input("\n \n \n SUR COMBIEN DE SEMAINES VOULEZ-VOUS REGARDER LES SEQUENCES?\n \n           VOTRE CHOIX : "))



users_combine = []
for i in range(len(users)):
    users_combine.append(combiner_lignes(users[i], nbre_listes_a_combiner))


final = combiner_lignes(users_combine, nbre_listes_a_combiner=len(users_combine))[0]  #Permet d'avoir  qu'une sous liste pour faire tourner l'algo sinon on a des sous-listes de sous-listes


choix1 = int(input("\n \n \n CHOISISSEZ LE MODE QUE VOUS DESIREZ : \n \n           1 : TOUTES LES SEQUENCES \n \n           2 : UNIQUEMENT LES SEQUENCES CONTENANT UN ACHAT \n \n           VOTRE CHOIX : "))





# TOUTES LES SEQUENCES
if choix1 == 1:
    choix2 = int(input("\n \n \n CHOISISSEZ LE MODE QUE VOUS DESIREZ : \n \n           1 : SEQUENCES D'UNE LONGUEUR PARTICULIERE \n \n           2 : TOUTES LES SEQUENCES DE LONGUEURS L PLUS GRANDES QU'UNE LONGUEUR CHOISIE \n \n           VOTRE CHOIX : "))

    regroupement = input("\n \n \n ETES-VOUS INTERESSE(E)S PAR LES PRODUITS OU UNIQUEMENT PAR LES ACHATS SANS DIFFERENCIER LES PRODUITS ?\n \n           POUR CONNAITRE LES SEQUENCES DE PRODUITS PARTICULIERS, TAPEZ P\n \n           POUR CONNAITRE UNIQUEMENT LES SEQUENCES AVEC DES ACHATS, TAPES A \n \n           VOTRE CHOIX : ")


    # TOUTES LES SEQUENCES D'UNE LONGUEUR PARTICULIERE AVEC LES PRODUITS
    if regroupement == 'P' or regroupement == 'p':

        if choix2 == 1:
            k = int(input("\n \n \n ENTREZ LA LONGUEUR DES SEQUENCES \n \n           VOTRE CHOIX : "))
            min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))
            print("IL Y A :", len(generate_frequent(final, min_sup, k)), "SEQUENCES DE LONGUEUR :", k, "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
            for i in range(len(generate_frequent(final, min_sup, k))):
                print("\n ", generate_frequent(final, min_sup, k)[i], "SUPPORT =", support(final, generate_frequent(final, min_sup, k)[i]))


        # TOUTES LES SEQUENCES DE LONGUEURS k PLUS GRANDES QU'UNE LONGUEUR DONNEE
        if choix2 == 2:
            k = int(input("\n \n \n ENTREZ LA LONGUEUR AU DESSUS DE LAQUELLE LES SEQUENCES SERONT RETOURNEES \n \n           VOTRE CHOIX : "))
            min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))

            frequent = generate_frequent(final, min_sup, k)
            l = [[]]
            enum = k - 1
            print("\n \n IL Y A : ", len(frequent), "SEQUENCES DE LONGUEUR : ", len(frequent[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
            for i in range(len(frequent)):
                print("\n ", frequent[i], "SUPPORT =", support(final, frequent[i]))

            while frequent != l: # C'etait len(frequent) != l
                tamp = []  # . ---------------------------------------------|
                for i in frequent:  # .                                     |
                    for j in frequent:  # .                                 |
                        if i[1:] == j[:len(j) - 1]:  # .                    |
                            list_tampon = deepcopy(i)  # .                  |> TOUT CA SERT POUR LES CANDIDATS k-SEQUENTS
                            list_tampon.append(j[len(j) - 1])  # .          |
                            tamp.append(list_tampon)  # .                   |

                candidat = tamp
                tamp_candidat = []
                list_a_regarder = []
                for i in range(len(final)):
                    if len(final[i]) >= k:
                        list_a_regarder.append(final[i])

                for elt in candidat:
                    count = 0
                    for i in range(len(list_a_regarder)):
                        if are_present(list_a_regarder[i], elt) is True:
                            count = count + 1
                    if count / len(final) >= min_sup:
                        tamp_candidat.append(elt)
                frequent = tamp_candidat
                if len(frequent) != 0:
                    print("\n \n \nIL Y A : ", len(frequent), "SEQUENCES DE LONGUEUR : ", len(frequent[0]),"AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                    for i in range(len(frequent)):
                        print("\n ", frequent[i], "SUPPORT =", support(final, frequent[i]))
                    enum = enum + 1
                else:
                    print("\n \n AUCUNE SEQUENCE FREQUENTE DE LONGUEUR :", enum + 2, "TROUVEE")
                    break



    if regroupement == 'A' or regroupement == 'a':

        final = regrouper_achats(final, id_product)

        if choix2 == 1:
            k = int(input("\n \n \n ENTREZ LA LONGUEUR DES SEQUENCES \n \n           VOTRE CHOIX : "))
            min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))
            print("IL Y A :", len(generate_frequent(final, min_sup, k)), "SEQUENCES DE LONGUEUR :", k)
            for i in range(len(generate_frequent(final, min_sup, k))):
                print("\n ", generate_frequent(final, min_sup, k)[i], "SUPPORT =", support(final, generate_frequent(final, min_sup, k)[i]))



        # TOUTES LES SEQUENCES DE LONGUEURS k PLUS GRANDES QU'UNE LONGUEUR DONNEE
        if choix2 == 2:
            k = int(input("\n \n \n ENTREZ LA LONGUEUR AU DESSUS DE LAQUELLE LES SEQUENCES SERONT RETOURNEES \n \n           VOTRE CHOIX : "))
            min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))

            frequent = generate_frequent(final, min_sup, k)
            l = [[]]
            enum = k - 1
            print("\n \n IL Y A : ", len(frequent), "SEQUENCES DE LONGUEUR : ", len(frequent[0]),"AYANT UN SUPPORT SUPERIEUR A :", min_sup)
            for i in range(len(frequent)):
                print("\n ", frequent[i], "SUPPORT =", support(final, frequent[i]))
            while frequent != l: # C'etait len(frequent) != l
                tamp = []  # . ---------------------------------------------|
                for i in frequent:  # .                                     |
                    for j in frequent:  # .                                 |
                        if i[1:] == j[:len(j) - 1]:  # .                    |
                            list_tampon = deepcopy(i)  # .                  |> TOUT CA SERT POUR LES CANDIDATS k-SEQUENTS
                            list_tampon.append(j[len(j) - 1])  # .          |
                            tamp.append(list_tampon)  # .                   |

                candidat = tamp
                tamp_candidat = []
                list_a_regarder = []
                for i in range(len(final)):
                    if len(final[i]) >= k:
                        list_a_regarder.append(final[i])

                for elt in candidat:
                    count = 0
                    for i in range(len(list_a_regarder)):
                        if are_present(list_a_regarder[i], elt) is True:
                            count = count + 1
                    if count / len(final) >= min_sup:
                        tamp_candidat.append(elt)

                frequent = tamp_candidat
                if len(frequent) != 0:
                    print("\n \n \nIL Y A : ", len(frequent), "SEQUENCES DE LONGUEUR : ", len(frequent[0]),"AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                    for i in range(len(frequent)):
                        print("\n ", frequent[i], "SUPPORT =", support(final, frequent[i]))
                    enum = enum + 1
                else:
                    print("\n \n AUCUNE SEQUENCE FREQUENTE DE LONGUEUR :", enum + 2, "TROUVEE")
                    break




# UNIQUEMENT LES SEQUENCES CONTENANT UN ACHAT
elif choix1 == 2:

    regroupement = input("\n \n \n ETES-VOUS INTERESSE(E)S PAR LES PRODUITS OU UNIQUEMENT PAR LES ACHATS SANS DIFFERENCIER LES PRODUITS ?\n \n           POUR CONNAITRE LES SEQUENCES DE PRODUITS PARTICULIERS, TAPEZ P\n \n           POUR CONNAITRE UNIQUEMENT LES SEQUENCES AVEC DES ACHATS, TAPES A \n \n           VOTRE CHOIX : ")



    # UNIQUEMENT LES SEQUENCES AVEC DES ACHATS SANS DIFFERENCIER LES PRODUITS
    if regroupement == 'A' or regroupement == 'a':
        choix2 = int(input("\n \n \n CHOISISSEZ LE MODE QUE VOUS DESIREZ : \n \n           1 : SEQUENCES D'UNE LONGUEUR PARTICULIERE \n \n           2 : TOUTES LES SEQUENCES DE LONGUEURS L PLUS GRANDES QU'UNE LONGUEUR CHOISIE \n \n           VOTRE CHOIX : "))
        sequences = []
        final = regrouper_achats(final, id_product)



        # UNIQUEMENT LES SEQUENCES D'UNE LONGUEUR PARTICULIERE AVEC DES ACHATS SANS DIFFERENCIER LES PRODUIT
        if choix2 == 1:

            k = int(input("\n \n \n CHOISISSEZ LA LONGUEUR DES SEQUENCES \n \n           VOTRE CHOIX : "))
            min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))
            frequent = generate_frequent(final, min_sup, k)
            sequences = []
            for elt in frequent:
                if 'purchase' in elt:
                    sequences.append(elt)
            sequence_menant_a_un_achat = input("\n \n \n VOULEZ-VOUS SELECTIONNER UNIQUEMENT LES SEQUENCES MENANT A UN ACHAT ?\n \n           SI VOUS LE SOUHAITEZ?, TAPEZ Y, SINON TAPEZ N\n \n           SI VOUS CHOISISSEZ N, LE PROGRAMME POURRA VOUS RETOURNER DES SEQUENCES DU TYPE ['purchase', 'purchase', 'purchase'] \n \n           VOTRE CHOIX : ")
            # SEQUENCE MENANT A UN ACHAT

            if len(sequences) != 0 and sequence_menant_a_un_achat == 'Y' or len(sequences) != 0 and sequence_menant_a_un_achat == 'y':
                tamp = []

                for i in range(len(sequences)):

                    if sequences[i][0] != 'purchase':
                        tamp.append(sequences[i])
                if len(tamp) == 0:
                    print("\n AUCUNE SEQUENCE DE LONGUEUR :", k, "AYANT UN SUPPORT SUPERIEUR A :", min_sup, "TROUVEE  \n \n          NOUS VOUS SUGGERONS DEE BAISSER LE MIN_SUP ET/OU DE REGARDER SUR UNE DUREE PLUS LONGUE")

                else:
                    print("\n \n IL Y A : ", len(tamp), "SEQUENCES DE LONGUEUR : ", len(tamp[0]),"AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                    for i in range(len(tamp)):
                        print("\n ", tamp[i], "SUPPORT =", support(final, tamp[i]))

            else:
                if len(sequences) == 0:
                    print("\n AUCUNE SEQUENCE DE LONGUEUR :", k, "AYANT UN SUPPORT SUPERIEUR A :", min_sup, "TROUVEE  \n \n          NOUS VOUS SUGGERONS DEE BAISSER LE MIN_SUP ET/OU DE REGARDER SUR UNE DUREE PLUS LONGUE")
                else:
                    print("\n IL Y A : ", len(sequences), "SEQUENCES DE LONGUEUR : ", len(sequences[0]),"AYANT UN SUPPORT SUPERIEUR A:", min_sup)
                    for i in range(len(sequences)):
                        print("\n ", sequences[i], "SUPPORT =", support(final, sequences[i]))





        # TOUTES LES SEQUENCES DE LONGUEURS L PLUS GRANDES QU'UNE LONGUEUR DONNEE AVEC DES ACHATS SANS DIFFERENCIER LES PRODUITS
        elif choix2 == 2:
            sequence_menant_a_un_achat = input("\n \n \n VOULEZ-VOUS SELECTIONNER UNIQUEMENT LES SEQUENCES MENANT A UN ACHAT ?\n \n           SI VOUS LE SOUHAITEZ?, TAPEZ Y, SINON TAPEZ N\n \n           SI VOUS CHOISISSEZ N, LE PROGRAMME POURRA VOUS RETOURNER DES SEQUENCES DU TYPE ['purchase', 'purchase', 'purchase'] \n \n           VOTRE CHOIX : ")

            # SANS UNIQUEMENT MENER AUX ACHATS
            if sequence_menant_a_un_achat == 'N' or sequence_menant_a_un_achat == 'n':


                k = int(input("\n \n \n CHOISISSEZ LA LONGUEUR DES SEQUENCES A PARTIR DE LAQUELLE VOUS VOULEZ CONNAITRES LES SEQUENCES FREQUENTES \n \n           VOTRE CHOIX : "))
                min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))
                frequent = generate_frequent(final, min_sup, k)
                sequences = []
                for elt in frequent:
                    if 'purchase' in elt:
                        sequences.append(elt)
                l = [[]]
                enum = k - 1
                print("\n \n IL Y A : ", len(sequences), "SEQUENCES DE LONGUEUR : ", len(sequences[0]),"AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                for i in range(len(sequences)):
                    print("\n ", sequences[i], "SUPPORT =", support(final, sequences[i]))

                while sequences != l: #c'etait len(sequences) != l
                    tamp = []  # . ---------------------------------------------|
                    for i in frequent:  # .                                     |
                        for j in frequent:  # .                                 |
                            if i[1:] == j[:len(j) - 1]:  # .                    |
                                list_tampon = deepcopy(i)  # .                  |> TOUT CA SERT POUR LES CANDIDATS k-SEQUENTS
                                list_tampon.append(j[len(j) - 1])  # .          |
                                tamp.append(list_tampon)  # .                   |

                    candidat = tamp
                    tamp_candidat = []
                    list_a_regarder = []
                    for i in range(len(final)):
                        if len(final[i]) >= k:
                            list_a_regarder.append(final[i])

                    for elt in candidat:
                        count = 0
                        for i in range(len(list_a_regarder)):
                            if are_present(list_a_regarder[i], elt) is True:
                                count = count + 1
                        if count / len(final) >= min_sup:
                            tamp_candidat.append(elt)


                    frequent = tamp_candidat
                    sequences = []
                    for elt in frequent:
                        if 'purchase' in elt:
                            sequences.append(elt)
                    if len(frequent) != 0:
                        print("\n \n \nIL Y A : ", len(sequences), "SEQUENCES DE LONGUEUR : ", len(sequences[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                        for i in range(len(sequences)):
                            print("\n ", sequences[i], "SUPPORT =", support(final, sequences[i]))
                        enum = enum + 1
                    else:
                        print("\n \n AUCUNE SEQUENCE FREQUENTE DE LONGUEUR :", enum + 2, "AYANT UN SUPPORT SUPERIEUR A :", min_sup, "TROUVEE")
                        break


           # UNIQUEMENT MENANT AUX ACHATS

            else:
                k = int(input("\n \n \n CHOISISSEZ LA LONGUEUR DES SEQUENCES A PARTIR DE LAQUELLE VOUS VOULEZ CONNAITRES LES SEQUENCES FREQUENTES \n \n           VOTRE CHOIX : "))
                min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))
                frequent = generate_frequent(final, min_sup, k)
                sequences = []

                for elt in frequent:
                    if 'purchase' in elt:
                        sequences.append(elt)

                tampo = []
                for i in range(len(sequences)):
                    if sequences[i][0] != 'purchase':
                        tampo.append(sequences[i])
                l = [[]]
                enum = k - 1
                if len(tampo) == 0:
                    print("\n \n AUCUNE SEQUENCE FREQUENTE DE LONGUEUR :", k, "TROUVEE AYANT UN SUPPORT SUPERIEUR A :", min_sup)

                else :
                    print("\n \n IL Y A : ", len(tampo), "SEQUENCES DE LONGUEUR : ", len(tampo[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                    for i in range(len(tampo)):
                        print("\n ", tampo[i], "SUPPORT =", support(final, tampo[i]))

                while tampo != l:
                    t0 = time()
                    tamp = []  # . ---------------------------------------------|
                    for i in frequent:  # .                                     |
                        for j in frequent:  # .                                 |
                            if i[1:] == j[:len(j) - 1]:  # .                    |
                                list_tampon = deepcopy(
                                    i)  # .                  |> TOUT CA SERT POUR LES CANDIDATS k-SEQUENTS
                                list_tampon.append(j[len(j) - 1])  # .          |
                                tamp.append(list_tampon)  # .                   |

                    candidat = tamp
                    tamp_candidat = []
                    list_a_regarder = []
                    for i in range(len(final)):
                        if len(final[i]) >= k:
                            list_a_regarder.append(final[i])

                    for elt in candidat:
                        count = 0
                        for i in range(len(list_a_regarder)):
                            if are_present(list_a_regarder[i], elt) is True:
                                count = count + 1
                        if count / len(final) >= min_sup:
                            tamp_candidat.append(elt)

                    frequent = tamp_candidat
                    sequences = []
                    for elt in frequent:
                        if 'purchase' in elt:
                            sequences.append(elt)

                    tampo = []
                    for i in range(len(sequences)):
                        if sequences[i][0] != 'purchase':
                            tampo.append(sequences[i])

                    if len(tampo) != 0:
                        print("\n \n \nIL Y A : ", len(tampo), "SEQUENCES DE LONGUEUR : ", len(tampo[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                        for i in range(len(tampo)):
                            print("\n ", tampo[i], "SUPPORT =", support(final, tampo[i]))
                        enum = enum + 1
                    else:
                        print("\n \n AUCUNE SEQUENCE FREQUENTE DE LONGUEUR :", enum + 2, "TROUVEE AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                        break



    # UNIQUEMENT LES SEQUENCES DE PRODUITS PARTICULIERS
    elif regroupement == 'P' or regroupement == 'p':
        print("\n \n \n VOICI LA LISTE DES ID_PRODUCT : ", id_product)
        values = input("\n \n QUELS SONT LES ID_PRODUCT QUI VOUS INTERESSENT ? \n \n           EX : POUR S'INTERESSER UNIQUEMENT AUX ID_PRODUCT '163792' ET '4379245' TAPEZ  :  163792 4379245 \n \n                SI VOULEZ TOUS LES ID_PRODUCTS : TAPEZ 'ALL'\n \n           VOTRE CHOIX : ")
        if values == 'ALL' or values == 'all':
            id_product_choisis = id_product

        else:
            id_product_choisis = values.split()


        choix2 = int(input("\n \n \n CHOISISSEZ LE MODE QUE VOUS DESIREZ : \n \n           1 : SEQUENCES D'UNE LONGUEUR PARTICULIERE \n \n           2 : TOUTES LES SEQUENCES DE LONGUEURS L PLUS GRANDES QU'UNE LONGUEUR CHOISIE \n \n           VOTRE CHOIX : "))

        sequence_menant_a_un_achat = input("\n \n \n VOULEZ-VOUS SELECTIONNER UNIQUEMENT LES SEQUENCES MENANT A UN ACHAT ?\n \n           SI VOUS LE SOUHAITEZ?, TAPEZ Y, SINON TAPEZ N\n \n           SI VOUS CHOISISSEZ N, LE PROGRAMME POURRA VOUS RETOURNER DES SEQUENCES DU TYPE ['purchase', 'purchase', 'purchase'] \n \n           VOTRE CHOIX : ")

        # UNIQUEMENT LES SEQUENCES DE PRODUITS PARTICULIERS D'UNE LONGUEUR PARTICULIERE
        if choix2 == 1:
            k = int(input("\n \n \n CHOISISSEZ LA LONGUEUR DES SEQUENCES QUE VOUS DESIREZ \n \n           VOTRE CHOIX : "))
            min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           EX : SI MIN_SUP = 0.2, L'ALGORITHME NE RETOURNERA QUE LES SEQUENCES APPARAISSANT DANS 20% DES CAS \n \n           VOTRE CHOIX : "))
            frequent = generate_frequent(final, min_sup, k)
            tampon = []
            for elt in frequent:
                for j in range(len(elt)):
                    if elt[j] in id_product_choisis:
                        tampon.append(elt)


            # NON UNIQUEMENT MENANT A UN ACHAT
            if sequence_menant_a_un_achat == 'N' or sequence_menant_a_un_achat == 'n':

                if len(tampon) == 0:
                    print("\n AUCUNE SEQUENCE AYANT UN SUPPORT SUPERIEUR A :", min_sup, "N'A ETE TROUVEE \n \n          NOUS VOUS SUGGERONS DEE BAISSER LE MIN_SUP ET/OU DE REGARDER PLUS DE PRODUITS DIFFERENTS")
                else:
                    print("\n IL Y A : ", len(tampon), "SEQUENCES DE LONGUEUR : ", len(tampon[0]), "AYANT UN SUPPORT SUPERIEUR A:", min_sup)
                    for i in range(len(tampon)):
                        print("\n ", tampon[i], "SUPPORT =", support(final, tampon[i]))


            # UNIQUEMENT MENANT A UN ACHAT
            elif sequence_menant_a_un_achat == 'Y' or sequence_menant_a_un_achat == 'y':
                renvoi = []
                for i in range(len(tampon)):
                    if tampon[i][0] not in id_product_choisis:
                        renvoi.append(tampon[i])

                if len(renvoi) == 0:
                    print("\n AUCUNE SEQUENCE DE LONGUEUR :", k, "AYANT UN SUPPORT SUPERIEUR A :", min_sup, "TROUVEE  \n \n          NOUS VOUS SUGGERONS DEE BAISSER LE MIN_SUP ET/OU DE REGARDER SUR UNE DUREE PLUS LONGUE")

                else:
                    print("\n IL Y A :", len(renvoi), "SEQUENCES DE LONGUEUR : ", len(renvoi[0]), "AYANT UN SUPPORT SUPERIEUR A:", min_sup)
                    for i in range(len(renvoi)):
                        print("\n ", renvoi[i], "SUPPORT =", support(final, renvoi[i]))


        # UNIQUEMENT LES SEQUENCES DE PRODUITS PARTICULIERS DE LONGUEURS L PLUS GRANDES QU'UNE LONGUEUR CHOISIE
        if choix2 == 2:
            k = int(input("\n \n \n CHOISISSEZ LA LONGUEUR DES SEQUENCES A PARTIR DE LAQUELLE VOUS VOULEZ CONNAITRE LES SEQUENCES FREQUENTES \n \n           VOTRE CHOIX : "))
            min_sup = float(input("\n \n \n CHOISISSEZ LE SUPPORT MINIMUM AU DESSUS DUQUEL LES SEQUENCES SERONT RETOURNEES. \n \n           Ex : si min_sup = 0.2, l'algorithme ne retournera que les séquences apparaissant dans 20% des cas \n \n           VOTRE CHOIX : "))


            if sequence_menant_a_un_achat == 'N' or sequence_menant_a_un_achat == 'n':

                tampon = []
                frequent = generate_frequent(final, min_sup, k)
                for elt in frequent:
                    for j in range(len(elt)):
                        if elt[j] in id_product_choisis:
                            tampon.append(elt)
                l = [[]]
                enum = k - 1
                print("\n \n IL Y A : ", len(tampon), "SEQUENCES DE LONGUEUR : ", len(tampon[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                for i in range(len(tampon)):
                    print("\n ", tampon[i], "SUPPORT =", support(final, tampon[i]))

                while tampon != l:
                    tampon = []
                    tamp = []  # . ---------------------------------------------|
                    for i in frequent:  # .                                     |
                        for j in frequent:  # .                                 |
                            if i[1:] == j[:len(j) - 1]:  # .                    |
                                list_tampon = deepcopy(i)  # .                  |> TOUT CA SERT POUR LES CANDIDATS k-SEQUENTS
                                list_tampon.append(j[len(j) - 1])  # .          |
                                tamp.append(list_tampon)  # .                   |

                    candidat = tamp
                    tamp_candidat = []
                    list_a_regarder = []
                    for i in range(len(final)):
                        if len(final[i]) >= k:
                            list_a_regarder.append(final[i])

                    for elt in candidat:
                        count = 0
                        for i in range(len(list_a_regarder)):
                            if are_present(list_a_regarder[i], elt) is True:
                                count = count + 1
                        if count / len(final) >= min_sup:
                            tamp_candidat.append(elt)


                    frequent = tamp_candidat
                    sequences = []
                    for elt in frequent:
                        for j in range(len(elt)):
                            if elt[j] in id_product_choisis:
                                tampon.append(elt)
                    if len(tampon) != 0:
                        print("\n \n \nIL Y A : ", len(tampon), "SEQUENCES DE LONGUEUR : ", len(tampon[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                        for i in range(len(tampon)):
                            print("\n ", tampon[i], "SUPPORT =", support(final, tampon[i]))
                        enum = enum + 1
                    else:
                        print("\n \n AUCUNE SEQUENCE DE LONGUEUR :", enum + 2, "AYANT UN SUPPORT SUPERIEUR A :", min_sup, "N'A ETE TROUVEE")
                        break

            elif sequence_menant_a_un_achat == 'Y' or sequence_menant_a_un_achat == 'y':

                tampon = []
                frequent = generate_frequent(final, min_sup, k)
                for i in range(len(frequent)):
                    for j in range(len(frequent[i])):
                        if frequent[i][j] in id_product_choisis:
                            tampon.append(frequent[i])
                l = [[]]
                enum = k - 1
                renvoi = []
                for i in range(len(tampon)):
                    if tampon[i][0] not in id_product_choisis:
                        renvoi.append(tampon[i])
                if len(renvoi) == 0:
                    print("\n \n AUCUNE SEQUENCE DE LONGUEUR :", k, "AYANT UN SUPPORT SUPERIEUR A :", min_sup, "N'A ETE TROUVEE")
                else:
                    print("\n \n IL Y A : ", len(renvoi), "SEQUENCES DE LONGUEUR : ", len(renvoi[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                    for i in range(len(renvoi)):
                        print("\n ", renvoi[i], "SUPPORT =", support(final, renvoi[i]))

                while tampon != l:
                    tampon = []
                    tamp = []  # . ---------------------------------------------|
                    for i in frequent:  # .                                     |
                        for j in frequent:  # .                                 |
                            if i[1:] == j[:len(j) - 1]:  # .                    |
                                list_tampon = deepcopy(i)  # .                  |> TOUT CA SERT POUR LES CANDIDATS k-SEQUENTS
                                list_tampon.append(j[len(j) - 1])  # .          |
                                tamp.append(list_tampon)  # .                   |

                    candidat = tamp
                    tamp_candidat = []
                    list_a_regarder = []
                    for i in range(len(final)):
                        if len(final[i]) >= k:
                            list_a_regarder.append(final[i])

                    for elt in candidat:
                        count = 0
                        for i in range(len(list_a_regarder)):
                            if are_present(list_a_regarder[i], elt) is True:
                                count = count + 1
                        if count / len(final) >= min_sup:
                            tamp_candidat.append(elt)


                    frequent = tamp_candidat
                    sequences = []
                    for elt in frequent:
                        for j in range(len(elt)):
                            if elt[j] in id_product_choisis:
                                tampon.append(elt)
                    renvoi = []
                    for i in range(len(tampon)):
                        if tampon[i][0] not in id_product_choisis:
                            renvoi.append(tampon[i])

                    if len(renvoi) != 0:
                        print("\n \n \nIL Y A : ", len(renvoi), "SEQUENCES DE LONGUEUR : ", len(renvoi[0]), "AYANT UN SUPPORT SUPERIEUR A :", min_sup)
                        for i in range(len(renvoi)):
                            print("\n ", renvoi[i], "SUPPORT =", support(final, renvoi[i]))
                        enum = enum + 1
                    else:
                        print("\n \n AUCUNE SEQUENCE DE LONGUEUR :", enum + 2, "AYANT UN SUPPORT SUPERIEUR A :", min_sup, "N'A ETE TROUVEE")
                        break


manque = input("\n \n VOULEZ VOUS SAVOIR POUR UNE SEQUENCE PRECISE COMBIEN D'UTILISATEURS ONT REALISE CETTE SEQUENCE SANS CONCLURE SUR UN ACHAT ? \n \n           TAPEZ Y SI VOUS LE SOUHAITEZ \n \n           TAPEZ N SINON  \n \n           VOTRE CHOIX : ")

if manque == 'Y' or manque == 'y':
    leq = input("\n \n VEUILLEZ SAISIR LA SEQUENCE SOUHAITEE \n \n           POUR LA SEQUENCE ['desktop', 'mobile_web', 'mobile_web', 'purchase'] ECRIVEZ : desktop mobile_web mobile_web purchase \n \n           ELLE DOIT FINIR PAR UN ACHAT \n \n           VOTRE CHOIX : ")
    seq = leq.split()
    sequence_sans_achat = deepcopy(seq)
    del sequence_sans_achat[-1]
    nbre_users = 0
    for i in range(len(final)):
        if nombre_apparition(final[i], sequence_sans_achat) != 0:
            nbre_users = nbre_users + 1


    print("\n \n LA SEQUENCE :", sequence_sans_achat, "A ETE REALISE :", nombre_apparition(final, sequence_sans_achat), "FOIS.\n\n ELLE A MENE A UN ACHAT :", nombre_apparition(final, seq) ," FOIS, ET N'A PAS MENE A UN ACHAT :", achat_manque(final, seq), "FOIS")

