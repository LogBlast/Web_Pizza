"""
URL configuration for webpizza project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from applipizza import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pizzas/', views.pizzas),
    path('ingredients/', views.ingredients),
    path('pizzas/<int:pizza_id>/', views.pizza),

    # l'utilisateur doit arriver sur la page de formulaire quand il appuie sur 'créer un ingrédient' avec pour url ingredients/add/
    path('ingredients/add/', views.formulaireCreationIngredient),
    # l'utilisateur doit arriver sur la page de la création de l'ingrédient quand il appuie, sur le formulaire, sur le bouton 'suivant' avec pour url ingredients/create/
    path('ingredients/create/', views.creerIngredient),

    path('ingredients/<int:ingredient_id>/delete/', views.supprimerIngredient),
    path('ingredients/<int:ingredient_id>/update/', views.afficherFormulaireModificationIngredient),
    path('ingredients/<int:ingredient_id>/updated/', views.modifierIngredient),



    
    path('pizzas/add/', views.formulaireCreationPizza),
    path('pizzas/create/', views.creerPizza),

    path('pizzas/<int:pizza_id>/addIngredient/', views.ajouterIngredientDansPizza),

    path('pizzas/<int:pizza_id>/delete/', views.supprimerPizza),
    path('pizzas/<int:pizza_id>/update/', views.afficherFormulaireModificationPizza),
    path('pizzas/<int:pizza_id>/updated/', views.modifierPizza),
    path('pizzas/<int:pizza_id>/deleteIngredient/<int:composition_id>/', views.supprimerIngredientDansPizza),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
