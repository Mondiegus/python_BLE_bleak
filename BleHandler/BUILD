load("@rules_python//python:defs.bzl", "py_library")
load("@pip//:requirements.bzl", "requirement")
load("//tools/flake:defs.bzl", "flake_test")

py_library(
    name = "ble_handler",
    srcs = glob(["src/*.py"]),
    imports = ["."],
    visibility = ["//visibility:public"],
    deps = [
        requirement("bleak"),
        ],
)

py_binary(
    name = "ble_handler_bin",
    srcs = ["ble_handler_bin.py"],
    deps = [
        ":ble_handler"
    ],
    imports = ["."]
)

# py_test(
#     name = "test_ble_handler",
#     srcs = glob(["tests/*.py"]),
#     main = "test_ble_handler.py",
#     deps = [
#         ":ble_handler",
#     ],
# )

flake_test(
    name = "test",
    srcs = glob(["src/bleHandler.py",],),
    deps = [
        ":ble_handler",
    ],
)