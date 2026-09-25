"""Telegram navigation engine for the academic resources bot."""

from __future__ import annotations

import logging
import os
from typing import Any
from dotenv import load_dotenv

load_dotenv()

import keep_alive
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

from resources_data import ACADEMIC_DATA, CATEGORY_LABELS

LOGGER = logging.getLogger(__name__)
TOKEN_ENV = "TELEGRAM_BOT_TOKEN"
MAX_CALLBACK_BYTES = 64
MI_INACTIVE_MESSAGE = "MI was newly opened; only 1st Year is currently active."



def _callback(*parts: str) -> str:
    value = ":".join(parts)
    if len(value.encode("utf-8")) > MAX_CALLBACK_BYTES:
        raise ValueError(f"callback_data exceeds Telegram's 64-byte limit: {value}")
    return value


def _button(label: str, callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(label, callback_data=callback_data)


def _rows(buttons: list[InlineKeyboardButton], columns: int = 1) -> list[list[InlineKeyboardButton]]:
    return [buttons[index : index + columns] for index in range(0, len(buttons), columns)]


def _branch_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        _button("MI · Mathematics & Informatics", _callback("d", "MI")),
        _button("ST · Science & Technology", _callback("d", "ST")),
    ]
    return InlineKeyboardMarkup(_rows(buttons))


def _years_keyboard(branch: str) -> InlineKeyboardMarkup:
    data = ACADEMIC_DATA[branch]
    years = range(1, 6) if branch == "MI" else data["active_years"]
    buttons = [
        _button(
            f"Year {year}" + (" · inactive" if branch == "MI" and year != 1 else ""),
            _callback("y", branch, str(year)),
        )
        for year in years
    ]
    buttons.append(_button("Back", _callback("b", "root")))
    return InlineKeyboardMarkup(_rows(buttons))


def _category_keyboard(
    branch: str, year: int, specialty: str | None = None
) -> InlineKeyboardMarkup:
    specialty_parts = [specialty] if specialty else []
    buttons = [
        _button(label, _callback("c", branch, str(year), *specialty_parts, key))
        for key, label in CATEGORY_LABELS.items()
    ]
    if specialty:
        back = _callback("y", branch, str(year))
    else:
        back = _callback("b", branch)
    buttons.append(_button("Back", back))
    return InlineKeyboardMarkup(_rows(buttons))


def _specialty_keyboard(branch: str, year: int) -> InlineKeyboardMarkup:
    year_data = ACADEMIC_DATA[branch]["years"][year]
    specialties = year_data["specialties"]
    buttons = [
        _button(item["label"], _callback("s", branch, str(year), key))
        for key, item in specialties.items()
    ]
    buttons.append(_button("Back", _callback("b", branch)))
    return InlineKeyboardMarkup(_rows(buttons))


def _resource_keyboard(
    branch: str,
    year: int,
    category: str,
    resources: list[dict[str, str]],
    specialty: str | None = None,
) -> InlineKeyboardMarkup:
    specialty_parts = [specialty] if specialty else []
    buttons: list[InlineKeyboardButton] = []
    for index, item in enumerate(resources):
        if item["url"]:
            buttons.append(InlineKeyboardButton(item["title"], url=item["url"]))
        else:
            buttons.append(
                _button(
                    f"{item['title']} · pending",
                    _callback(
                        "n",
                        branch,
                        str(year),
                        *specialty_parts,
                        category,
                        str(index),
                    ),
                )
            )
    back = _callback("s", branch, str(year), specialty) if specialty else _callback("y", branch, str(year))
    buttons.append(_button("Back", back))
    return InlineKeyboardMarkup(_rows(buttons))


def _start_text() -> str:
    return (
        "Academic Resource Hub\n\n"
        "Choose your branch to find drives, software, tools, and curated playlists."
    )


def _year_text(branch: str) -> str:
    return f"{ACADEMIC_DATA[branch]['label']}\n\nChoose your year."


def _category_text(branch: str, year: int, specialty: str | None = None) -> str:
    year_data = ACADEMIC_DATA[branch]["years"][year]
    if specialty:
        return f"{year_data['specialties'][specialty]['label']}\n\nChoose a resource category."
    return f"{year_data['label']}\n\nChoose a resource category."


def _resource_text(
    branch: str, year: int, category: str, specialty: str | None = None
) -> tuple[str, list[dict[str, str]]]:
    year_data = ACADEMIC_DATA[branch]["years"][year]
    if specialty:
        resources = year_data["specialties"][specialty]["categories"][category]
    else:
        resources = year_data["categories"][category]
    lines = [CATEGORY_LABELS[category], ""]
    for item in resources:
        lines.append(f"• {item['title']}: {item['description']}")
    return "\n".join(lines), resources


async def _edit(
    query: Any,
    text: str,
    keyboard: InlineKeyboardMarkup | None = None,
) -> None:
    await query.edit_message_text(
        text=text,
        reply_markup=keyboard,
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        await update.message.reply_text(_start_text(), reply_markup=_branch_keyboard())


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    query = update.callback_query
    if query is None or query.data is None:
        return

    parts = query.data.split(":")
    action = parts[0]

    if action == "n":
        await query.answer(
            "This resource is not configured yet. Add its URL in resources_data.py.",
            show_alert=True,
        )
        return

    if action == "b":
        await query.answer()
        if parts[1] == "root":
            await _edit(query, _start_text(), _branch_keyboard())
        elif len(parts) == 2:
            await _edit(query, _year_text(parts[1]), _years_keyboard(parts[1]))
        elif len(parts) == 3:
            await _edit(
                query,
                _year_text(parts[1]),
                _years_keyboard(parts[1]),
            )
        return

    if action == "d":
        branch = parts[1]
        await query.answer()
        await _edit(query, _year_text(branch), _years_keyboard(branch))
        return

    if action == "y":
        branch, year = parts[1], int(parts[2])
        if branch == "MI" and year != 1:
            await query.answer(MI_INACTIVE_MESSAGE, show_alert=True)
            return
        await query.answer()
        year_data = ACADEMIC_DATA[branch]["years"][year]
        if "specialties" in year_data:
            await _edit(query, f"{year_data['label']}\n\nChoose your specialty.", _specialty_keyboard(branch, year))
        else:
            await _edit(query, _category_text(branch, year), _category_keyboard(branch, year))
        return

    if action == "s":
        branch, year, specialty = parts[1], int(parts[2]), parts[3]
        await query.answer()
        await _edit(
            query,
            _category_text(branch, year, specialty),
            _category_keyboard(branch, year, specialty),
        )
        return

    if action == "c":
        branch, year = parts[1], int(parts[2])
        if len(parts) == 4:
            category = parts[3]
            specialty = None
        else:
            specialty, category = parts[3], parts[4]
        await query.answer()
        text, resources = _resource_text(branch, year, category, specialty)
        await _edit(
            query,
            text,
            _resource_keyboard(branch, year, category, resources, specialty),
        )
        return

    await query.answer()
    LOGGER.warning("Ignoring unknown callback action: %s", action)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        text = (
            "💡 *ERISE Academic Resource Bot Guide*\n\n"
            "1. Select your Department (MI or ST).\n"
            "2. Select your Year (1 to 5).\n"
            "3. If in Engineering cycle (Years 3–5), select your specialty.\n"
            "4. Access official course drives, software tools, external resources, and YouTube playlists.\n\n"
            "Type /start to return to the main menu at any time."
        )
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    if update.message:
        text = (
            "🌟 *ERISE Scientific Club*\n"
            "National Higher School of Renewable Energies, Environment & Sustainable Development\n"
            "(HNS RE2SD Batna)\n\n"
            "Empowering future engineers through innovation, knowledge sharing, and technical resources."
        )
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def create_application() -> Application:
    token = os.getenv(TOKEN_ENV) or os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            f"{TOKEN_ENV} or BOT_TOKEN is required. Set your bot token in .env or environment variables."
        )

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    return application


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    port_env = os.getenv("PORT")
    if port_env:
        try:
            keep_alive.start_keep_alive(int(port_env))
        except Exception as err:
            LOGGER.warning("Could not start keep_alive server: %s", err)
    LOGGER.info("Starting academic resource bot")
    create_application().run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()