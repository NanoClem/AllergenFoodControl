import openfoodfacts as openFF
from AllergenFoodControl import AllergenFoodControl



def printAllergens(country) :
    """
    Affiche les allergenes selon le pays
    PARAM country : code pays
    """
    allergens = openFF.facets.get_allergens()       # allergenes disponibles
    country += ":"
    for prod in allergens :
        if country in prod['name'] :
            print(prod)



def printProducts(country) :
    """
    Affiche les éléments du produit selon le pays
    PARAM country : code pays
    """
    products = openFF.products.get_by_language("fr")
    for prod in products :
        print("==========================================================")
        print("################## PRODUIT SUIVANT ##################")
        for key,value in prod.items() :
            print(key + ":", value)
        # print(prod['product_name'])
        # print(prod['id'])
        print("==========================================================")



def getAllergens(country) :
    """
    Retourne la liste des noms de tous les
    allergenes disponibles selon le pays
    PARAM country : code pays
    """
    ret = []
    allerg = openFF.facets.get_allergens()      # allergenes disponibles
    country += ":"
    for prod in allerg :
        id = prod['id']
        if country in id :                      # si l'allergene est disponible dans la langue du pays specifie
            toAppend = id.split(':')[1]         # formatage str (enlever le code pays)
            ret.append(toAppend)                # on recupere le nom de l'allergene

    return ret



#__________MAIN__________

def main() :
    country = "fr"
    spec    = getAllergens(country)


    #======================================================================
    #   FONCTIONS DE TEST
    #======================================================================
    #printAllergens(country)
    #printProducts(country)


    #======================================================================
    #   CLASSE NoAllergenProducts
    #======================================================================
    AFC = AllergenFoodControl(spec)

    # PRODUITS CONTENANT LES ALLERGENES SPECIFIES
    # AllergenProds = AFC.getAllergenProds()
    # for prod in AllergenProds :
    #     print(prod)


    #======================================================================
    #   TESTS AVEC LA CLASSE AllergenFoodControl
    #======================================================================
    # CONVERSION EN DATAFRAME
    # testDF = [  {'nom' : 'Clément', 'formation' : 'IDU'},
    #             {'nom' : 'Maxime',  'formation' : 'IAI'},
    #             {'nom' : 'July',    'formation' : 'MM' }  ]
    # df = AFC.toDataFrame(testDF)
    # print(df)
    #
    # # FICHIER CSV OU EXCEL
    # AFC.toExcel(df, "Etudiants.xlsx", "Polytech")





if __name__ == '__main__':
    main()
