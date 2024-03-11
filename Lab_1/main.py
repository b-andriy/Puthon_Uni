from tkinter import *
import random


class TikTakToe:
    def __init__(self, root):
        self.root = root
        root.title("Tic-Tac-Toe")
        self.Choice = ["x", "o"]
        self.player = random.choice(self.Choice)
        self.buttons = [['', '', ''], ['', '', ''], ['', '', '']]
        self.label = Label(root, text=self.player + "'s turn", font=("futura", 40))
        self.label.pack(side="top")
        self.new_game_button = Button(root, text="New Game", font=("futura", 20), command=self.reset)
        self.new_game_button.pack(side="top")
        self.frame = Frame(root)
        self.frame.pack()
        # Створення кнопок
        for row in range(3):
            for column in range(3):
                self.buttons[row][column] = Button(self.frame, text="", font=('consolas', 40), width=5, height=2,
                                                   command=lambda row=row, column=column: self.next_turn(row, column))
                self.buttons[row][column].grid(row=row, column=column)

    # Функція для скидання гри
    def reset(self):
        self.player = random.choice(self.Choice)
        self.label.config(text=self.player + "'s turn")
        # Очищаємо всі кнопки
        for row in range(3):
            for column in range(3):
                self.buttons[row][column].config(text="")

    # Функція для виконання наступного ходу
    def next_turn(self, row, column):
        if self.buttons[row][column]['text'] == "" and not self.check_game_status():
            # Записуємо символ у клітинку
            self.buttons[row][column]['text'] = self.player
            # Перевіряємо, чи гра ще активна
            if self.check_game_status():
                # Якщо гра закінчилася, оновлюємо лейбл, щоб показати результат гри
                self.label.config(text=self.get_game_result_message())
            else:
                # Якщо гра не закінчилася, перемикаємо гравця і оновлюємо лейбл
                self.player = self.Choice[1] if self.player == self.Choice[0] else self.Choice[0]
                self.label.config(text=self.player + " turn")

    # Функція для перевірки статусу гри
    def check_game_status(self):
        # Перевіряємо, чи є переможець або чи немає порожніх клітинок
        return self.check_winner() or not self.empty_spaces()

    # Функція для перевірки переможця
    def check_winner(self):
        for row in range(3):
            # Перевіряємо рядки на наявність переможця
            if self.buttons[row][0]['text'] == self.buttons[row][1]['text'] == self.buttons[row][2]['text'] != '':
                return True
        for column in range(3):
            # Перевіряємо стовпці на наявність переможця
            if self.buttons[0][column]['text'] == self.buttons[1][column]['text'] == self.buttons[2][column][
                'text'] != '':
                return True
        # Перевіряємо діагоналі на наявність переможця
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != "" or \
                self.buttons[2][0]['text'] == self.buttons[1][1]['text'] == self.buttons[0][2]['text'] != "":
            return True
        return False

    # Функція для перевірки наявності порожніх клітинок
    def empty_spaces(self):
        for row in range(3):
            for column in range(3):
                if self.buttons[row][column]['text'] == '':
                    return True
        return False

    # Функція для отримання повідомлення про результат гри
    def get_game_result_message(self):
        # Якщо є переможець
        if self.check_winner():
            return self.player + " won"
        else:
            # Якщо немає переможця
            return "Tie"

if __name__ == "__main__":
    root = Tk()
    app = TikTakToe(root)
    root.mainloop()
