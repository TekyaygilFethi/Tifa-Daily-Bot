import pygsheets
import pandas as pd
import os

from Classes.DateHelper import DateHelper

class GSpreadsheet():
    def __init__(self):
        self.open_connection()
        self.date_object = DateHelper()

    def open_connection(self):
        self.gc = pygsheets.authorize(service_account_env_var='GDRIVE_AUTHENTICATION')
        self.sh = self.gc.open('Fethi Bot Test')
        self.wks = self.sh[0]

    def GetAllRecords(self):
        return pd.DataFrame(self.wks.get_all_records())

    def GetTodaysRecords(self):
        today_date = self.date_object.GetFormattedToday()
        df = self.GetAllRecords()
        df = df[df.Date == today_date]
        return df

    def AddUserDailyInSheet(self, ctx):
        splitted_message = ctx.message.content.split()
        message_contents = [m for m in splitted_message if splitted_message.index(m) > 1]

        try:
            possible_date = self.date_object.ParseDate(splitted_message[2])
            message = ' '.join(message_contents[1:])
        except:
            possible_date = self.date_object.GetFormattedToday()
            message = ' '.join(message_contents)

        users_dict = eval(os.environ['USER_DISCORD_IDS'])
        author_id = ctx.message.author.id
        author_name = ctx.message.author.display_name

        ctx.message.raw_mentions.insert(0, ctx.message.author.id)

        for mention in ctx.message.raw_mentions:
            new_message = message
            formatted_mention = "<@!" + str(mention) + ">"
            user_name = users_dict[mention]

            if mention != author_id:
                new_message = new_message.replace(formatted_mention, author_name)

            for inner_mention in [x for x in ctx.message.raw_mentions if x != author_id or x != mention]:
                formatted_inner_mention = "<@!" + str(inner_mention) + ">"
                new_message = new_message.replace(formatted_inner_mention, users_dict[inner_mention])

            self.CreateNewRecord(user_name, new_message, possible_date)

    def CreateNewRecord(self, user, message, possible_date):
        row_nums = len(self.wks.get_all_records())
        self.wks.insert_rows(row=row_nums + 1, number=3, values=[possible_date, user, message])