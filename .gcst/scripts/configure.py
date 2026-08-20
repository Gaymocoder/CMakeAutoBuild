import json
import os, shutil

from pathlib import Path
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString as lss

yaml = YAML()

HERE = Path(__file__).resolve().parent
GCST_DIR = HERE.parent
ROOT = GCST_DIR.parent

CONAN_PROFILES = {}
CMAKE_PRESETS = {
    "version": 3,
    "cmakeMinimumRequired": {
        "major": 3,
        "minor": 25,
        "patch": 0
    },
    "configurePresets": []
}

def run_from_file(script_name):
    script_path = os.path.join(ROOT, ".github", "workflows", "scripts", script_name)
    if os.path.exists(script_path):
        with open(script_path, 'r', encoding = 'utf-8') as script:
            return script.read() + "\n\n"
    print("No script with name '{script_name}' was found in '.github/workflows/scripts/'")
    return ''


def cmake_preset_process(key, preset, out_presets):
    cmake_preset = {"name": key, **preset["cmake"]}
    out_presets["configurePresets"].append(cmake_preset)

    
def conan_preset_process(key, preset, out_profiles):
    out_profiles[key] = '[settings]\n'
    for conkey in preset["conan"]:
        conval = preset["conan"][conkey]
        out_profiles[key] += f'{conkey}={conval}\n'


def githubci_preset_process(key, preset, out_steps, out_matrix):
    matrix_preset = {"preset": f'{key}'}
    match preset["conan"]["os"]:
        case "Linux":
            matrix_preset["os"] = "ubuntu-latest"
            matrix_preset["build"] = "sh build.sh"

        case "Windows":
            matrix_preset["os"] = "windows-latest"
            matrix_preset["build"] = "./build.bat"

    preset_steps = []
    for step in preset["github_ci"]:
        step["if"] = f'${{{{ matrix.preset == \'{key}\' }}}}'
        if "run-files" not in step:
            preset_steps.append(step)
            continue

        step["run"] = ''
        for script in step["run-files"]:
            step["run"] += run_from_file(script)
        step["run"] = lss(step["run"])
        del step["run-files"]
        preset_steps.append(step)

    out_matrix.append(matrix_preset)
    out_steps.extend(preset_steps)


def presets_extract(presets, cmake_out, conan_out, out_ghci_steps, out_ghci_matrix):
    for key in presets:
        if key in [".common-pre", ".common-post"]:
            continue
        preset = presets[key]
        cmake_preset_process(key, preset, cmake_out)
        conan_preset_process(key, preset, conan_out)
        githubci_preset_process(key, preset, out_ghci_steps, out_ghci_matrix)


def presets_write(cmake_presets, conan_profiles, github_ci):
    with open(os.path.join(ROOT, 'CMakePresets.json'), 'w', encoding = 'utf-8') as f:
        json.dump(cmake_presets, f, indent = 4)

    profile_dir = os.path.join(ROOT, 'conan', 'profiles')
    shutil.rmtree(profile_dir, ignore_errors = True)
    os.makedirs(profile_dir, exist_ok = True)
    for key in conan_profiles:    
        profile_path = os.path.join(profile_dir, key)
        with open(profile_path, 'w', encoding = 'utf-8') as f:
            f.write(conan_profiles[key])

    with open(os.path.join(ROOT, ".github", "workflows", "ci.yml"), "w", encoding = "utf-8") as f:
        yaml.dump(github_ci, f)


def main():
    with open(os.path.join(GCST_DIR, "presets.json"), "r", encoding = "utf-8") as f:
        presets = json.load(f)
    with open(os.path.join(ROOT, ".github", "workflows", "ci.yml"), "r", encoding = "utf-8") as f:
        github_ci = yaml.load(f)

    github_ci["jobs"]["build"]["strategy"]["matrix"]["include"] = []
    matrix = github_ci["jobs"]["build"]["strategy"]["matrix"]["include"]
    steps = github_ci["jobs"]["build"]["steps"] = presets[".common-pre"]

    presets_extract(presets, CMAKE_PRESETS, CONAN_PROFILES, steps, matrix)
    steps.append({"name": "Build", "run": "${{ matrix.build }} ${{ matrix.preset }}"})
    steps.extend(presets[".common-post"])

    presets_write(CMAKE_PRESETS, CONAN_PROFILES, github_ci)

if __name__ == '__main__':
    main()