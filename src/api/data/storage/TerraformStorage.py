#  Mahjopi-IaC - API
#  Infrastructure as Code project, automatic machine and network deployment
#  Copyright (c), MahjoPi, 2022.
#  This code belongs exclusively to its authors, use, redistribution or reproduction
#  forbidden except with authorization from the authors.
import os
from jinja2 import Template

from models.TerraformConfig import TerraformConfig


def render_content_templates(config: TerraformConfig):
    """
    Renders the content templates for the given config.

    :param config: the config to render
    :return: None
    """
    templates = ['gcp']
    content = ""
    for template in templates:
        with open(f'./templates/tf/{template}_content.tf.j2', 'r') as f:
            template = Template(f.read(), trim_blocks=True, lstrip_blocks=True)
            rendered_template = template.render(machines=config.machines, networks=config.networks)
            content += rendered_template
    return content


def store_terraform_infra(config: TerraformConfig):
    """
    Stores the machines in the Terraform state file.

    :param config: the config to store
    :return: None
    """
    if not os.path.exists(f'./config/terraform_configs/{config.name}'):
        os.makedirs(f'./config/terraform_configs/{config.name}')
    with open(f'./config/terraform_configs/{config.name}/main.tf', "w") as f:
        # generate jinja template
        locals_template = open('./templates/tf/locals.tf.j2', 'r')
        template = Template(locals_template.read(), trim_blocks=True, lstrip_blocks=True, )
        locals_template.close()
        # render template
        rendered_template = template.render(machines=config.machines, networks=config.networks,
                                            project_id=config.project_id, region=config.region,
                                            ssh_user=config.ssh_user,
                                            private_key_path=f'./config/secrets/{config.private_key_name}')
        # write to file
        f.write(rendered_template + '\n' + render_content_templates(config))
        f.close()
    return True


def get_all_config_names():
    """
    Returns a list of all the terraform configs.

    :return: list of all the terraform configs
    """
    return os.listdir('./config/terraform_configs/')


def delete_terraform_infra(name):
    """
    Deletes the terraform config with the given name.

    :param name: the name of the config to delete
    :return: None
    """
    os.remove(f'./config/terraform_configs/{name}/main.tf')
    os.rmdir(f'./config/terraform_configs/{name}')
