from git import Repo
import shutil
import os

class OdooDockerClone:
    
    def __init__(self):
        self.localDir = "/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/OdooCloneDir"
        
    async def cloneOdoo(self, dir):    
        if os.path.exists(self.localDir) and os.listdir(self.localDir):
            print('Folder exists and already cloned')
            shutil.move(f'{self.localDir}/{dir}.0/Dockerfile', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/odoo.conf', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/entrypoint.sh', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/wait-for-psql.py', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
        else:
            print('Cloning odoo docker files')
            Repo.clone_from('https://github.com/odoo/docker.git', self.localDir)
            shutil.move(f'{self.localDir}/{dir}.0/Dockerfile', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/odoo.conf', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/entrypoint.sh', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
            shutil.move(f'{self.localDir}/{dir}.0/wait-for-psql.py', f"/home/osama/Desktop/ubuntu-machine-for-jenkins/Image Creation Automation/{dir}")
            print('Odoo docker files cloned and moved')
