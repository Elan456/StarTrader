import PyInstaller.__main__
import os
import shutil

# # Delete the dist folder if it exists
# if os.path.exists("dist"):
#     shutil.rmtree("dist")

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
])

copy_assets = input("Copy assets? (y/n): ") == "y"
if copy_assets:
    # Create a copy of the assets folder and put it in the dist folder
    os.system("xcopy assets dist\\assets /E /I /Y")

    # Copy module/Modules.ods to dist folder within module folder
    os.makedirs("dist\\module", exist_ok=True)
    shutil.copy("module\\Modules.ods", "dist\\module\\Modules.ods")

    # Copy enemyships to dist folder
    os.system("xcopy enemyships dist\\enemyships /E /I /Y")
