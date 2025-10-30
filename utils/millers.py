import os
import locale
from openai import OpenAI
from dotenv import load_dotenv
import utils.extractors as extractors

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
load_dotenv()

class SimpleOpenAILabeler:
    API_KEY = os.getenv('OPENAI_API_KEY')

    def __init__(self, transaction):
        self.transaction = transaction
        self.openai = OpenAI()
        self.df_cat = extractors.fetch_categories()
        self.system_prompt = self.create_system_prompt()
        self.messages = self.create_messages()

    def create_system_prompt(self):
        categories_markdown = self.df_cat.loc[:, ['parent_name', 'category_name']].to_markdown(index=False)

        system_prompt = (f"You are labeling the categories of transactions for a personal budget. "
                         f"The following categories are available for you:\n\n{categories_markdown}\n\n"
                         "Reply only with the category name, no explanation")

        return system_prompt

    def create_messages(self):
        amount_fmt = locale.currency(abs(self.transaction['amount']), grouping=True)
        user_prompt = (f"The transaction description is \"{self.transaction['description']}\" "
                       f"and the amount is {amount_fmt}")

        return [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": "The category is:"},
        ]

    def get_category(self):
        response = self.openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=self.messages,
            seed=69,
            # max_tokens=5,
        )
        reply = response.choices[0].message.content

        return reply