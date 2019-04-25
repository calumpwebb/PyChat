#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

import settings

setup(
    name="pychat-client",
    author="Calum Webb",
    packages=find_packages(exclude=["tests", "alembic", "build", "dist"]),
)
