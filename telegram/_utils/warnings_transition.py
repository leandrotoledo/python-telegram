#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2023
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains classes used for transition warnings issued by this library.

It was created to prevent circular imports that would be caused by creating the warnings
inside warnings.py.

.. versionadded:: NEXT.VERSION
"""
import functools
from typing import Any

from telegram._utils.warnings import warn
from telegram.warnings import PTBDeprecationWarning


# Narrower type hints will cause linting errors and/or circular imports.
# We'll use `Any` here and put type hints in the calling code.
def warn_about_deprecated_arg_return_new_arg(
    deprecated_arg: Any,
    new_arg: Any,
    deprecated_arg_name: str,
    new_arg_name: str,
    bot_api_version: str,
) -> Any:
    """A helper function for the transition in API when argument is renamed.

    Checks the `deprecated_arg` and `new_arg` objects; warns if non-None `deprecated_arg` object
    was passed. Returns `new_arg` object (either the one originally passed by the user or the one
    that user passed as `deprecated_arg`).

    Raises `ValueError` if both `deprecated_arg` and `new_arg` objects were passed, and they are
    different.
    """
    if deprecated_arg and new_arg and deprecated_arg != new_arg:
        raise ValueError(
            f"You passed different entities as '{deprecated_arg_name}' and '{new_arg_name}'. "
            f"The parameter '{deprecated_arg_name}' was renamed to '{new_arg_name}' in Bot API "
            f"{bot_api_version}. We recommend using '{new_arg_name}' instead of "
            f"'{deprecated_arg_name}'."
        )

    if deprecated_arg:
        warn(
            f"Bot API {bot_api_version} renamed the argument '{deprecated_arg}' to '{new_arg}'.",
            PTBDeprecationWarning,
            stacklevel=2,
        )
        return deprecated_arg

    return new_arg


warn_about_thumb_return_thumbnail = functools.partial(
    warn_about_deprecated_arg_return_new_arg,
    deprecated_arg_name="thumb",
    new_arg_name="thumbnail",
    bot_api_version="6.6",
)
"""A helper function to warn about using a deprecated 'thumb' argument and return it or the new
'thumbnail' argument, introduced in API 6.6.
"""
