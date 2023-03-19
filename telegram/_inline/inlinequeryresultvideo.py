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
"""This module contains the classes that represent Telegram InlineQueryResultVideo."""
from typing import TYPE_CHECKING, Optional, Sequence, Tuple

from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._inline.inlinequeryresult import InlineQueryResult
from telegram._messageentity import MessageEntity
from telegram._utils.argumentparsing import parse_sequence_arg
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict, ODVInput
from telegram._utils.warnings_transition import (
    warn_about_deprecated_arg_return_new_arg,
    warn_about_deprecated_attr_in_property,
    warn_about_required_renamed_param_passed_as_kwarg,
)
from telegram.constants import InlineQueryResultType

if TYPE_CHECKING:
    from telegram import InputMessageContent


class InlineQueryResultVideo(InlineQueryResult):
    """
    Represents a link to a page containing an embedded video player or a video file. By default,
    this video file will be sent by the user with an optional caption. Alternatively, you can use
    :attr:`input_message_content` to send a message with the specified content instead of
    the video.

    Note:
        If an InlineQueryResultVideo message contains an embedded video (e.g., YouTube), you must
        replace its content using :attr:`input_message_content`.

    .. seealso:: :wiki:`Working with Files and Media <Working-with-Files-and-Media>`

    Args:
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        video_url (:obj:`str`): A valid URL for the embedded video player or video file.
        mime_type (:obj:`str`): Mime type of the content of video url, "text/html" or "video/mp4".
        thumbnail_url (:obj:`str`, optional): URL of the thumbnail (JPEG only) for the video.

            Warning:
                The Bot API does **not** define this as an optional argument. It is formally
                optional for backwards compatibility with the deprecated :paramref:`thumb_url`.
                If you pass neither :paramref:`thumbnail_url` nor :paramref:`thumb_url`,
                :class:`ValueError` will be raised.

            .. versionadded:: NEXT.VERSION
        title (:obj:`str`, optional): Title for the result.

            Warning:
                The Bot API does **not** define this as an optional argument. It is formally
                optional to ensure backwards compatibility of :paramref:`thumbnail_url` with the
                deprecated :paramref:`thumb_url`, which required that :paramref:`thumbnail_url`
                become optional. :class:`TypeError` will be raised if no ``title`` is passed.
        caption (:obj:`str`, optional): Caption of the video to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters after entities
            parsing.
        parse_mode (:obj:`str`, optional): |parse_mode|
        caption_entities (Sequence[:class:`telegram.MessageEntity`], optional): |caption_entities|

            .. versionchanged:: 20.0
                |sequenceclassargs|

        video_width (:obj:`int`, optional): Video width.
        video_height (:obj:`int`, optional): Video height.
        video_duration (:obj:`int`, optional): Video duration in seconds.
        description (:obj:`str`, optional): Short description of the result.
        reply_markup (:class:`telegram.InlineKeyboardMarkup`, optional): Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional): Content of the
            message to be sent instead of the video. This field is required if
            ``InlineQueryResultVideo`` is used to send an HTML-page as a result
            (e.g., a YouTube video).
        thumb_url (:obj:`str`, optional): URL of the thumbnail (JPEG only) for the video.

            .. deprecated:: NEXT.VERSION
               |thumbargumentdeprecation| :paramref:`thumbnail_url`.

    Raises:
        :class:`ValueError`: If neither :paramref:`thumbnail_url` nor :paramref:`thumb_url` is
            supplied or if both are supplied and are not equal.
        :class:`TypeError`: If no :paramref:`title` is passed.

    Attributes:
        type (:obj:`str`): :tg-const:`telegram.constants.InlineQueryResultType.VIDEO`.
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        video_url (:obj:`str`): A valid URL for the embedded video player or video file.
        mime_type (:obj:`str`): Mime type of the content of video url, "text/html" or "video/mp4".
        thumbnail_url (:obj:`str`): URL of the thumbnail (JPEG only) for the video.

            .. versionadded:: NEXT.VERSION
        title (:obj:`str`): Title for the result.
        caption (:obj:`str`): Optional. Caption of the video to be sent,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters after entities
            parsing.
        parse_mode (:obj:`str`): Optional. |parse_mode|
        caption_entities (Tuple[:class:`telegram.MessageEntity`]): Optional.
            |captionentitiesattr|

            .. versionchanged:: 20.0

                * |tupleclassattrs|
                * |alwaystuple|

        video_width (:obj:`int`): Optional. Video width.
        video_height (:obj:`int`): Optional. Video height.
        video_duration (:obj:`int`): Optional. Video duration in seconds.
        description (:obj:`str`): Optional. Short description of the result.
        reply_markup (:class:`telegram.InlineKeyboardMarkup`): Optional. Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`): Optional. Content of the
            message to be sent instead of the video. This field is required if
            ``InlineQueryResultVideo`` is used to send an HTML-page as a result
            (e.g., a YouTube video).

    """

    __slots__ = (
        "video_url",
        "reply_markup",
        "caption_entities",
        "caption",
        "title",
        "description",
        "video_duration",
        "parse_mode",
        "mime_type",
        "input_message_content",
        "video_height",
        "video_width",
        "thumbnail_url",
    )

    @warn_about_required_renamed_param_passed_as_kwarg(
        deprecated_param_names=("thumb_url",),
        new_param_names=("thumbnail_url",),
        bot_api_version="6.6",
    )
    def __init__(
        self,
        id: str,  # pylint: disable=redefined-builtin
        video_url: str,
        mime_type: str,
        # thumbnail_url and title are not optional in Telegram API, but we want to support
        # thumb_url as well, so thumbnail_url may not be passed if thumb_url is passed.
        # We will raise ValueError manually if neither thumbnail_url nor thumb_url are passed.
        thumbnail_url: str = None,
        # title had to be made optional because of thumbnail_url. This is compensated by raising
        # TypeError manually if title is not passed.
        title: str = None,
        caption: str = None,
        video_width: int = None,
        video_height: int = None,
        video_duration: int = None,
        description: str = None,
        reply_markup: InlineKeyboardMarkup = None,
        input_message_content: "InputMessageContent" = None,
        parse_mode: ODVInput[str] = DEFAULT_NONE,
        caption_entities: Sequence[MessageEntity] = None,
        # thumbnail_url is not optional in Telegram API, but it is here, along with thumb_url.
        # This way the user can pass thumbnail_url as a positional argument and thumb_url
        # as a keyword_argument
        thumb_url: str = None,
        *,
        api_kwargs: JSONDict = None,
    ):
        if not (thumbnail_url or thumb_url):
            raise ValueError(
                "You must pass either 'thumbnail_url' or 'thumb_url'. Note that 'thumb_url' is "
                "deprecated."
            )

        if title is None:
            raise TypeError(
                "InlineQueryResultVideo.__init__() missing a required argument: you forgot to pass"
                " either 'title' or 'thumbnail_url'."
            )

        # Required
        super().__init__(InlineQueryResultType.VIDEO, id, api_kwargs=api_kwargs)
        with self._unfrozen():
            self.video_url: str = video_url
            self.mime_type: str = mime_type
            self.thumbnail_url: str = warn_about_deprecated_arg_return_new_arg(
                deprecated_arg=thumb_url,
                new_arg=thumbnail_url,
                deprecated_arg_name="thumb_url",
                new_arg_name="thumbnail_url",
                bot_api_version="6.6",
            )
            self.title: str = title

            # Optional
            self.caption: Optional[str] = caption
            self.parse_mode: ODVInput[str] = parse_mode
            self.caption_entities: Tuple[MessageEntity, ...] = parse_sequence_arg(caption_entities)
            self.video_width: Optional[int] = video_width
            self.video_height: Optional[int] = video_height
            self.video_duration: Optional[int] = video_duration
            self.description: Optional[str] = description
            self.reply_markup: Optional[InlineKeyboardMarkup] = reply_markup
            self.input_message_content: Optional[InputMessageContent] = input_message_content

    @property
    def thumb_url(self) -> str:
        """:obj:`str`: URL of the thumbnail (JPEG only) for the video.

        .. deprecated:: NEXT.VERSION
           |thumbattributedeprecation| :attr:`thumbnail_url`.
        """
        warn_about_deprecated_attr_in_property(
            deprecated_attr_name="thumb_url",
            new_attr_name="thumbnail_url",
            bot_api_version="6.6",
        )
        return self.thumbnail_url
