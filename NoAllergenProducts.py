"""
author : decoopmc
"""

import openfoodfacts as openFF
import pandas as pd



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
        self.allergens       = _allergen
        self.NoAllergenProds = self.getNoAllergenProds()


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



    def getAllProdsName(self, country) :
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



    def getAllergenProdsName(self) :
        """
        Retourne la liste des noms des produits contenant
        le ou les allergenes specifies
        RETURN type : list[string]
        """
        ret = []
        for allergen in self.allergens :
            products = openFF.products.get_by_allergen(allergen)
            for prod in products :
                ret.append(prod['product_name'])

        return ret



    def getNoAllergenName(self, country) :
        """
        Recupere la liste des noms des produits ne contenant
        pas les allergenes specificies
        PARAM country : code pays
        """
        allergenProds   = set(self.getAllergenProdsName())     # produits allergenes cast en set
        allProds        = set(self.getAllProdsName(country))   # tous les produits selon le pays cast en set
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
        # temp = {}
        products   = openFF.products.get_by_language(country)     # Tous les produits selon le pays
        noAllergen = self.getNoAllergenName(country)              # Tous les produits non allergen (specifiques) selon le pays

        for prod in products :
            for noAl in noAllergen :
                if prod['product_name'] == noAl :
                    # temp = {'id' : prod['id'],
                    #         'name' : prod['product_name']}
                    ret.append(prod)

        return ret



    def toDataFrame(self, dataTab = []) :
        """
        Converti en DataFrame les donnees en parametre
        PARAM dataTab : donnees a convetir
        PARAM TYPE : list[dict]
        """
        colNames = dataTab[0].keys()        # noms des colonnes
        rows     = []                       # lignes
        dfDict   = {}                       # dictionnaire du DataFrame
        df       = None                     # DataFrame

        # RECUPERATION DES DONNEES DE CHAQUE PRODUIT
        for data in dataTab :
            rows.append(data.values())      # donnees de chaque produit sous forme de ligne

        # MISE EN FORME DU DATAFRAME
        for c,r in colNames,rows :
            dfDict[c] = r
        df = pd.DataFrame(dfDict)

        return df



    def toCsv(self, df) :
        """
        Converti en CSV les champs (et leurs indexes) des produits non
        concernes par les allergenes specifies
        PARAM df : DataFrame des donnees a ecrire
        """
        ret = df.to_csv()
        return ret



    def toExcel(self, df, filename, sheetname) :
        """
        Converti en Excel les champs (et leurs indexes) des produits non
        concernes par les allergenes specifies
        PARAM df : DataFrame des donnees a ecrire
        PARAM filename : nom du fichier excel
        PARAM sheetname : nom de la feuille excel ou l'on ecrit les donnees
        """
        df.to_excel(filename, sheetname)
