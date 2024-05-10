#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2024
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
"""This module contains objects related to chat backgrounds."""
from typing import TYPE_CHECKING, Dict, Final, Optional, Sequence, Type

from telegram import constants
from telegram._files.document import Document
from telegram._telegramobject import TelegramObject
from telegram._utils import enum
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.types import JSONDict

if TYPE_CHECKING:
    from telegram import Bot


class BackgroundFill(TelegramObject):
    """Base class for Telegram BackgroundFill Objects. It can be one of:

    * :class:`telegram.BackgroundFillSolid`
    * :class:`telegram.BackgroundFillGradient`
    * :class:`telegram.BackgroundFillFreeformGradient`

    .. versionadded:: NEXT.VERSION

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`type` is equal.

    Args:
        type (:obj:`str`): Type of the background fill. Can be one of:
          :attr:`~telegram.BackgroundFill.SOLID`, :attr:`~telegram.BackgroundFill.GRADIENT`
          or :attr:`~telegram.BackgroundFill.FREEFORM_GRADIENT`.

    Attributes:
        type (:obj:`str`): Type of the background fill. Can be one of:
          :attr:`~telegram.BackgroundFill.SOLID`, :attr:`~telegram.BackgroundFill.GRADIENT`
          or :attr:`~telegram.BackgroundFill.FREEFORM_GRADIENT`.

    """

    __slots__ = ("type",)

    SOLID: Final[constants.BackgroundFill] = constants.BackgroundFill.SOLID
    """:const:`telegram.constants.BackgroundFill.SOLID`"""
    GRADIENT: Final[constants.BackgroundFill] = constants.BackgroundFill.GRADIENT
    """:const:`telegram.constants.BackgroundFill.GRADIENT`"""
    FREEFORM_GRADIENT: Final[constants.BackgroundFill] = constants.BackgroundFill.FREEFORM_GRADIENT
    """:const:`telegram.constants.BackgroundFill.FREEFORM_GRADIENT`"""

    def __init__(
        self,
        type: str,  # pylint: disable=redefined-builtin
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        # Required by all subclasses
        self.type: str = enum.get_member(constants.BackgroundFill, type, type)

        self._id_attrs = (self.type,)
        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["BackgroundFill"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        _class_mapping: Dict[str, Type[BackgroundFill]] = {
            cls.SOLID: BackgroundFillSolid,
            cls.GRADIENT: BackgroundFillGradient,
            cls.FREEFORM_GRADIENT: BackgroundFillFreeformGradient,
        }

        if cls is BackgroundFill and data.get("type") in _class_mapping:
            return _class_mapping[data.pop("type")].de_json(data=data, bot=bot)

        return super().de_json(data=data, bot=bot)


class BackgroundFillSolid(BackgroundFill):
    """
    The background is filled using the selected color.

    .. versionadded:: NEXT.VERSION

    Args:
        color (:obj:`int`): The color of the background fill in the `RGB24` format.

    Attributes:
        type (:obj:`str`): Type of the background fill. Always
            :attr:`~telegram.BackgroundFill.SOLID`.
        color (:obj:`int`): The color of the background fill in the `RGB24` format.
    """

    __slots__ = ("color",)

    def __init__(
        self,
        color: int,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=self.SOLID, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.color: int = color


class BackgroundFillGradient(BackgroundFill):
    """
    The background is a gradient fill.

    .. versionadded:: NEXT.VERSION

    Args:
        top_color (:obj:`int`): Top color of the gradient in the `RGB24` format.
        bottom_color (:obj:`int`): Bottom color of the gradient in the `RGB24` format.
        rotation_angle (:obj:`int`): Clockwise rotation angle of the background
          fill in degrees; `0-359`.

    Attributes:
        type (:obj:`str`): Type of the background fill. Always
            :attr:`~telegram.BackgroundFill.GRADIENT`.
        top_color (:obj:`int`): Top color of the gradient in the `RGB24` format.
        bottom_color (:obj:`int`): Bottom color of the gradient in the `RGB24` format.
        rotation_angle (:obj:`int`): Clockwise rotation angle of the background
          fill in degrees; `0-359`.
    """

    __slots__ = ("bottom_color", "rotation_angle", "top_color")

    def __init__(
        self,
        top_color: int,
        bottom_color: int,
        rotation_angle: int,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=self.GRADIENT, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.top_color: int = top_color
            self.bottom_color: int = bottom_color
            self.rotation_angle: int = rotation_angle


class BackgroundFillFreeformGradient(BackgroundFill):
    """
    The background is a freeform gradient that rotates after every message in the chat.

    .. versionadded:: NEXT.VERSION

    Args:
        colors (Sequence[:obj:`int`]): A list of the 3 or 4 base colors that are used to
          generate the freeform gradient in the `RGB24` format

    Attributes:
        type (:obj:`str`): Type of the background fill. Always
          :attr:`~telegram.BackgroundFill.FREEFORM_GRADIENT`.
        colors (Sequence[:obj:`int`]): A list of the 3 or 4 base colors that are used to
          generate the freeform gradient in the `RGB24` format
    """

    __slots__ = ("colors",)

    def __init__(
        self,
        colors: Sequence[int],
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=self.FREEFORM_GRADIENT, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.colors: Sequence[int] = parse_sequence_arg(colors)


class BackgroundType(TelegramObject):
    """Base class for Telegram BackgroundType Objects. It can be one of:

    * :class:`telegram.BackgroundTypeFill`
    * :class:`telegram.BackgroundTypeWallpaper`
    * :class:`telegram.BackgroundTypePattern`
    * :class:`telegram.BackgroundTypeChatTheme`.

    .. versionadded:: NEXT.VERSION

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`type` is equal.

    Args:
        type (:obj:`str`): Type of the background. Can be one of:
          :attr:`~telegram.BackgroundType.FILL`, :attr:`~telegram.BackgroundType.WALLPAPER`
          :attr:`~telegram.BackgroundType.PATTERN` or
          :attr:`~telegram.BackgroundType.CHAT_THEME`.

    Attributes:
        type (:obj:`str`): Type of the background. Can be one of:
          :attr:`~telegram.BackgroundType.FILL`, :attr:`~telegram.BackgroundType.WALLPAPER`
          :attr:`~telegram.BackgroundType.PATTERN` or
          :attr:`~telegram.BackgroundType.CHAT_THEME`.

    """

    __slots__ = ("type",)

    FILL: Final[constants.BackgroundType] = constants.BackgroundType.FILL
    """:const:`telegram.constants.BackgroundType.FILL`"""
    WALLPAPER: Final[constants.BackgroundType] = constants.BackgroundType.WALLPAPER
    """:const:`telegram.constants.BackgroundType.WALLPAPER`"""
    PATTERN: Final[constants.BackgroundType] = constants.BackgroundType.PATTERN
    """:const:`telegram.constants.BackgroundType.PATTERN`"""
    CHAT_THEME: Final[constants.BackgroundType] = constants.BackgroundType.CHAT_THEME
    """:const:`telegram.constants.BackgroundType.CHAT_THEME`"""

    def __init__(
        self,
        type: str,  # pylint: disable=redefined-builtin
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        # Required by all subclasses
        self.type: str = enum.get_member(constants.BackgroundType, type, type)

        self._id_attrs = (self.type,)
        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["BackgroundType"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        _class_mapping: Dict[str, Type[BackgroundType]] = {
            cls.FILL: BackgroundTypeFill,
            cls.WALLPAPER: BackgroundTypeWallpaper,
            cls.PATTERN: BackgroundTypePattern,
            cls.CHAT_THEME: BackgroundTypeChatTheme,
        }

        if cls is BackgroundType and data.get("type") in _class_mapping:
            return _class_mapping[data.pop("type")].de_json(data=data, bot=bot)

        if "fill" in data:
            data["fill"] = BackgroundFill.de_json(data.get("fill"), bot)

        if "document" in data:
            data["document"] = Document.de_json(data.get("document"), bot)

        return super().de_json(data=data, bot=bot)


class BackgroundTypeFill(BackgroundType):
    """
    The background is automatically filled based on the selected colors.

    .. versionadded:: NEXT.VERSION

    Args:
        fill (:obj:`telegram.BackgroundFill`): The background fill.
        dark_theme_dimming (:obj:`int`): Dimming of the background in dark themes, as a
          percentage; `0-100`.

    Attributes:
        type (:obj:`str`): Type of the background. Always
          :attr:`~telegram.BackgroundType.FILL`.
        fill (:obj:`telegram.BackgroundFill`): The background fill.
        dark_theme_dimming (:obj:`int`): Dimming of the background in dark themes, as a
          percentage; `0-100`.
    """

    __slots__ = ("dark_theme_dimming", "fill")

    def __init__(
        self,
        fill: BackgroundFill,
        dark_theme_dimming: int,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=self.FILL, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.fill: BackgroundFill = fill
            self.dark_theme_dimming: int = dark_theme_dimming


class BackgroundTypeWallpaper(BackgroundType):
    """
    The background is a wallpaper in the `JPEG` format.

    .. versionadded:: NEXT.VERSION

    Args:
        document (:obj:`telegram.Document`): Document with the wallpaper
        dark_theme_dimming (:obj:`int`): Dimming of the background in dark themes, as a
          percentage; `0-100`
        is_blurred (:obj:`bool`, optional): :obj:`True`, if the wallpaper is downscaled to fit
          in a `450x450` square and then box-blurred with radius `12`
        is_moving (:obj:`bool`, optional): :obj:`True`, if the background moves slightly
          when the device is tilted

    Attributes:
        type (:obj:`str`): Type of the background. Always
          :attr:`~telegram.BackgroundType.WALLPAPER`.
        document (:obj:`telegram.Document`): Document with the wallpaper
        dark_theme_dimming (:obj:`int`): Dimming of the background in dark themes, as a
          percentage; `0-100`
        is_blurred (:obj:`bool`): Optional. :obj:`True`, if the wallpaper is downscaled to fit
          in a `450x450` square and then box-blurred with radius `12`
        is_moving (:obj:`bool`): Optional. :obj:`True`, if the background moves slightly
          when the device is tilted
    """

    __slots__ = ("dark_theme_dimming", "document", "is_blurred", "is_moving")

    def __init__(
        self,
        document: Document,
        dark_theme_dimming: int,
        is_blurred: Optional[bool] = None,
        is_moving: Optional[bool] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=self.WALLPAPER, api_kwargs=api_kwargs)

        with self._unfrozen():
            # Required
            self.document: Document = document
            self.dark_theme_dimming: int = dark_theme_dimming
            # Optionals
            self.is_blurred: Optional[bool] = is_blurred
            self.is_moving: Optional[bool] = is_moving


class BackgroundTypePattern(BackgroundType):
    """
    The background is a `PNG` or `TGV` (gzipped subset of `SVG` with `MIME` type
    `"application/x-tgwallpattern"`) pattern to be combined with the background fill
    chosen by the user.

    .. versionadded:: NEXT.VERSION

    Args:
        document (:obj:`telegram.Document`): Document with the pattern.
        fill (:obj:`telegram.BackgroundFill`): The background fill that is combined with
          the pattern.
        intensity (:obj:`int`): Intensity of the pattern when it is shown above the filled
          background; `0-100`.
        is_inverted (:obj:`int`, optional): :obj:`True`, if the background fill must be applied
          only to the pattern itself. All other pixels are black in this case. For dark
          themes only.
        is_moving (:obj:`bool`, optional): :obj:`True`, if the background moves slightly
          when the device is tilted.

    Attributes:
        type (:obj:`str`): Type of the background. Always
          :attr:`~telegram.BackgroundType.PATTERN`.
        document (:obj:`telegram.Document`): Document with the pattern.
        fill (:obj:`telegram.BackgroundFill`): The background fill that is combined with
          the pattern.
        intensity (:obj:`int`): Intensity of the pattern when it is shown above the filled
          background; `0-100`.
        is_inverted (:obj:`int`): Optional. :obj:`True`, if the background fill must be applied
          only to the pattern itself. All other pixels are black in this case. For dark
          themes only.
        is_moving (:obj:`bool`): Optional. :obj:`True`, if the background moves slightly
          when the device is tilted.
    """

    __slots__ = (
        "document",
        "fill",
        "intensity",
        "is_inverted",
        "is_moving",
    )

    def __init__(
        self,
        document: Document,
        fill: BackgroundFill,
        intensity: int,
        is_inverted: Optional[bool] = None,
        is_moving: Optional[bool] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=self.PATTERN, api_kwargs=api_kwargs)

        with self._unfrozen():
            # Required
            self.document: Document = document
            self.fill: BackgroundFill = fill
            self.intensity: int = intensity
            # Optionals
            self.is_inverted: Optional[bool] = is_inverted
            self.is_moving: Optional[bool] = is_moving


class BackgroundTypeChatTheme(BackgroundType):
    """
    The background is taken directly from a built-in chat theme.

    .. versionadded:: NEXT.VERSION

    Args:
        theme_name (:obj:`str`): Name of the chat theme, which is usually an emoji.

    Attributes:
        type (:obj:`str`): Type of the background. Always
          :attr:`~telegram.BackgroundType.CHAT_THEME`.
        theme_name (:obj:`str`): Name of the chat theme, which is usually an emoji.
    """

    __slots__ = ("theme_name",)

    def __init__(
        self,
        theme_name: str,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(type=self.CHAT_THEME, api_kwargs=api_kwargs)

        with self._unfrozen():
            self.theme_name: str = theme_name


class ChatBackground(TelegramObject):
    """
    This object represents a chat background.

    Objects of this class are comparable in terms of equality. Two objects of this class are
    considered equal, if their :attr:`type` is  equal.

    .. versionadded:: NEXT.VERSION

    Args:
        type (:obj:`telegram.BackgroundType`): Type of the background.

    Attributes:
        type (:obj:`telegram.BackgroundType`): Type of the background.
    """

    __slots__ = ("type",)

    def __init__(
        self,
        type: BackgroundType,  # pylint: disable=redefined-builtin
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        super().__init__(api_kwargs=api_kwargs)
        self.type: BackgroundType = type

        self._id_attrs = (self.type,)
        self._freeze()

    @classmethod
    def de_json(cls, data: Optional[JSONDict], bot: "Bot") -> Optional["ChatBackground"]:
        """See :meth:`telegram.TelegramObject.de_json`."""
        data = cls._parse_data(data)

        if not data:
            return None

        data["type"] = BackgroundType.de_json(data.get("type"), bot)

        return super().de_json(data=data, bot=bot)