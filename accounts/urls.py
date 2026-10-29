from django.urls import path
from .views import (LoginUserView, LogoutUserView, ProfileView, EmployeeListView, 
                EmployeeDetailView, CreateEmployeeView, UpdateEmployeeView, DeleteEmployeeView,)

urlpatterns = [
    # path('register/', RegisterView.as_view(), name='register'),
    # path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    # employee==============
    path('profile/', ProfileView.as_view(), name='profile'),
    path('employees/', EmployeeListView.as_view(), name='employee_list'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('create-employee/', CreateEmployeeView.as_view(), name='create_employee'),
    path('update-employee/<int:pk>/', UpdateEmployeeView.as_view(), name='update_employee'),
    path('delete-employee/<int:pk>/', DeleteEmployeeView.as_view(), name='delete_employee'),
    
    

]