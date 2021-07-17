from django.urls import path
from . import views
urlpatterns = [
    path('', views.index,name="index"),
    path('login',views.login_view,name="login"),
    path('register',views.register,name="register"),
    path('logout',views.logout_view,name="logout"),
    path("search",views.search,name="search"),
    path("importCsv",views.book_csv,name="index"),
    path("books_select",views.list_books,name="machineLearn"),
    path("book/<int:id>",views.details,name="details"),
    path("add/<int:id>",views.add,name="add"),
    path("add_summary/<int:id>",views.add_summary,name="add_summary")
]