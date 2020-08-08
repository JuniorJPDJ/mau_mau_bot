#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""Defines helper functions to build the inline result list"""

from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker

import card as c
from utils import display_color, display_color_group, display_name
from internationalization import _, __


def add_choose_color(results, game, anti_cheat):
    """Add choose color options"""
    for color in c.COLORS:
        results.append(
            InlineQueryResultArticle(
                id=f"{color}:{anti_cheat}",
                title=_("Choose Color"),
                description=display_color(color),
                input_message_content=
                InputTextMessageContent(display_color_group(color, game))
            )
        )


def add_other_cards(player, results, game, anti_cheat):
    """Add hand cards when choosing colors"""

    results.append(
        InlineQueryResultArticle(
            f"hand:{anti_cheat}",
            title=_("Card (tap for game state):",
                    "Cards (tap for game state):",
                    len(player.cards)),
            description=', '.join([repr(card) for card in player.cards]),
            input_message_content=game_info(game)
        )
    )


def player_list(game):
    """Generate list of player strings"""
    return [_("{name} ({number} card)",
              "{name} ({number} cards)",
              len(player.cards))
            .format(name=player.user.first_name, number=len(player.cards))
            for player in game.players]


def add_no_game(results):
    """Add text result if user is not playing"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("You are not playing"),
            input_message_content=
            InputTextMessageContent(_('Not playing right now. Use /new to '
                                      'start a game or /join to join the '
                                      'current game in this group'))
        )
    )


def add_not_started(results, anti_cheat):
    """Add text result if the game has not yet started"""
    results.append(
        InlineQueryResultArticle(
            f"nogame:{anti_cheat}",
            title=_("The game wasn't started yet"),
            input_message_content=
            InputTextMessageContent(_('Start the game with /start'))
        )
    )


def add_mode_classic(results, anti_cheat):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            f"mode_classic:{anti_cheat}",
            title=_("🎻 Classic mode"),
            input_message_content=
            InputTextMessageContent(_('Classic 🎻'))
        )
    )


def add_mode_fast(results, anti_cheat):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            f"mode_fast:{anti_cheat}",
            title=_("🚀 Sanic mode"),
            input_message_content=
            InputTextMessageContent(_('Gotta go fast! 🚀'))
        )
    )


def add_mode_wild(results, anti_cheat):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            f"mode_wild:{anti_cheat}",
            title=_("🐉 Wild mode"),
            input_message_content=
            InputTextMessageContent(_('Into the Wild~ 🐉'))
        )
    )


def add_mode_text(results, anti_cheat):
    """Change mode to text"""
    results.append(
        InlineQueryResultArticle(
            f"mode_text:{anti_cheat}",
            title=_("✍️ Text mode"),
            input_message_content=
            InputTextMessageContent(_('Text ✍️'))
        )
    )


def add_mode_waffle(results, anti_cheat):
    """Change mode to waffle"""
    results.append(
        InlineQueryResultArticle(
            f"mode_waffle:{anti_cheat}",
            title=_("🧇 Waffle mode"),
            input_message_content=
            InputTextMessageContent(_('Waffle kurwa 🧇'))
        )
    )


def add_draw(player, results, anti_cheat):
    """Add option to draw"""
    n = player.game.draw_counter or 1

    results.append(
        Sticker(
            f"draw:{anti_cheat}", sticker_file_id=c.STICKERS['option_draw'],
            input_message_content=
            InputTextMessageContent(__('Drawing {number} card',
                                       'Drawing {number} cards', n,
                                       multi=player.game.translate)
                                    .format(number=n))
        )
    )


def add_gameinfo(game, results, anti_cheat):
    """Add option to show game info"""

    results.append(
        Sticker(
            f"gameinfo:{anti_cheat}",
            sticker_file_id=c.STICKERS['option_info'],
            input_message_content=game_info(game)
        )
    )


def add_pass(results, game, anti_cheat):
    """Add option to pass"""
    results.append(
        Sticker(
            f"pass:{anti_cheat}", sticker_file_id=c.STICKERS['option_pass'],
            input_message_content=InputTextMessageContent(
                __('Pass', multi=game.translate)
            )
        )
    )


def add_call_bluff(results, game, anti_cheat):
    """Add option to call a bluff"""
    results.append(
        Sticker(
            f"call_bluff:{anti_cheat}",
            sticker_file_id=c.STICKERS['option_bluff'],
            input_message_content=
            InputTextMessageContent(__("I'm calling your bluff!",
                                       multi=game.translate))
        )
    )


def add_card(game, card, results, can_play, anti_cheat):
    """Add an option that represents a card"""

    if can_play:
        if game.mode != "text":
            results.append(
                Sticker(f"{card}:{anti_cheat}", sticker_file_id=c.STICKERS[str(card)])
        )
        if game.mode == "text":
            results.append(
                Sticker(f"{card}:{anti_cheat}", sticker_file_id=c.STICKERS[str(card)], input_message_content=InputTextMessageContent("Card Played: {card}".format(card=repr(card).replace('Draw Four', '+4').replace('Draw', '+2').replace('Colorchooser', 'Color Chooser')))
        ))
    else:
        results.append(
            Sticker(f"{uuid4()}:{anti_cheat}", sticker_file_id=c.STICKERS_GREY[str(card)],
                    input_message_content=game_info(game))
        )


def game_info(game):
    players = player_list(game)
    return InputTextMessageContent(
        _("Current player: {name}")
        .format(name=display_name(game.current_player.user)) +
        "\n" +
        _("Last card: {card}").format(card=repr(game.last_card)) +
        "\n" +
        _("Player: {player_list}",
          "Players: {player_list}",
          len(players))
        .format(player_list=" -> ".join(players))
    )
