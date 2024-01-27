from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path("UserLogin", views.UserLogin, name="UserLogin"),
	       path("User.html", views.User, name="User"),
	       path("Register.html", views.Register, name="Register"),
	       path("Signup", views.Signup, name="Signup"),	    
	       path("AuthImageAction", views.AuthImageAction, name="AuthImageAction"),	
	       path("LoginAuthImageAction", views.LoginAuthImageAction, name="LoginAuthImageAction"),
	       path("UploadFile.html", views.UploadFile, name="UploadFile"),
	       path("UploadFileAction", views.UploadFileAction, name="UploadFileAction"),
	       path("DownloadFile", views.DownloadFile, name="DownloadFile"),
	        path("DownloadFileAction", views.DownloadFileAction, name="DownloadFileAction"),
]