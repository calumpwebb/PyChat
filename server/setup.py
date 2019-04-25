#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    name="pychat-server",
    author="Calum Webb",
    packages=find_packages(exclude=["tests", "alembic", "build", "dist"]),
)
