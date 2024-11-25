from git import Repo
import shutil
import os

class OdooDockerClone:
    
    def __init__(self):
        self.localDir = "~/Odoo-Image-BuilderOdooCloneDir"
        
    async def cloneOdoo(self, dir):    
        if os.path.exists(self.localDir) and os.listdir(self.localDir):
            print('Folder exists and already cloned')
            shutil.move(f'{self.localDir}/{dir}.0/Dockerfile', f"~/Odoo-Image-Builder{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/odoo.conf', f"~/Odoo-Image-Builder{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/entrypoint.sh', f"~/Odoo-Image-Builder{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/wait-for-psql.py', f"~/Odoo-Image-Builder{dir}")
        else:
            print('Cloning odoo docker files')
            Repo.clone_from('https://github.com/odoo/docker.git', self.localDir)
            shutil.move(f'{self.localDir}/{dir}.0/Dockerfile', f"~/Odoo-Image-Builder{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/odoo.conf', f"~/Odoo-Image-Builder{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/entrypoint.sh', f"~/Odoo-Image-Builder{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/wait-for-psql.py', f"~/Odoo-Image-Builder{dir}")
            print('Odoo docker files cloned and moved')
