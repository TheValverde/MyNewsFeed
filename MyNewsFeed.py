import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import requests
from bs4 import BeautifulSoup
from supabase_py import create_client, Client

supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

class NewsSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("News Summarizer")
        self.topic_list = []
        self.add_topic_button = tk.Button(root, text="Add Topic", command=self.add_topic)
        self.add_topic_button.pack()
        self.topic_listbox = tk.Listbox(root)
        self.topic_listbox.pack()
        self.remove_topic_button = tk.Button(root, text="Remove Topic", command=self.remove_topic)
        self.remove_topic_button.pack()
        self.refresh_feed_button = tk.Button(root, text="Refresh Feed", command=self.refresh_feed)
        self.refresh_feed_button.pack()
        self.headline_listbox = tk.Listbox(root)
        self.headline_listbox.pack()
        self.load_topics()
        if self.topic_list:
            self.refresh_feed()

    def load_topics(self):
        if os.path.exists('topics.txt'):
            with open('topics.txt', 'r') as file:
                self.topic_list = file.read().strip().split('\n')
                for topic in self.topic_list:
                    self.topic_listbox.insert(tk.END, topic)

    def save_topics(self):
        with open('topics.txt', 'w') as file:
            file.write('\n'.join(self.topic_list))

    def add_topic(self):
        topic = simpledialog.askstring("Input", "Please enter a topic:")
        if topic:
            self.topic_list.append(topic)
            self.topic_listbox.insert(tk.END, topic)
            self.save_topics()

    def remove_topic(self):
        selected_topic_index = self.topic_listbox.curselection()
        if selected_topic_index:
            self.topic_listbox.delete(selected_topic_index)
            self.topic_list.pop(selected_topic_index[0])
            self.save_topics()

    def refresh_feed(self):
        headlines = self.get_headlines()
        self.headline_listbox.delete(0, tk.END)  # Clear previous headlines
        for topic, headlines in headlines.items():
            for headline in headlines:
                self.headline_listbox.insert(tk.END, f"{topic}: {headline}")

    def get_headlines(self):
        headlines = {}
        for topic in self.topic_list:
            url = f'https://news.google.com/search?q={topic}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            headlines[topic] = [item.text for item in soup.find_all('a', {'class': 'DY5T1d'})]
        return headlines
    
if __name__ == "__main__":
    root = tk.Tk()
    app = NewsSummarizerApp(root)
    root.mainloop()
