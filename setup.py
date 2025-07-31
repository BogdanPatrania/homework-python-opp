from setuptools import setup, find_packages

setup(
    name="math-microservice",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "jinja2",
        "click",
        "pydantic",
        "httpx",
        "pytest",
        "anyio",
        "flake8"
    ],
    entry_points={
        "console_scripts": [
            "mathcli = cli.main:cli"
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
