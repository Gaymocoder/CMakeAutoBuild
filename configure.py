import os
import json
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString as lss

yaml = YAML()

def main():
    with open("presets.json", "r", encoding = "utf-8") as f:
        presets = json.load(f)

    cmake_presets = {
        "version": 3,
        "cmakeMinimumRequired": {
            "major": 3,
            "minor": 25,
            "patch": 0
        },
        "configurePresets": []
    }

    conan_profiles = {}

    with open(os.path.join(".github", "workflows", "ci.yml"), "r", encoding = "utf-8") as f:
        github_ci = yaml.load(f)

    github_ci["jobs"]["build"]["strategy"]["matrix"]["include"] = []
    matrix = github_ci["jobs"]["build"]["strategy"]["matrix"]["include"]
    github_ci["jobs"]["build"]["steps"] = [{"uses":"actions/checkout@v4"}]

    for key in presets.keys():
        preset = presets[key]
        cmake_preset = {"name": key, **preset["cmake"]}
        cmake_presets["configurePresets"].append(cmake_preset)

        conan_profiles[key] = '[settings]\n'
        for conkey in preset["conan"].keys():
            conval = preset["conan"][conkey]
            conan_profiles[key] += f'{conkey}={conval}\n'

        matrix_preset = {"preset": f'{key}'}
        match preset["conan"]["os"]:
            case "Linux":
                matrix_preset["os"] = "ubuntu-latest"
                matrix_preset["build"] = "sh build.sh"
            case "Windows":
                matrix_preset["os"] = "windows-latest"
                matrix_preset["build"] = "build.bat"
        
        for ghkey in preset["github_ci"].keys():
            match ghkey:
                case "uses":
                    for use in preset["github_ci"][ghkey]:
                        use["if"] = f'${{{{ matrix.preset == \'{key}\' }}}}'
                        github_ci["jobs"]["build"]["steps"].append(use)
                case "run-file":
                    for script_name in preset["github_ci"][ghkey]:
                        script_path = os.path.join(".github", "workflows", "scripts", script_name)
                        command = {
                            "if": f'${{{{ matrix.preset == \'{key}\' }}}}',
                            "name": "install",
                        }
                        if os.path.exists(script_path):
                            with open(script_path, 'r', encoding = 'utf-8') as script:
                                command["run"] = lss(script.read())
                        github_ci["jobs"]["build"]["steps"].append(command)
                case "run":
                    github_ci["jobs"]["build"]["steps"].append({"name": "install", "run": preset["github_ci"][ghkey]})
                case _:
                    github_ci["jobs"]["build"]["steps"].append({ghkey: preset["github_ci"][ghkey]})
        matrix.append(matrix_preset)
    github_ci["jobs"]["build"]["steps"].append({"name": "Build", "run": "${{ matrix.build }}"})


    with open('CMakePresets.json', 'w', encoding = 'utf-8') as f:
        json.dump(cmake_presets, f, indent = 4)

    profile_dir = os.path.join(os.path.abspath('.'), 'conan', 'profiles')
    os.makedirs(profile_dir, exist_ok = True)
    for key in conan_profiles.keys():    
        profile_path = os.path.join(profile_dir, key)
        with open(profile_path, 'w', encoding = 'utf-8') as f:
            f.write(conan_profiles[key])

    with open(os.path.join(".github", "workflows", "ci.yml"), "w", encoding = "utf-8") as f:
        yaml.dump(github_ci, f)

main()