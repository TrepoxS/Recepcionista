import datetime
import random
import asyncio
import discord
from discord.ext import commands
from discord.ext import commands

ids_to_mark = [539573952293371925, 1215101248051871785, 539902997568946186, 299236832271532032, 453312192507281418, 848296948264075334, 639578268756082689, 483951165592305665, 845024865739997224, 968609750206001162, 366295924370178053, 939631239248367696, 340281735394754564, 802409659012349972, 365976506473644044, 1070121026991685663, 1002074604405272657]
ids_burros = [483951165592305665, 560102412103450637, 639578268756082689, 802409659012349972, 1016902031618871356, 1002074604405272657]

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        super().__init__()
        
        def add_id(member_id):
            if member_id not in ids_burros:
                ids_burros.append(member_id)
                return True
            else:
                return False   
            
        def add_burro(member_id):
            if member_id not in ids_burros:
                ids_burros.append(member_id)
                return True
            else:
                return False
            
        def remove_burro(member_id):
            if member_id in ids_burros:
                ids_burros.remove(member_id)
                return True
            else:
                return False

        def add_id(member_id):
            if member_id not in ids_to_mark:
                ids_to_mark.append(member_id)
                return True
            else:
                return False

        def remove_id(member_id):
            if member_id in ids_to_mark:
                ids_to_mark.remove(member_id)
                return True
            else:
                return False

        @bot.hybrid_command(name='adicionar', with_app_command=True, description='Adiciona o usuário na lista dos de verdade')
        async def burro(ctx: commands.Context, member: discord.Member):
            role_id = 1229823390014246972

            # Verifica se o autor do comando está na lista de ids_burros
            if ctx.author.id in ids_burros:
                await ctx.send("Você é burro demais para usar esse comando, estude.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            if role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            if member.id in ids_to_mark:
                await ctx.send(f"{member.mention} já um um dos de verdade, seu burro.")
                return

            # Adiciona o ID especificado na lista de ids monitorados
            ids_to_mark.append(member.id)
            await ctx.send(f"O {member.mention} deixou de ser random e entrou na lista dos de verdade.")

        @bot.hybrid_command(name='del', with_app_command=True, description='Tira o usuario da lista dos de verdade e deixa ele como um random, o que ele é.')
        async def deletar(ctx: commands.Context, member: discord.Member):
            role_id = 1229823390014246972

            # Verifica se o autor do comando está na lista de ids_burros
            if ctx.author.id in ids_burros:
                await ctx.send("Você é burro demais para usar esse comando, estude.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            if role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            # Verifica se o ID especificado está na lista de ids monitorados
            if member.id in ids_to_mark:
                # Remove o ID especificado da lista de ids monitorados
                ids_to_mark.remove(member.id)
                await ctx.send(f"O random do {member.mention} foi removido da lista dos de verdade.")
            else:
                await ctx.send(f"O {member.mention} não é um random, ele já faz parte da lista dos de verdade.")

        @bot.hybrid_command(name='burro', with_app_command=True, description='Coloca o burro na lista de burros que não podem usar comandos')
        async def burro(ctx: commands.Context, member: discord.Member):
            role_id = 1229823390014246972

            # Verifica se o autor do comando está na lista de ids_burros
            if ctx.author.id in ids_burros:
                await ctx.send("Você é burro demais para usar esse comando, estude.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            if role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            if member.id in ids_burros:
                await ctx.send(f"{member.mention} já ta na lista de burro kkk, esperava oq kkk")
                return

            # Adiciona o ID especificado na lista de ids monitorados
            ids_burros.append(member.id)
            await ctx.send(f"O {member.mention} é muito burro, vou levar ele pra estudar.")


        @bot.hybrid_command(name='estudou', with_app_command=True, description='Tira o burrinho da lista de burros que não podem usar comandos')
        async def estudou(ctx: commands.Context, member: discord.Member):
            role_id = 1229823390014246972

            # Verifica se o autor do comando está na lista de ids_burros
            if ctx.author.id in ids_burros:
                await ctx.send("Você é burro demais para usar esse comando, estude.")
                return

            # Verifica se o autor do comando tem permissão para usar o comando
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            if role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo.")
                return

            # Verifica se o ID especificado está na lista de ids monitorados
            if member.id in ids_burros:
                # Remove o ID especificado da lista de ids monitorados
                ids_burros.remove(member.id)
                await ctx.send(f"O {member.mention} estudou o suficiente, eu acho.")
            else:
                await ctx.send(f"O {member.mention}, por incrivel que pareça, não está na lista de burros.")

        @bot.hybrid_command(name= 'call', with_app_command= True, description = 'Chama para a call os de verdade que estão online')
        async def call(ctx: commands.Context):
            online_members = [member for member in ctx.guild.members if member.status != discord.Status.offline]
            call_members = [member for channel in ctx.guild.voice_channels for member in channel.members]

            members_to_mark = [member for member in online_members if member not in call_members and member.id in ids_to_mark and member != ctx.author]

            if members_to_mark:
                await ctx.send(f"Call? {' '.join(member.mention for member in members_to_mark)}")
            else:
                await ctx.send("Ta todo mundo off lerdão")

        @bot.hybrid_command(name= 'list', with_app_command= True, description = 'Lista os de verdade que podem ser marcados')
        async def list(ctx: commands.Context):
            role_id = 1229823390014246972  # ID do cargo necessário para executar este comando
            await ctx.defer(ephemeral= True)
            
            if ctx.author.id in ids_burros:
                await ctx.send('Você é burro de mais para executar esse comando, estude.')
                return

            role = discord.utils.get(ctx.guild.roles, id=role_id)
            if role is None:
                await ctx.send("CONFIGURA O CARGO SEU ANIMAL")
                return

            if role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo")
                return

            members_to_mark = [member.mention for member_id in ids_to_mark if (member := ctx.guild.get_member(member_id)) is not None]

            if members_to_mark:
                await ctx.send(f"Os de verdade {' '.join(members_to_mark)}")
            else:
                await ctx.send("Você é solitário.")

        @bot.hybrid_command(name= 'burroslist', with_app_command= True, description = 'Lista os burros que não podem usar comandos')
        async def burroslist(ctx: commands.Context):
            role_id = 1229823390014246972  # ID do cargo necessário para executar este comando
            await ctx.defer(ephemeral= True)

            if ctx.author.id in ids_burros:
                await ctx.send('Você é burro de mais para executar esse comando, estude.')
                return

            role = discord.utils.get(ctx.guild.roles, id=role_id)
            if role is None:
                await ctx.send("CONFIGURA O CARGO SEU ANIMAL")
                return

            if role not in ctx.author.roles:
                await ctx.send("Você é random, não entrosa, sem cargo")
                return

            members_to_mark = [member.mention for member_id in ids_burros if (member := ctx.guild.get_member(member_id)) is not None]

            if members_to_mark:
                await ctx.send(f"Os burrinhos do server {' '.join(members_to_mark)}")
            else:
                await ctx.send("Você é solitário.")

        @bot.tree.command(name='perfil', description='Mostra as informações do perfil do membro escolhido.')
        async def perfil(interaction: discord.Interaction, member: discord.Member = None):
            if member is None:
                member = interaction.user

            embed = discord.Embed(
                title='Informações de Usuário',
                description=f'Essas são as informações de {member.mention}',
                color=discord.Color.dark_gray(),
                timestamp=datetime.datetime.now()
            )
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name='ID', value=member.id)
            embed.add_field(name='Nome', value=f'{member.name}')
            embed.add_field(name='Nickname', value=member.display_name)
            embed.add_field(name='Status', value= member.status)
            embed.add_field(name='Criado em', value=member.created_at.strftime('%a, %B %d, %Y, %I:%M %p'))
            embed.add_field(name='Entrou em', value=member.joined_at.strftime('%a, %B %d, %Y, %I:%M %p'))

            await interaction.response.send_message(embed=embed)

        @bot.tree.command(name='clear', description='Limpa até 100 mensagens do chat.')
        async def clear(ctx: discord.Interaction, quantidade: int):
            # Verifica se a quantidade está entre 0 e 100
            if 0 < quantidade <= 100:
                # Adia a resposta inicial
                await ctx.response.defer()

                # Limpa as mensagens
                deleted = await ctx.channel.purge(limit=quantidade)

                # Envia uma mensagem confirmando a limpeza
                await ctx.send(f"Foram apagadas {len(deleted)} mensagens.", ephemeral=True)
            else:
                # Envia uma mensagem de erro se a quantidade estiver fora do intervalo permitido
                await ctx.send("Você pode limpar entre 1 e 100 mensagens.", ephemeral=True)

        @bot.tree.command(name='backrooms', description="Joga o colegão nas backrooms.")
        async def backrooms(interaction: discord.Interaction, member: discord.Member):
            try:
                role_id = 1059650347834032219  # ID do cargo necessário para executar este comando
                novo_cargo_id = 1028537557195169872  # Substitua pelo ID do cargo desejado

                role_id = interaction.guild.get_role(role_id)
                if role_id is None or role_id not in interaction.user.roles:
                    return await interaction.response.send_message("Você não é um Guardião das Backrooms.")

                # Obtém o objeto de cargo usando o ID fornecido
                novo_cargo = interaction.guild.get_role(novo_cargo_id)
                if novo_cargo is None:
                    return await interaction.response.send_message("O cargo especificado não foi encontrado.")

                # Remove todos os outros cargos do usuário
                await member.edit(roles=[novo_cargo], reason="Troca de cargo")

                await interaction.response.send_message(f"O {member.mention} foi movido para as backrooms.")
            except Exception as e:
                await interaction.response.send_message(f"Ocorreu um erro ao trocar os cargos: {e}")

        @bot.tree.command(name='mute', description="Joga o colegão nas backrooms.")
        async def backrooms(interaction: discord.Interaction, member: discord.Member, horas: int, minutos: int, segundos: int):
            try:
                role_id = 1059650347834032219  # ID do cargo necessário para executar este comando
                novo_cargo_id = 1028537557195169872  # Substitua pelo ID do cargo desejado

                role_id = interaction.guild.get_role(role_id)
                if role_id is None or role_id not in interaction.user.roles:
                    return await interaction.response.send_message("Você não é um Guardião das Backrooms.")

                # Obtém o objeto de cargo usando o ID fornecido
                novo_cargo = interaction.guild.get_role(novo_cargo_id)
                if novo_cargo is None:
                    return await interaction.response.send_message("O cargo especificado não foi encontrado.")

                # Remove todos os outros cargos do usuário
                await member.edit(roles=[novo_cargo], reason="Troca de cargo")

                await interaction.response.send_message(f"O {member.mention} foi levado para um lugar desconhecido, daqui um tempinho ele volta.")

                # Espera o tempo especificado
                await asyncio.sleep(horas * 3600 + minutos * 60 + segundos)

                # Restaura os cargos originais do usuário
                await member.edit(roles=member.roles, reason="Restauração de cargos")
                
                await interaction.response.send_message(f"O tempo expirou para {member.mention}, os cargos foram restaurados.")
            except Exception as e:
                await interaction.response.send_message(f"Ocorreu um erro ao trocar os cargos: {e}")

        @bot.tree.command(name='escolha', description='Escolhe uma das duas opções aleatoriamente.')
        async def escolha(interaction: discord.Interaction, opção1: str, opção2: str):
            options = [opção1, opção2]
            chosen_option = random.choice(options)
            await interaction.response.send_message(f"Pensei bem e, com certeza, eu escolho {chosen_option}.")

        class MyView(discord.ui.View):
            def __init__(self):
                super().__init__()
                self.add_github_button()  # Chamamos o método para adicionar o botão do Github

            def add_github_button(self):
                # Adiciona o botão do Github
                self.add_item(discord.ui.Button(label='Github', style=discord.ButtonStyle.url, url='https://github.com/TrepoxS/Recepcionista/tree/main'))      

            #setting up button (you can add multiple such)
            @discord.ui.button(label='Comandos', style=discord.ButtonStyle.blurple)
            async def asdf(self, interaction: discord.Interaction, button: discord.ui.Button):
                # on interaction
                await interaction.response.send_message('''No momento eu possuo alguns comandos slash que utilizam o prefixo '/', recomendo digitar no seu chat e me procurar na barra lateral a esquerda, assim pode ver os comandos e suas descrições.

            Fora desses, também tenho alguns comandos de música com o prefixo '.' que são:

            Play = Toca um áudio a partir do link de um vídeo do Youtube.
            Pause = Pausa o áudio que está tocando.
            Resume = Faz o áudio pausado voltar a tocar.
            Skip = Pula o áudio que está tocando naquele momento e começa o áudio seguinte.
            Stop = Para o áudio atual e me desconecta da chamada.

            Espero ter ajudado ;)''', ephemeral=True)
            print("yes")

            #setting up button (you can add multiple such)
            @discord.ui.button(label='Créditos', style=discord.ButtonStyle.green)
            async def asd2f(self, interaction: discord.Interaction, button: discord.ui.Button):
                # on interaction
                await interaction.response.send_message('Meus criadores e tutores foram o @d.lau e o @trepoxs, pelo o que me lembro tambem teve um caso de traição com um tal de Chat GPT mas a gente n fala sobre isso.', ephemeral=True)
                print("yes")          

        @bot.tree.command(name="help", description="Comandos, criadores e codigo opensource da secretaria.")
        async def hello(ctx: discord.Interaction):
            # add the view to a message
            await ctx.response.send_message("", view=MyView(), ephemeral=True)    

async def setup(bot):
    await bot.add_cog(Slash(bot))

