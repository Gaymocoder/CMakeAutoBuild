import json
import os

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

    for key in presets.keys():
        preset = presets[key]
        cmake_preset = {"name": key, **preset["cmake"]}
        cmake_presets["configurePresets"].append(cmake_preset)

        conan_profiles[key] = '[settings]\n'
        for conkey in preset["conan"].keys():
            conval = preset["conan"][conkey]
            conan_profiles[key] += f'{conkey}={conval}\n'

    with open('CMakePresets.json', 'w', encoding = 'utf-8') as f:
        json.dump(cmake_presets, f, indent = 4)

    profile_dir = os.path.join(os.path.abspath('.'), 'conan', 'profiles')
    os.makedirs(profile_dir, exist_ok = True)
    for key in conan_profiles.keys():    
        profile_path = os.path.join(profile_dir, key)
        with open(profile_path, 'w', encoding = 'utf-8') as f:
            f.write(conan_profiles[key])

main()