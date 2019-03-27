"""
author : decoopmc
"""

import openfoodfacts as openFF



class NoAllergenProducts :
    """
    Cette classe modelise les differents produits d'OpenFoodFacts
    selon certaines specifications de l'utilisateur
    """

    def __init__(self, _allergen = []) :
        """
        CONSTRUCTEUR de la classe Products
        ATTRIBUTE allergen : liste des allergenes specifies par l'utilisateur
        ATTRIBUTE allergenProds : liste des noms des produits contenant les allergenes specifies
        """
        self.allergens     = _allergen


    def getAllergens(self, country) :
        """
        Retourne la liste des noms de tous les
        allergenes disponibles selon le pays
        PARAM country : code pays
        """
        ret = []
        allerg = openFF.facets.get_allergens()                    # allergenes disponibles
        country += ":"
        for prod in allerg :
            id = prod['product_name']                                       # id de chaque allergene
            if country in id :                                    # si le code pays correspond a l'allergene
                toAppend = id.split(':')[1].replace('-', ' ')     # formatage str (code pays et - en moins)
                ret.append(toAppend)                              # on recupere le nom de l'allergene

        return ret



    def getAllProds(self, country) :
        """
        Retourne la liste de tous les noms des produits
        selon le pays
        PARAM country : code pays
        """
        ret = []
        products = openFF.products.get_by_language("fr")
        for prod in products :
            ret.append(prod['product_name'])

        return ret


    def getAllergenProds(self) :
        """
        Retourne la liste des noms des produits contenant
        le ou les allergenes specifies
        RETURN type : list[<string>]
        """
        ret = []
        for allergen in self.allergens :
            products = openFF.products.get_by_allergen(allergen)
            for prod in products :
                ret.append(prod['product_name'])

        return ret



    def getNoAllergenProd(self, country) :
        """
        """
        allergenProds   = set(self.getAllergenProds())     # produits allergenes cast en set
        allProds        = set(self.getAllProds(country))   # tous les produits selon le pays cast en set
        ret             = list(allProds - allergenProds)   # liste des produits non allergenes

        return ret
