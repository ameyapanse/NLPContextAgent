from conversation import Conversation
from embed import Embedder
from configs import set_keys
set_keys()
e = Embedder()
e.embed_all_documents()
conv = Conversation(debug_mode=False, courses=None)
conv.chat()