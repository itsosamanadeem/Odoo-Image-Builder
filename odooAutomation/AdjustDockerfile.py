import os
import re

class AdjustingDockerFileForEnterprise:
    async def formatDockerfile(self, dir):
        dockerDir = f'~/Odoo-Image-Builder/{dir}'

        if os.path.exists(dockerDir) and os.listdir(dockerDir):
            with open(f'{dockerDir}/Dockerfile', 'r', encoding='utf-8') as file:
                data = file.read()

            pattern = re.compile(
                r"""
                ENV\s+ODOO_VERSION\s+{}\.0\s*\n
                ARG\s+ODOO_RELEASE=\d+\s*\n
                ARG\s+ODOO_SHA=\w+\s*\n
                RUN\s+curl\s+-o\s+odoo\.deb\s+-sSL\s+http://nightly\.odoo\.com/\$\{{ODOO_VERSION}}/nightly/deb/odoo_\$\{{ODOO_VERSION}}.\$\{{ODOO_RELEASE}}_all\.deb\s*\\\n
                \s*&&\s+echo\s+"\$\{{ODOO_SHA}}\s+odoo\.deb"\s+\|\s+sha1sum\s+-c\s+-\s*\\\n
                \s*&&\s+apt-get\s+update\s*\\\n
                \s*&&\s+apt-get\s+-y\s+install\s+--no-install-recommends\s+\./odoo\.deb\s*\\\n
                """.format(dir),
                re.VERBOSE
            )

            match = pattern.search(data)
            if match:
                print(f"Pattern found in version {dir}:")
                oldGroup = match.group()
                newGroup = f"""
ENV ODOO_VERSION={dir}.0
COPY ./odoo_{dir}.0+e.latest_all.deb /
RUN apt-get update \\
    && apt-get -y install --no-install-recommends ./odoo_{dir}.0+e.latest_all.deb \\
                """

                updatedData = data.replace(oldGroup, newGroup)

                finalData = updatedData.replace(
                    '&& rm -rf /var/lib/apt/lists/* odoo.deb',
                    f'&& rm -rf /var/lib/apt/lists/* odoo_{dir}.0+e.latest_all.deb'
                )
                with open(f'{dockerDir}/Dockerfile', 'w', encoding='utf-8') as file:
                    file.write(finalData)

                print(f"Dockerfile for version {dir} updated successfully.")
            else:
                print(f"Pattern not found in version {dir}.")
