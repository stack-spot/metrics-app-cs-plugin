from templateframework.runner import run
from templateframework.template import Template
from templateframework.metadata import Metadata
import subprocess
import os

class Plugin(Template):
    def post_hook(self, metadata: Metadata):
        project_name = metadata.global_inputs['project_name']

        if 'Prometheus' in metadata.inputs['type']:
            os.chdir(f'{metadata.target_path}/src/{project_name}.Application/')
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Metrics'])
            
            os.chdir(f'{metadata.target_path}/src/{project_name}.Infrastructure/')
            subprocess.run(['dotnet', 'add', 'package', 'StackSpot.Metrics'])            
            
            using = "using StackSpot.Metrics;using Prometheus;"
            service = "services.ConfigureMetrics();"
            app = "app.UseMetricServer();\napp.UseHttpMetrics();"
        
        print('Setting Configuration...')

        os.chdir(f'{metadata.target_path}/src/{project_name}.Application/Common/StackSpot/')

        configuration_file = open(file='DependencyInjection.cs', mode='r')
        content = configuration_file.readlines()
        index = [x for x in range(len(content)) if 'return services' in content[x].lower()]
        index_app = [x for x in range(len(content)) if 'return app' in content[x].lower()]
        index_using = [x for x in range(len(content)) if 'using' in content[x].lower()]

        content[index[0]] = f"{service}\n{content[index[0]]}"
        content[index_app[0]] = f"{app}\n{content[index_app[0]]}"        
        content[index_using[0]] = f"{using}\n{content[index_using[0]]}"

        configuration_file = open(file='DependencyInjection.cs', mode='w')                     
        configuration_file.writelines(content)
        configuration_file.close()

        print('Setting Configuration done.') 

        print('Apply dotnet format...')
        os.chdir(f'{metadata.target_path}/')
        subprocess.run(['dotnet', 'dotnet-format', f'src/{project_name}.Application/{project_name}.Application.csproj', '--include-generated'])    
        print('Apply dotnet format done...')

if __name__ == '__main__':
    run(Plugin())