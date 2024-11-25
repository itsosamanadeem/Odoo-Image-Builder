import os
import time
import docker
import docker.errors
import asyncio
import shutil
from datetime import date
from odooAutomation import downloadOdooDebian
from odooAutomation import gitCloneOdoo
from odooAutomation import AdjustDockerfile

class OdooImage:
    def __init__(self):
        self.dir = "~/Odoo-Image-Builder/"
        self.client = docker.from_env()
    
    # async def dockerBuild(self):
    #     try:
    #         print("Building Docker images...")
    #         await self.check_odooDebian()

    #         for build in range(16, 19):
    #             build_path = f"{self.dir}/{build}"
    #             if not os.path.exists(build_path):
    #                 print(f"Build directory {build_path} does not exist.")
    #                 continue
    #             print(f"Starting build for Odoo version {build}.0...")

    #             image, logs = self.client.images.build(
    #                 path=build_path, 
    #                 tag=f"odoo_{build}:{date.today()}", 
    #                 rm=True
    #             )

    #             for log in logs:
    #                 if 'stream' in log:
    #                     print(log['stream'].strip())  

    #             print(f"Docker image for version {image.id} and odoo{build}.0 built successfully!")
            
    #         self.showBuiltImages()

    #     except docker.errors.BuildError as e:
    #         print(f"Error building the image: {e}")
    #     except docker.errors.APIError as e:
    #         print(f"Docker API error: {e}")

    # def showBuiltImages(self):
    #     images = self.client.images.list()

    #     print("\nList of built Docker images:")
    #     for image in images:
    #         tags = ", ".join(image.tags) if image.tags else "<none>"
    #         print(f"Image ID: {image.id}, Tags: {tags}")

    async def check_odooDebian(self):
        for dir_number in range(16, 19):
            dir_path = os.path.join(self.dir, str(dir_number))
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                shutil.rmtree(f"{self.dir}/OdooCloneDir")
                print(f"Removed directory: {dir_path}")
            await downloadOdooDebian.DownloadOdooSetup().downloadOdoo(dir_number, time=250)
            await gitCloneOdoo.OdooDockerClone().cloneOdoo(str(dir_number))
            await AdjustDockerfile.AdjustingDockerFileForEnterprise().formatDockerfile(dir_number)


async def main_loop():
    odoo_image = OdooImage()

    while True:
        await odoo_image.check_odooDebian()
        print("Waiting for 5 minutes before next execution...")
        time.sleep(300)

if __name__ == "__main__":
    asyncio.run(main_loop())