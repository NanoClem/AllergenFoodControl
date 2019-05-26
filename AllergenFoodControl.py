"""
author : decoopmc
"""

import openfoodfacts as openFF
import pandas as pd
import json



class AllergenFoodControl :
    """
    Cette classe modelise les differents produits d'OpenFoodFacts
    selon certaines specifications de l'utilisateur, notamment
    sur les produits allergenes
    """

    def __init__(self, _allergen) :
        """
        CONSTRUCTEUR de la classe AllergenFoodControl
        ATTRIBUTE allergen : liste des allergenes specifies par l'utilisateur
        """
        self.allergen = _allergen



    def getAllProds(self, country) :
        """
        Retourne la liste de tous les noms des produits
        selon le pays
        PARAM country : code pays
        """
        ret = []
        products = openFF.products.get_by_language("fr")
        for prod in products :
            #if 'product_name' in prod.keys() :                  # Apparemment, ce champ n'existe pas pour tous les produits
            ret.append(prod['product_name'])

        return ret



    def getAllergenProds(self) :
        """
        Retourne la liste des noms des produits contenant
        le ou les allergenes specifies
        RETURN type : list[string]
        """
        ret = []
        products = openFF.products.get_by_allergen(self.allergen)
        for prod in products :
            ret.append(prod['product_name'])

        return ret



    def getNoAllergen(self, country) :
        """
        Recupere la liste des noms des produits ne contenant
        pas les allergenes specificies
        PARAM country : code pays
        """
        allergenProds   = set(self.getAllergenProds())         # produits allergenes cast en set
        allProds        = set(self.getAllProds(country))       # tous les produits selon le pays cast en set
        ret             = list(allProds - allergenProds)       # liste des produits non allergenes

        return ret



    def getNoAllergenProds(self, country) :
        """
        Retourne la liste des produits ne contenant pas
        les allergenes specifies
        PARAM country : code pays
        RETURN TYPE : list[dict]
        """
        ret  = []
        temp = {}
        products   = openFF.products.get_by_language(country)     # Tous les produits selon le pays
        noAllergen = self.getNoAllergen(country)                  # Tous les produits non allergen (specifiques) selon le pays

        for prod in products :
            for noAl in noAllergen :
                if noAl in prod['product_name'] :                 # Apparemment, ce champ n'existe pas pour tous les produits
                    temp = {'id'                   : prod['id'],
                            'name'                 : prod['product_name'],
                            'brand'                : prod['brands'],
                            'ingredients'          : prod['ingredients'],
                            'ingredients_allergen' : prod['allergens_from_ingredients'],
                            'url'                  : prod['url']}
                    ret.append(temp)

        return ret



    def toDataFrame(self, data = []) :
        """
        Converti en DataFrame les donnees en parametre
        PARAM data : donnees a convetir
        PARAM TYPE : list[dict]
        """
        df = pd.DataFrame.from_dict(data, orient='columns')
        return df



    def toJSON(self, df) :
        """
        Converti le DataFrame en format JSON
        """
        ret = json.dumps(df, indent=4)
        return ret



    def toCsv(self, df, filename) :
        """
        Converti en CSV les champs (et leurs indexes) des produits non
        concernes par les allergenes specifies
        PARAM df : DataFrame des donnees a ecrire
        """
        df.to_csv(filename, encoding='utf-8', index = False)



    def toExcel(self, df, filename, sheetname) :
        """
        Converti en Excel les champs (et leurs indexes) des produits non
        concernes par les allergenes specifies
        PARAM df : DataFrame des donnees a ecrire
        PARAM filename : nom du fichier excel
        PARAM sheetname : nom de la feuille excel ou l'on ecrit les donnees
        """
        df.to_excel(filename, sheetname)
