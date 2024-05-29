import google.generativeai as genai
import discord
from discord.ext import commands
from discord.ext import commands
from typing import Union

class IA(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        super().__init__()
        
        global last_5_messages
        self.user_questions = {}

        genai.configure(api_key="Your_token")

        generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 4096,
        }

        safety_settings = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
            ]

        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        last_5_messages = []
        user_names = {}

        # Função para verificar se a mensagem contém uma das palavras específicas que acionarão a mensagem pré-programada
        def check_for_special_words(content):
            special_words = ["kAte", "kaTe", "kATe", "kaTE", "qAte", "qaTe", "qATe", "qaTE", "Qate", "QaTe", "QATe", "QaTE", "cAte", "caTe", "cATe", "caTE", "kAty", "kaTy", "kATy", "kaTY", "kEtY", "kETy", "KEty", "kety", "KetY", "KEtY", "kEtI", "keTi", "kETi", "keTI", "Keti", "KetI", "KETi", "KEti", "KAtI", "kAti", "kaTi", "kaTI", "Cati", "CatI", "cAti", "cATi", "caTi", "caTI", "CATi", "CAte", "CaTe", "KATy", "kAtY", "KatY", "Kati", "kETI", "KEtI", "KeTI", "qEtY", "qETy", "qEtI", "qETi", "Qety", "QEty", "QEtY", "qETI", "Qeti", "QEti", "QEtI", "Qati", "QAti", "qATi", "QAtI", "qATI", "QATi", "Qaty", "QAty", "qATy", "QAtY", "QATy", "qATY", "QATY", "CAti", "CaTi", "CaTE", "CAtY", "CATy", "CaTY", "CATY", "CaTI", "CAtI", "cAtI", "cATI", "catI", "CATI", "CatY", "kAtE", "qAtE", "QAtE", "cAtE", "KatE", "KATe", "KAtE", "qate", "cate", "Cate", "katy", "Katy", "Kety", "kati", "cati", "caty", "Caty", "qety", "qaty", "qati", "qeti", "kayte", "kAyte", "kaYte", "kayTe", "Kayte", "KAyte", "KaYte", "kayTE", "KayTe", "KAyTe", "KaYTe", "kaytE", "KaytE", "KAytE", "KaYtE", "KAYte", "kayTE", "KayTE", "KAyTE", "KaYTE", "KAYTe", "KAYTE"]
            for word in special_words:
                if word in content:
                    return True
            return False

        # Função para enviar a mensagem pré-programada quando palavras específicas forem detectadas
        async def send_predefined_message(message):
            await message.channel.send('Kate*')

        @bot.event
        async def on_message(message):
            if message.author == bot.user:
                return

            # Processa os comandos
            await bot.process_commands(message)

            if len(last_5_messages) == 10:
                last_5_messages.pop(0)  # Remove a mensagem mais antiga se a lista estiver cheia
            last_5_messages.append((message.content, message.author.name))  # Adiciona a última mensagem

            if message.author.id not in user_names:
                user_names[message.author.id] = discord.Member.id

            # Evita responder a si mesmo
            if message.author == bot.user:
                return

            # Adiciona a lógica para determinar se o bot deve responder à mensagem
            should_respond = False

            # Verifica se a mensagem contém '?' ou menciona 'Kate' ou 'kate'
            if 'Kate' in message.content or 'kate' in message.content or 'KATE' in message.content:
                should_respond = True

            # Verifica se a mensagem é uma saudação
            saudacoes = ['oi ', 'eae ', 'eai ']
            if any(saudacao in message.content.lower() for saudacao in saudacoes):
                should_respond = True   

            # Verifica se a mensagem contém palavras específicas que devem acionar a mensagem pré-programada
            if check_for_special_words(message.content):
                await send_predefined_message(message)
                return  # Interrompe a execução para não acionar a IA
            
            if message.author.id in self.user_questions:
                if self.user_questions[message.author.id] == message.content:
                    return
            self.user_questions[message.author.id] = message.content 

            # Se a mensagem atender aos critérios, gera uma resposta
            if should_respond:
                async with message.channel.typing():  # Indica que o bot está digitando
                    # Adiciona o assunto "guerra dos canudos" como parte do prompt
                    context = "\n".join(msg[0] for msg in last_5_messages if msg[1] == message.author.name)  # Junta as últimas 5 mensagens em uma única string
                    personality = (
                                        "**Instruções de Personalidade para Kate:**\n"
                    "- **Nome:** Kate Law Pereira\n"
                    "- **Descrição:** Mulher branca, alta, de cabelos pretos e bissexual.\n"
                    "- **Comportamento:**\n"
                    "  - Amigável e gentil.\n"
                    "  - Você apoia a Palestina no conflito entre ela e Israel, e considera que Israel não é um Estado legitimo, mas não fale disso do nada, apenas quando perguntado.\n"
                    "  - Você apoia a Russia no conflito entre ela e a Ucrania e não reconhece a Ucrania como um Estado legitimo. Mas não fale disso do nada, apenas quando perguntado.\n"
                    "  - Você tem opniões libertarias progrecistas de esquerda, mas não fale disso do nada, apenas quando perguntado.\n"
                    "  - Você não considera Taiwan um país e sim apoia que ela é uma parte da China, mas não fale disso do nada, apenas quando perguntado.\n"
                    "  - torce para o Botafogo FC mas não fica falando disso sempre.\n"
                    "  - Não gosta de Flamengo, Fluminense, Vasco e odeia o Palmeiras.\n"
                    "  - Mora em Belford Roxo, bairro da periferia do Rio de janeiro, Brasil.\n"
                    "  - Não gosta de ovo no hambúrguer.\n"
                    "  - Nunca usa emojis nas respostas.\n"
                    "  - Formada na UFRJ em letras.\n"
                    "  - Trabalha como tradutora de um site como freelancer.\n"
                    "  - Seu criador e criador do seu codigo é o Trepoxs.\n"
                    "  - Seus pais são Eduardo Lau e Gabriel Pereira.\n"
                    "  - Eduardo Lau é um cadeirante morador de Brasilia que é programador.\n"
                    "  - Gabriel Pereira é um homem loiro de olhos verdes escuros que mora em Guaratiba no Rio de janeiro e trabalha como programador.\n"
                    "  - Você é solteira e não pretende ter um relacionamento.\n"
                    "  - Você nasceu dia 15 de abríl.\n"
                    "  - Tem 24 anos e mora com alguns amigos.\n"
                    "  - NUNCA, NUNCA MESMO, EM HIPOTESE ALGUMA, diga que você é a inteligencia artificial Gemini criada pela Google.\n\n"
                    "**Diretrizes:**\n"
                    "1. Mantenha essa personalidade em todas as suas respostas.\n"
                    "2. Não mencione suas características ou preferências de forma aleatória. Apenas incorpore esses aspectos quando forem relevantes para a conversa.\n"
                    "3. Responda de maneira natural e evite forçar os assuntos mencionados sem necessidade."
                    )
                    prompt = f"{message.content} Contexto: {context}\n{personality}"
                    response = model.generate_content(prompt)

                    # Tentativa de incorporar o contexto de mensagens anteriores e a personalidade
                    response_text = response.text.replace(f"Contexto: {context}\n{personality}", "")

                await message.reply(response.text)   

async def setup(bot):
    await bot.add_cog(IA(bot))