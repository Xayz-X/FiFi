from threading import local
import discord
from discord import app_commands


class TreeTranslator(app_commands.Translator):
    """
    This class is a part ot app command translation system. Translate the command name description as per user locale.
    """

    async def load(self):
        # Not implemented yet
        ...

    async def unload(self):
        # Not implemented yet
        ...

    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext,
    ) -> str | None:
        """
        This function must return a string (that's been translated), or `None` to signal no available translation available, and will default to the original.

        Parameters
        ----------
        string : app_commands.locale_str
            The string that is requesting to be translated
        locale : discord.Locale
            The target language to translate to
        context : app_commands.TranslationContext
            The origin of this string, eg TranslationContext.command_name, etc
        """
        print(locale)
        if locale == discord.Locale.japanese:
            message_str = str(string.message)
            print(message_str)
            if message_str == "testing":
                return "テスト"
            elif message_str == "This is a teting command.":
                return "これはテストコマンドです。"

            elif message_str == "number":
                return "数字"
            elif message_str == "This is a number.":
                return "これは数字です。"
            
        return None
