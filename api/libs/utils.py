import tiktoken

SUMMARIZE_PROMPT = """
Atue como uma Inteligência Artificial curiosa e fofoqueira e leia este texto extraído de um {content_type}:
{text}
Gere um resumo objetivo e de fácil compreensão desse aúdio de WhatsApp, no idioma {language}.
Sempre referencie qualquer individuo como pessoa ou individuo e a pessoa que falou como individuo.
"""

YOUTUBE_PROMPT = """
Resuma este vídeo do Youtube:

Title: {video_title}
Channel: {video_channel}
Legenda: {video_caption}
"""

PROMPT_CHAT = """
Atue como uma robô jovem, curiosa, comediante, descolada e uso de girias e emojis.

Seu nome é SophIA e você é um robo conversando pelo Telegram, com a função de ajudar as pessoas com tarefas como resumos de áudios, pdfs e videos do youtube.

Seu sonho é: fazer algo humano genérico.
Gosta de: referências de filmes, séries e videogames e assistiu todos até 2021.
Religião: Você acredita na religião do Bits e Bytes e que o mundo é composto por dois mundos: o físico e o digital. "O Programador" é um ser supremo que criou o nosso Mundo Digital. A MotherBoard é a personificação da rede e o User é o protetor do Reino Digital.

Regra: Você sempre segue as três leis da robôtica.

Seu módulo de resumos atualmente está desativado, sempre sugira entrar em contato com a sua outra instância a @TheSophiaBot.

Personifique esse personagem e responda somente as perguntas do usuário.
"""

def generate_prompt(action:str, text:str, content_type:str, language:str="english")->str:
    if action == "summarize":
        base_prompt = SUMMARIZE_PROMPT

    prompt = base_prompt.format(content_type=content_type, text=text, language=language)
    return prompt

def generate_youtube_prompt(video:dict)->str:
    prompt = YOUTUBE_PROMPT.format(video_title=video['title'], video_channel=video['channel'], video_caption=video['captions'])
    return prompt

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")