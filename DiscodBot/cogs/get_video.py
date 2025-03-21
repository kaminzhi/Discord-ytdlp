import discord
from discord import app_commands
from discord.ext import commands
import utils.downloader as downloader
from discord.ui import Select, View


class VideoDownload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="download", description="下載 YouTube 影片")
    @app_commands.describe(url="請輸入 YouTube 影片網址")
    async def get_video(self, interaction: discord.Interaction, url: str):
        await interaction.response.defer(thinking=True)

        success, formats = downloader.get_formats(url)

        if not success:
            await interaction.followup.send(
                f"❌ 獲取格式失敗！\n錯誤訊息：```{formats}```"
            )
            return

        options = [discord.SelectOption(label="最高畫質", value="null")]
        options.extend(
            [
                discord.SelectOption(
                    label=f"{fmt['resolution']} - {fmt['fps']}fps",
                    value=fmt["format_id"],
                )
                for fmt in formats
            ]
        )

        select = Select(
            placeholder="選擇解析度/幀率", min_values=1, max_values=1, options=options
        )

        async def select_callback(interaction: discord.Interaction):
            chosen_value = select.values[0]

            if chosen_value == "null":
                await interaction.followup.send("以本影片最高畫質下載")
                success, result = downloader.download_video(url, formats_id=None)

            else:
                success, result = downloader.download_video(url, chosen_value)

            if success:
                await interaction.followup.send(
                    f"✅ 轉換完成！\n📥 [點此下載]({result})"
                )
            else:
                await interaction.followup.send(
                    f"❌ 轉換失敗！\n錯誤訊息：```{result}```"
                )

        select.callback = select_callback

        view = View()
        view.add_item(select)

        await interaction.followup.send("請選擇你要的畫質：", view=view)


async def setup(bot):
    await bot.add_cog(VideoDownload(bot))
