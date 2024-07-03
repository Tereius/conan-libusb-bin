#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conan import ConanFile
from conan.tools.files import download, copy, unzip, rename, rm
import json, os

required_conan_version = ">=2.0"

class libusbbinConan(ConanFile):

    jsonInfo = json.load(open("info.json", 'r'))
    # ---Package reference---
    name = jsonInfo["projectName"]
    version = jsonInfo["version"]
    user = jsonInfo["domain"]
    channel = "stable"
    # ---Metadata---
    description = jsonInfo["projectDescription"]
    license = jsonInfo["license"]
    author = jsonInfo["vendor"]
    topics = jsonInfo["topics"]
    homepage = jsonInfo["homepage"]
    url = jsonInfo["repository"]
    # ---Requirements---
    requires = []
    tool_requires = ["7zip/[*]@com.github.tereius/stable"]
    # ---Sources---
    exports = ["info.json"]
    exports_sources = []
    # ---Binary model---
    settings = "os", "compiler", "build_type", "arch"
    options = {}
    default_options = {}
    # ---Build---
    generators = []
    # ---Folders---
    no_copy_source = True

    def validate(self):
        valid_os = ["Windows"]
        if str(self.settings.os) not in valid_os:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following operating systems: {valid_os}")
        valid_arch = ["x86_64"]
        if str(self.settings.arch) not in valid_arch:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following architectures on {self.settings.os}: {valid_arch}")
        valid_compiler = ["gcc"]
        if str(self.settings.compiler) not in valid_compiler:
            raise ConanInvalidConfiguration(f"{self.name} {self.version} is only supported for the following compiler on {self.settings.os}: {valid_arch}")

    def build(self):
        download(self, **self.conan_data["sources"][self.version][str(self.settings.os)])
        self.run("7z x -y libusb.7z -o%s" % self.package_folder)

    def package_info(self):
        self.cpp_info.libdirs = ["MinGW64/static"]
