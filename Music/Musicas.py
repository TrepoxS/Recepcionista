import discord
from discord.ext import commands
import asyncio
import yt_dlp
from dotenv import load_dotenv
import urllib.parse, urllib.request, re
from typing import Union

queues = {}
voice_bots = {}
youtube_base_url = 'https://www.youtube.com/'
youtube_results_url = youtube_base_url + 'results?'
youtube_watch_url = youtube_base_url + 'watch?v='
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn -filter:a "volume=0.25"'}

class Musicas(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        super().__init__()

    async def play_next(self, ctx):
        if queues[ctx.guild.id] != []:
            link = queues[ctx.guild.id].pop(0)
            await self.play(ctx, link=link)
    
    @commands.command(name="play")
    async def play(self, ctx, *, link):
        try:
            # Verifica se o comando está sendo usado no canal correto
            allowed_channel_id = 966756925402386474  # ID do canal permitido
            if ctx.channel.id != allowed_channel_id:
                await ctx.send("TEM UM CHAT DE COMANDO DE MUSICA IRMÃO.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role_id = 1238236350914760785  # ID do cargo requerido
            required_role = discord.utils.get(ctx.guild.roles, id=role_id)
            if required_role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            # Verifica se o autor do comando está em um canal de áudio
            if ctx.author.voice is None or ctx.author.voice.channel is None:
                await ctx.send("Você não tá em nenhum canal de áudio, burro.")
                return

            # Se o bot não está conectado, conecta-se ao canal do autor
            if ctx.guild.id not in voice_bots or not voice_bots[ctx.guild.id].is_connected():
                voice_bot = await ctx.author.voice.channel.connect()
                voice_bots[voice_bot.guild.id] = voice_bot
            else:
                voice_bot = voice_bots[ctx.guild.id]

            # Adiciona a música à fila se já há uma música tocando
            if voice_bot.is_playing() or voice_bot.is_paused():
                if ctx.guild.id not in queues:
                    queues[ctx.guild.id] = []
                queues[ctx.guild.id].append(link)
                await ctx.send("Adicionado à fila!")
                return

            # Caso contrário, reproduz a música imediatamente
            if "www.youtube.com" not in link:
                query_string = urllib.parse.urlencode({'search_query': link})
                content = urllib.request.urlopen(youtube_results_url + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                link = youtube_watch_url + search_results[0]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))
            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)
            voice_bot.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), loop))
        except Exception as e:
            print(e)

    @commands.command(name="clear")
    async def clear_queue(self, ctx):
        try:
            # Verifica se o comando está sendo usado no canal correto
            allowed_channel_id = 966756925402386474  # ID do canal permitido
            if ctx.channel.id != allowed_channel_id:
                await ctx.send("TEM UM CHAT DE COMANDO DE MUSICA IRMÃO.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role_id = 1238236350914760785  # ID do cargo requerido
            required_role = discord.utils.get(ctx.guild.roles, id=role_id)
            if required_role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            if ctx.guild.id in queues:
                queues[ctx.guild.id].clear()
                await ctx.send("Lista limpa.")
            else:
                await ctx.send("Não tem nada na lista, boboca.")
        except Exception as e:
            print(e)

    @commands.command(name="pause")
    async def pause(self, ctx):
        try:
            # Verifica se o comando está sendo usado no canal correto
            allowed_channel_id = 966756925402386474  # ID do canal permitido
            if ctx.channel.id != allowed_channel_id:
                await ctx.send("TEM UM CHAT DE COMANDO DE MUSICA IRMÃO.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role_id = 1238236350914760785  # ID do cargo requerido
            required_role = discord.utils.get(ctx.guild.roles, id=role_id)
            if required_role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            voice_bots[ctx.guild.id].pause()
        except Exception as e:
            print(e)

    @commands.command(name="resume")
    async def resume(self, ctx):
        try:
            # Verifica se o comando está sendo usado no canal correto
            allowed_channel_id = 966756925402386474  # ID do canal permitido
            if ctx.channel.id != allowed_channel_id:
                await ctx.send("TEM UM CHAT DE COMANDO DE MUSICA IRMÃO.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role_id = 1238236350914760785  # ID do cargo requerido
            required_role = discord.utils.get(ctx.guild.roles, id=role_id)
            if required_role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            voice_bots[ctx.guild.id].resume()
        except Exception as e:
            print(e)

    @commands.command(name="stop")
    async def stop(self, ctx):
        try:
            # Verifica se o comando está sendo usado no canal correto
            allowed_channel_id = 966756925402386474  # ID do canal permitido
            if ctx.channel.id != allowed_channel_id:
                await ctx.send("TEM UM CHAT DE COMANDO DE MUSICA IRMÃO.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role_id = 1238236350914760785  # ID do cargo requerido
            required_role = discord.utils.get(ctx.guild.roles, id=role_id)
            if required_role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            voice_bot = voice_bots[ctx.guild.id]
            if voice_bot.is_connected():
                await voice_bot.disconnect()
            del voice_bots[ctx.guild.id]
        except Exception as e:
            print(e)

    @commands.command(name="skip")
    async def skip(self, ctx):
        try:
            # Verifica se o comando está sendo usado no canal correto
            allowed_channel_id = 966756925402386474  # ID do canal permitido
            if ctx.channel.id != allowed_channel_id:
                await ctx.send("TEM UM CHAT DE COMANDO DE MUSICA IRMÃO.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role_id = 1238236350914760785  # ID do cargo requerido
            required_role = discord.utils.get(ctx.guild.roles, id=role_id)
            if required_role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            voice_bot = voice_bots[ctx.guild.id]
            voice_bot.stop()
            await self.play_next(ctx)
            await ctx.send("Música pulada!")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(Musicas(bot))