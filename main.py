import openfoodfacts as openFF



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


def printProductsByAllergen(allergen) :
    """
    Affiche les produits contenant
    l'allergene specifique
    PARAM allergen : id de l'allergene
    """
    products = openFF.products.get_by_allergen(allergen)
    for prod in products :
        print("==========================================================")
        print("################## PRODUIT SUIVANT ##################")
        # for key,value in prod.items() :
        #     print(key + ":", value)
        print(prod['product_name'])
        print("==========================================================")


def printProducts(country) :
    """
    Affiche les éléments du produit selon le pays
    PARAM country : code pays
    """
    products = openFF.products.get_by_language("fr")
    for key,value in products[0].items() :
        print(key + ":", value)




def main() :
    country = "fr"
    spec    = "fr:lait-de-savoie"
    #printAllergens(country)
    #printProducts(country)
    printProductsByAllergen(spec)



if __name__ == '__main__':
    main()
