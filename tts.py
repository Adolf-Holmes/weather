#%%
from gtts import gTTS
tts = gTTS('你好', lang='zh-tw')
tts.save('hello.mp3')


# %%
