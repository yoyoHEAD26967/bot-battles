from arena import Arena

from beginner_bot import BeginnerBot
from balanced_bot import BalancedBot
from smart_hunter_bot import SmartHunterBot
from test_bot import TestBot
from yahya_bot import YahyaBot

arena = Arena(BalancedBot(), YahyaBot())

arena.run()
