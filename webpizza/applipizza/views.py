from django.shortcuts import render


#import des modèles
from applipizza.models import Pizza
from applipizza.models import Ingredient
from applipizza.models import Composition

from applipizza.forms import CompositionForm, IngredientForm
from applipizza.forms import PizzaForm



# Create your views here.
def pizzas(request) : 
    #récupération des pizzas de la base de données
    #avec les mêmes instructions que dans le shell

    lesPizzas = Pizza.objects.all()

    #on retourne l'emplacement du template et, même
    #s'il ne sert pas cette fois, la paramètre
    # request, ainsi que le contenu calculé (lesPizzas)
    # sous forme d'un dictionnaire python

    return render(
        request,
        'applipizza/pizzas.html',
        {'pizzas' : lesPizzas}
    )


def ingredients(request) : 
    #récupération des ingrédients de la base de données
    #avec les mêmes instructions que dans le shell

    lesIngredients = Ingredient.objects.all()

    #on retourne l'emplacement du template et, même
    #s'il ne sert pas cette fois, la paramètre
    # request, ainsi que le contenu calculé (lesPizzas)
    # sous forme d'un dictionnaire python

    return render(
        request,
        'applipizza/ingredients.html',
        {'ingredients' : lesIngredients}
    )

def pizza(request, pizza_id) : 
    #récupération de la pizza dont l'id a été
    #passé en paramètre

    laPizza = Pizza.objects.get(idIPizza=pizza_id)
   
    #récupération des ingrédients entrant dans la composition de la pizza
    lesCompositions = Composition.objects.filter(pizza=pizza_id)

    #construction d'une liste d'ingrédients
    #avec leur quantité
    ingredients = []
    for composition in lesCompositions :
        ingredients.append({
            'idComposition' : composition.idComposition,
            'nomIngredient' : composition.ingredient.nomIngredient,
            'quantite' : composition.quantite
        })

    lesIngredients = Ingredient.objects.all()

    #on retourne l'emplacement du template, la pizza récupérée de la base
    #et la liste des ingrédients calculée ci-dessus

    return render(
        request,
        'applipizza/pizza.html',
        {'pizza' : laPizza, 'ingredients' : ingredients, "lesIng": lesIngredients}
    )

def formulaireCreationIngredient(request) : 
    #On retourne l'emplacement du template
    return render(
        request,
        'applipizza/formulaireCreationIngredient.html',
    )

def creerIngredient(request):
    # Récupération du formulaire posté
    form = IngredientForm(request.POST)

    # Si le formulaire est valide
    if form.is_valid():
        # Récupération de la valeur du champ nomIngredient
        nomIng = form.cleaned_data['nomIngredient']

        # Création d'un nouvel ingrédient
        ing = Ingredient()

        # Affectation de son attribut nomIngredient
        ing.nomIngredient = nomIng

        # Enregistrement de l'ingrédient dans la base
        ing.save()

        # Retour du contenu calculé
        return render(
            request,
            'applipizza/traitementFormulaireCreationIngredient.html',
            {'nom': nomIng},
        )
    else:
        return render(
            request,
            'applipizza/formulaireCreationIngredient.html',
            {'form': form},
        )
    
    

def formulaireCreationPizza(request) : 
    #On retourne l'emplacement du template
    return render(
        request,
        'applipizza/formulaireCreationPizza.html',
    )

def creerPizza(request):
    form = PizzaForm(request.POST)
    if form.is_valid():
        pizza = Pizza(
            nomPizza=form.cleaned_data['nomPizza'],
            prix=form.cleaned_data['prix'],
            image=request.FILES['image'],
        )

        pizza.save()
        return render(
            request,
            'applipizza/traitementFormulaireCreationPizza.html',
            {'pizza': pizza}
        )
    
    else:
        return render(
            request,
            'applipizza/formulaireCreationPizza.html',
            {'form': form},
        )
    

def ajouterIngredientDansPizza(request, pizza_id):
    # récupération du formulaire posté
    formulaire = CompositionForm(request.POST)

    if formulaire.is_valid():
        # récupération des données postées
        ing = formulaire.cleaned_data['ingredient']
        qte = formulaire.cleaned_data['quantite']
        piz = Pizza.objects.get(idIPizza=pizza_id)
        compoPizza = Composition.objects.filter(pizza=pizza_id)
        lesIngredientsDeLaPizza = ((ligne.ingredient) for ligne in compoPizza)

        # suppression de l'ingrédient si déjà présent
        if ing in lesIngredientsDeLaPizza:
            compo = Composition.objects.filter(pizza=pizza_id, ingredient=ing)
            compo.delete()

        # création de la nouvelle instance de Composition et remplissage des attributs
        compo = Composition()
        compo.ingredient = ing
        compo.pizza = piz
        compo.quantite = qte
        # sauvegarde dans la base de la composition
        compo.save()

    # récupération de tous les ingrédients pour construire le futur select
    lesIngredients = Ingredient.objects.all()

    # actualisation des Ingrédients entrant dans la composition de la pizza
    compoPizza = Composition.objects.filter(pizza=pizza_id)

    # on crée une liste dont chaque item contiendra l'identifiant de la composition (idComposition),
    # le nom de l'ingrédient et la quantité de l'ingrédient dans cette composition
    listeIngredients = []
    for ligneCompo in compoPizza:
        # on récupère l'Ingredient pour utiliser son nomIngredient
        ingredient = Ingredient.objects.get(idIngredient=ligneCompo.ingredient.idIngredient)
        listeIngredients.append({
            "idComposition": ligneCompo.idComposition,
            "nomIngredient": ingredient.nomIngredient,
            "quantite": ligneCompo.quantite
        })

    # on retourne l'emplacement du template, la pizza récupérée et la liste des ingrédients calculée ci-dessus
    return render(
        request,
        "applipizza/pizza.html",
        {"pizza": piz, "ingredients": listeIngredients, "lesIng": lesIngredients}
    )



## TP 8

## Partie sur la Pizza


def supprimerPizza(request, pizza_id):

    # Récupération de la pizza à supprimer
    pizza = Pizza.objects.get(idIPizza=pizza_id)

    # Suppression de la pizza
    pizza.delete()

    # Récupération de la liste de toutes les pizzas
    lesPizzas = Pizza.objects.all()

    # Retour de la liste des pizzas
    return render(
        request,
        "applipizza/pizzas.html",
        {'pizzas': lesPizzas}
    )

def afficherFormulaireModificationPizza(request, pizza_id):
    pizza_a_modifier = Pizza.objects.get(idIPizza=pizza_id)
    return render(
        request,
        "applipizza/formulaireModificationPizza.html",
        {"pizza": pizza_a_modifier}
    )

def modifierPizza(request, pizza_id):

    # Récupération de la pizza à modifier
    pizza = Pizza.objects.get(idIPizza=pizza_id)

    # Récupération du formulaire posté
    form = PizzaForm(request.POST, request.FILES, instance=pizza)

    # Si le formulaire est valide
    if form.is_valid():

        pizza.image = request.FILES['image']

        # Mise à jour de la pizza
        form.save()

        # Récupération de la pizza modifiée
        pizzaModif = Pizza.objects.get(idIPizza=pizza_id)

        return render(
        request,
        'applipizza/traitementFormulaireModificationPizza.html',
        {'pizza': pizzaModif}
    )


## Partie sur l'ingrédient
    
def supprimerIngredient(request, ingredient_id):

    # Récupération de l'ingrédient à supprimer
    ingredient = Ingredient.objects.get(idIngredient=ingredient_id)

    # Suppression de l'ingrédient
    ingredient.delete()

    # Récupération de la liste de tous les ingrédients
    lesIngredients = Ingredient.objects.all()

    # Retour de la liste des ingrédients
    return render(
        request,
        "applipizza/ingredients.html",
        {'ingredients': lesIngredients}
    )


def afficherFormulaireModificationIngredient(request, ingredient_id):
    ingredient_a_modifier = Ingredient.objects.get(idIngredient=ingredient_id)
    return render(
        request,
        "applipizza/formulaireModificationIngredient.html",
        {"ingredient": ingredient_a_modifier}
    )



def modifierIngredient(request, ingredient_id):
    
        # Récupération de l'ingrédient à modifier
        ingredient = Ingredient.objects.get(idIngredient=ingredient_id)
    
        # Récupération du formulaire posté
        form = IngredientForm(request.POST, instance=ingredient)
    
        # Si le formulaire est valide
        if form.is_valid():
            # Mise à jour de l'ingrédient
            form.save()
    
            # Récupération de l'ingrédient modifié
            ingredientModif = Ingredient.objects.get(idIngredient=ingredient_id)
    
            return render(
            request,
            'applipizza/traitementFormulaireModificationIngredient.html',
            {'ingredient': ingredientModif}
        )

## TP9

def supprimerIngredientDansPizza(request, pizza_id, composition_id):

    # Récupération de la composition à supprimer
    composition = Composition.objects.get(idComposition=composition_id)

    # Appel de la méthode delete() sur cette composition
    composition.delete()

    # Récupération de la pizza dont l’idPizza est passé en paramètre
    pizza = Pizza.objects.get(idIPizza=pizza_id)

    # Récupération de toutes les compositions concernant la pizza dont l’idPizza est passé en paramètre
    lesCompositions = Composition.objects.filter(pizza=pizza_id)

    # Refabriquer la liste des ingrédients de la pizza
    ingredients = []
    for composition in lesCompositions:
        ingredient = Ingredient.objects.get(idIngredient=composition.ingredient.idIngredient)
        ingredients.append({
            "idComposition": composition.idComposition,
            "nomIngredient": ingredient.nomIngredient,
            "quantite": composition.quantite
        })

    # Créer un nouveau formulaire CompositionForm
    form = CompositionForm()

    lesPizzas = Pizza.objects.all()

    # Appel du template pizzas.html en lui fournissant la liste des pizzas (comme dans la vue pizzas), le formulaire, et la pizza
    return render(
        request,
        "applipizza/pizza.html",
        {
            "pizzas": lesPizzas,
            "form": form,
            "pizza": pizza,
            "ingredients": ingredients,
        },
    )

    
    
