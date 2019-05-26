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
        print("################## PRODUIT SUIVANT ##################")
        print(prod['product_name'])
        print(prod['id'])
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

    country     = "fr"   # code pays
    spec        = input("Quel allergène voulez-vous éviter ?  > ")

    #======================================================================
    #   CLASSE NoAllergenProducts
    #======================================================================
    AFC = AllergenFoodControl(spec)
    NoAllergenProds = AFC.getNoAllergenProds(country)  # produits sans les allergènes

    #======================================================================
    #   DATAFRAME ET CSV
    #======================================================================
    foodDF = AFC.toDataFrame(NoAllergenProds)
    AFC.toExcel(foodDF, "Safe_Products.csv", "products")    # Conversion Excel
    #AFC.toCsv(foodDF, "Safe_Products.csv")






if __name__ == '__main__':

    # FONCTIONS DE TEST
    # printAllergens("fr")
    # printProducts("fr")

    main()
