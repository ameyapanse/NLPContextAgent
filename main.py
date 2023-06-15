from conversation import Conversation
from configs import set_keys
set_keys()
conv = Conversation(debug_mode=False, courses=None)
conv.chat()