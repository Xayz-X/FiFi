import discord
from discord import app_commands


class TreeTranslator(app_commands.Translator):
  
    async def load(self): ...
    async def unload(self): ...

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

        message_str = string.message
        return message_str