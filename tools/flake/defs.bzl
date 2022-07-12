"""Wrap pytest"""

load("@rules_python//python:defs.bzl", "py_test")
load("@pip//:requirements.bzl", "requirement")

def flake_test(name, srcs, deps = [], args = [], data = [], **kwargs):
    """
        Call pytest
    """
    py_test(
        name = name,
        srcs = [
            "//tools/flake:flake_wrapper.py",
        ] + srcs,
        main = "//tools/flake:flake_wrapper.py",
        args = [
            "--ignore=E501,S104,S605,F541,W503,S404,S607,S603",
        ],
        deps = [],
        data = [],
        **kwargs
    )
