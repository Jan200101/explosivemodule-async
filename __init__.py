from sys import _getframe
from __main__ import bot
from discord.ext.commands import Context


class MissingContext(Exception):
    pass


class asyncmodule:

    def __init__(self, bot):
        functions = {
            'say': self.say,
            'send_message': self.send_message,
            'send_typing': self.send_typing,
        }

        self.appendattr(bot, functions)

    @staticmethod
    def appendattr(bot, functions):
        for name, val in functions.items():
            bot.__setattr__(name, val)

    # BRIDGE FUNCTIONS BEYOND HERE
    async def say(self, msg):
        stack = [x[1] for x in _getframe(
            1).f_locals.items() if isinstance(x[1], Context)]
        if not stack:
            print("WARNING Context is missing in " +
                  _getframe(1).f_code.co_name)
            # context was optional in async and mandatory in rewrite
            return
        await stack[0].send(msg)

    async def send_message(self, channel, msg):
        return await channel.send(msg)

    async def send_typing(self, destination, *args, **kwargs):
        await destination.trigger_typing(*args, **kwargs)

    async def wait_for_message(self, *args, **kwargs):
        return await bot.wait_for('message', *args, **kwargs)


def init():
    asyncmodule(bot)


def destroy():
    pass
