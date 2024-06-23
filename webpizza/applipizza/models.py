from django.db import models

# Create your models here.

class Ingredient(models.Model) :

    #idIngredient est une clé primaire, n auto-incrément => AutoField
    idIngredient = models.AutoField(primary_key = True)

    #nomIngredient est une chaine de carctères => Charfield
    nomIngredient = models.CharField(max_length = 50, verbose_name ='le nom')


    #une méthode de type "toString"
    def __str__(self) -> str :
        return self.nomIngredient



class Pizza(models.Model) :

    #idPizza est une clé primaire, n auto-incrément => AutoField
    idIPizza = models.AutoField(primary_key = True)

    #nomPizza est une chaine de carctères => Charfield
    nomPizza = models.CharField(max_length = 50, verbose_name ='le nom de cette Pizza')

    prix = models.DecimalField(max_digits = 4, decimal_places = 2, verbose_name = 'le prix')

    image = models.ImageField(default= 'imagesPizzas/default.PNG', upload_to = 'imagesPizzas/')

    #une méthode de type "toString"
    def __str__(self) -> str :
        return 'pizza ' + self.nomPizza + ' (prix : ' + str(self.prix) + ' €)'



class Composition(models.Model) :

    #la classe Meta qui gère l'unicité du couple de clés étrangères 
    class Meta : 
        unique_together = ('ingredient','pizza')  # le nom des champs clés étrangères

    #idComposition est la clé primaire
    idComposition = models.AutoField(primary_key = True)

    #les deux champs clés étrangères dont les noms correspondent 
    #aux classes respectives, en minuscules

    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete = models.CASCADE)

    quantite = models.CharField(max_length = 100, verbose_name = 'la quantité')

    def __str__(self) -> str :
        ing = self.ingredient
        piz = self.pizza
        return ing.nomIngredient + ' fait partie de la pizza ' + piz.nomPizza + ' (quantité : ' + self.quantite + ' )'