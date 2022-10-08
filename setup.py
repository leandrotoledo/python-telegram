#!/usr/bin/env python
"""The setup and build script for the python-telegram-bot library."""
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from pkg_resources import DistributionNotFound, get_distribution
from setuptools import find_packages, setup


def get_requirements(raw=False):
    """Build the requirements list for this project"""
    requirements_list = []

    with Path("requirements.txt").open() as reqs:
        for install in reqs:
            if install.startswith("# only telegram.ext:"):
                if raw:
                    break
                continue
            requirements_list.append(install.strip())

    return requirements_list


def get_packages_requirements(raw=False):
    """Build the package & requirements list for this project"""
    reqs = get_requirements(raw=raw)

    exclude = ["tests*"]
    if raw:
        exclude.append("telegram.ext*")

    packs = find_packages(exclude=exclude)

    return packs, reqs


def get_optional_requirements(raw=False):
    """Build the optional dependencies"""
    requirements = defaultdict(list)

    with Path("requirements-opts.txt").open() as reqs:
        for line in reqs:
            if line.startswith("#"):
                continue
            dependency, names = line.split("#")
            dependency = dependency.strip()
            for name in names.split(","):
                name = name.strip()
                if name.endswith("!ext"):
                    if raw:
                        continue
                    else:
                        name = name[:-4]
                requirements[name].append(dependency)

    return requirements


def get_setup_kwargs(raw=False):
    """Builds a dictionary of kwargs for the setup function"""
    packages, requirements = get_packages_requirements(raw=raw)

    raw_ext = "-raw" if raw else ""
    readme = Path(f'README{"_RAW" if raw else ""}.rst')

    version_file = Path("telegram/_version.py").read_text()
    first_part = version_file.split("# SETUP.PY MARKER")[0]
    exec(first_part)

    kwargs = dict(
        script_name=f"setup{raw_ext}.py",
        name=f"python-telegram-bot{raw_ext}",
        version=locals()["__version__"],
        author="Leandro Toledo",
        author_email="devs@python-telegram-bot.org",
        license="LGPLv3",
        url="https://python-telegram-bot.org/",
        # Keywords supported by PyPI can be found at https://github.com/pypa/warehouse/blob/aafc5185e57e67d43487ce4faa95913dd4573e14/warehouse/templates/packaging/detail.html#L20-L58
        project_urls={
            "Documentation": "https://docs.python-telegram-bot.org",
            "Bug Tracker": "https://github.com/python-telegram-bot/python-telegram-bot/issues",
            "Source Code": "https://github.com/python-telegram-bot/python-telegram-bot",
            "News": "https://t.me/pythontelegrambotchannel",
            "Changelog": "https://docs.python-telegram-bot.org/en/stable/changelog.html",
        },
        download_url=f"https://pypi.org/project/python-telegram-bot{raw_ext}/",
        keywords="python telegram bot api wrapper",
        description="We have made you a wrapper you can't refuse",
        long_description=readme.read_text(),
        long_description_content_type="text/x-rst",
        packages=packages,
        install_requires=requirements,
        extras_require=get_optional_requirements(raw=raw),
        include_package_data=True,
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Communications :: Chat",
            "Topic :: Internet",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        python_requires=">=3.7",
    )

    return kwargs


def avoid_common_setup_errors(raw=False):
    # This runs before the setup, trying to catch common setup errors

    # check if ptb package exists
    # import telegram (DOUBLE CHECK with telegram.py or telegram folder)
    # if yes, check if ModuleNotFoundError == httpx
    try:
        get_distribution("telegram")
        print(
            """
            =============================DEBUG ASSISTANCE==========================
            You can not use python-telegram-bot and telegram. Please run 
            pip uninstall telegram and try again.
            =============================DEBUG ASSISTANCE==========================
            """
        )
        raise Exception("BuildError")
    except DistributionNotFound:
        pass
    try:
        get_distribution(f'python-telegram-bot{"" if raw else "-raw"}')
        print(
            f"""
            =============================DEBUG ASSISTANCE==========================
            You can not use python-telegram-bot and python-telegram-bot-raw. Please 
            run pip uninstall python-telegram-bot{"" if raw else "-raw"} and try again.
            =============================DEBUG ASSISTANCE==========================
            """
        )
        raise Exception("BuildError")
    except DistributionNotFound:
        pass
    try:
        # if the telegram import works here, something locally overrides telegram
        import telegram

        print(
            """
            =============================DEBUG ASSISTANCE==========================
            The python-telegram-bot library uses the telegram namespace. You 
            probably have a local file or folder called telegram. Please rename it
            and try again.
            =============================DEBUG ASSISTANCE==========================
            """
        )
    except ModuleNotFoundError:
        pass


def main():
    # If we're building, build ptb-raw as well
    if set(sys.argv[1:]) in [{"bdist_wheel"}, {"sdist"}, {"sdist", "bdist_wheel"}]:
        args = ["python", "setup-raw.py"]
        args.extend(sys.argv[1:])
        subprocess.run(args, check=True, capture_output=True)

    avoid_common_setup_errors(raw=False)
    setup(**get_setup_kwargs(raw=False))


if __name__ == "__main__":
    main()
