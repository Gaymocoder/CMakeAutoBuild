from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps

class gcsabConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    
    def requirements(self):
        self.requires("boost/1.87.0")

    def generate(self):
        CMakeToolchain(self).generate()
        CMakeDeps(self).generate()