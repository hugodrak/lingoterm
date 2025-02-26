import time
import random
import json
import os
import click
from termcolor import colored

# File to store progress
PROGRESS_FILE = "progress.json"

class LanguageTrainer:
    def __init__(self, dataset_file, mode):
        self.dataset_file = dataset_file
        self.mode = mode
        self.words = self.load_words()
        self.progress = self.load_progress()

    def load_words(self):
        words = []
        with open(self.dataset_file, "r", encoding="utf-8") as f:
            for line in f.read().splitlines():
                parts = line.split("\t")
                if len(parts) == 5:
                    words.append({"index": parts[0], "native": parts[1], "meaning": parts[2], "romanized": parts[3]})
        random.shuffle(words)
        print(f"Loaded {len(words)} words.")
        return words

    def load_progress(self):
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_progress(self):
        with open(PROGRESS_FILE, "w") as f:
            json.dump(self.progress, f)

    def get_unlearned_word(self):
        for _ in self.words:
            i = random.randint(0, len(self.words) - 1)
            word = self.words[i]
            key = word["native"]
            if key not in self.progress or self.progress[key] < 3:
                return word
        return None

    def ask_question(self, word):
        native, meaning, romanized = word["native"], word["meaning"], word["romanized"]
        correct_answer = meaning if self.mode == "native2meaning" else native
        prompt = native if self.mode == "native2meaning" else meaning

        print(colored(f"Translate: {prompt}", "cyan"))
        user_input = input("=> ").strip()
        return user_input.lower() == correct_answer.lower(), correct_answer

    def run(self):
        while True:
            word = self.get_unlearned_word()
            if not word:
                print(colored("🎉 You have mastered all words! 🎉", "green"))
                break
            correct, correct_answer = self.ask_question(word)
            native_word = word["native"]
            if correct:
                print(colored(f"✅ Correct! ({correct_answer})", "green"))
                self.progress[native_word] = self.progress.get(native_word, 0) + 1
            else:
                print(colored(f"❌ Incorrect! Correct answer: {correct_answer}", "red"))
                self.progress[native_word] = max(0, self.progress.get(native_word, 0) - 1)
                time.sleep(random.uniform(1, 3))  # Random delay before repeating
            self.save_progress()

@click.command()
@click.option("--dataset", default="korean_words.tsv", help="Path to the TSV dataset.")
@click.option("--mode", default="native2meaning", type=click.Choice(["native2meaning", "meaning2native"]), help="Mode: Native to meaning or Meaning to native.")
def start_trainer(dataset, mode):
    trainer = LanguageTrainer(dataset, mode)
    trainer.run()

if __name__ == "__main__":
    start_trainer()
