import os
import subprocess
import time

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode().strip()}")
    else:
        print(stdout.decode().strip())

def create_laravel_project(project_name, with_jetstream=False):
    # Crear proyecto Laravel
    print(f"Creando el proyecto Laravel '{project_name}'...")
    run_command(f"composer create-project laravel/laravel {project_name}")

    # Cambiar al directorio del proyecto
    os.chdir(project_name)

    if with_jetstream:
        # Instalar Jetstream
        print("Instalando Jetstream...")
        run_command("composer require laravel/jetstream")

        # Ejecutar el comando para seleccionar Inertia.js
        print("Configurando Jetstream con Inertia.js...")
        run_command("php artisan jetstream:install inertia")

def create_django_project(project_name):
    # Crear proyecto Django
    print(f"Creando el proyecto Django '{project_name}'...")
    run_command(f"django-admin startproject {project_name}")

    os.chdir(project_name)

    app_name = input("¿Cuál es el nombre de la aplicación? ")

    # Crear aplicación Django
    print(f"Creando la aplicación Django '{app_name}'...")
    run_command(f"python3 manage.py startapp {app_name}")

    # Crear archivo urls.py en la aplicación
    app_urls_path = os.path.join(app_name, 'urls.py')
    with open(app_urls_path, 'w') as file:
        file.write("from django.urls import path\n")
        file.write("from . import views\n\n")
        file.write("urlpatterns = [\n")
        file.write("    # path('', views.index, name='index'),\n")
        file.write("]\n")

    # Añadir la aplicación al archivo settings.py
    settings_path = os.path.join(project_name, 'settings.py')
    with open(settings_path, 'r') as file:
        settings_content = file.readlines()

    with open(settings_path, 'w') as file:
        for line in settings_content:
            file.write(line)
            if line.strip() == 'INSTALLED_APPS = [':
                file.write(f"    '{app_name}',\n")

    # Añadir la ruta de la aplicación al archivo urls.py del proyecto
    project_urls_path = os.path.join(project_name, 'urls.py')
    with open(project_urls_path, 'r') as file:
        urls_content = file.readlines()

    with open(project_urls_path, 'w') as file:
        for line in urls_content:
            if line.strip() == "from django.urls import path":
                file.write(line)
                file.write(f"from django.urls import include\n")
            elif line.strip() == "urlpatterns = [":
                file.write(line)
                file.write(f"    path('{app_name}/', include('{app_name}.urls')),\n")
            else:
                file.write(line)

    # Crear directorio models con archivo __init__.py y añadir modelo Test
    models_dir_path = os.path.join(app_name, 'models')
    os.makedirs(models_dir_path)
    with open(os.path.join(models_dir_path, '__init__.py'), 'w') as file:
        file.write("from django.db import models\n\n")
        file.write("class Test(models.Model):\n")
        file.write("    name = models.CharField(max_length=100)\n\n")
        file.write("    def __str__(self):\n")
        file.write("        return self.name\n")

def main():
    print("Seleccione el tipo de proyecto que desea crear:")
    print("1. Laravel")
    print("2. Laravel con Jetstream (Inertia.js)")
    print("3. Django")

    choice = input("Ingrese el número de la opción deseada: ")

    project_name = input("¿Cuál es el nombre del proyecto? ")

    if choice == '1':
        create_laravel_project(project_name)
    elif choice == '2':
        create_laravel_project(project_name, with_jetstream=True)
    elif choice == '3':
        create_django_project(project_name)
    else:
        print("Opción no válida. Saliendo del script.")
        return

    print("Proyecto configurado con éxito.")

if __name__ == "__main__":
    main()
