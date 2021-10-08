#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2021
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
"""Common base class for media objects with thumbnails"""
from __future__ import annotations
from typing import TYPE_CHECKING, Any, TypeVar, Optional, Type

from telegram import PhotoSize
from telegram.files.basemedium import _BaseMedium
from telegram.utils.defaultvalue import DEFAULT_NONE
from telegram.utils.types import JSONDict, ODVInput

if TYPE_CHECKING:
    from telegram import Bot, File

ThumbedMT = TypeVar('ThumbedMT', bound='_BaseThumbedMedium', covariant=True)


class _BaseThumbedMedium(_BaseMedium):
    """Base class for objects representing the various media file types that may include a
        thumbnail.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`file_unique_id` is equal.

    .. versionadded:: 14.0

    Args:
        file_id (:obj:`str`): Identifier for this file, which can be used to download
            or reuse the file.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_name (:obj:`str`, optional): Original animation filename as defined by sender.
        file_size (:obj:`int`, optional): File size.
        thumb (:class:`telegram.PhotoSize`, optional): Animation thumbnail as defined by sender.
        bot (:class:`telegram.Bot`, optional): The Bot to use for instance methods.
        **kwargs (:obj:`dict`): Arbitrary keyword arguments.

    Attributes:
        file_id (:obj:`str`): File identifier.
        file_unique_id (:obj:`str`): Unique identifier for this file, which
            is supposed to be the same over time and for different bots.
            Can't be used to download or reuse the file.
        file_name (:obj:`str`): Optional. Original animation filename as defined by sender.
        file_size (:obj:`int`): Optional. File size.
        thumb (:class:`telegram.PhotoSize`): Optional. Animation thumbnail as defined by sender.
        bot (:class:`telegram.Bot`): Optional. The Bot to use for instance methods.

    """

    __slots__ = ('thumb', )

    def __init__(
        self,
        file_id: str,
        file_unique_id: str,
        file_size: int = None,
        thumb: PhotoSize = None,
        bot: Bot = None,
        **_kwargs: Any,
    ):
        super().__init__(file_id, file_unique_id, file_size, bot)
        self.thumb = thumb

    @classmethod
    def de_json(cls: Type[ThumbedMT], data: Optional[JSONDict], bot: Bot) -> Optional[ThumbedMT]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data['thumb'] = PhotoSize.de_json(data.get('thumb'), bot)

        return cls(bot=bot, **data)

    def get_file(
        self, timeout: ODVInput[float] = DEFAULT_NONE, api_kwargs: JSONDict = None
    ) -> File:
        """Convenience wrapper over :attr:`telegram.Bot.get_file`

        For the documentation of the arguments, please see :meth:`telegram.Bot.get_file`.

        Returns:
            :class:`telegram.File`

        Raises:
            :class:`telegram.error.TelegramError`

        """
        return self.bot.get_file(file_id=self.file_id, timeout=timeout, api_kwargs=api_kwargs)
