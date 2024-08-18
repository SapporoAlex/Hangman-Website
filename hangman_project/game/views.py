from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random

words_dict = {1: ["elephant", "giraffe"], 2: ["harrypotter", "hermionegranger"], 3: ["python", "javascript"]}

stick_figure_dict = {0: "", 1: " O ", 2: " O\n | ", 3: " O\n/| ", 4: " O\n/|\\", 5: " O\n/|\\\n/", 6: " O\n/|\\\n/ \\"}

@login_required
def play_game(request, category):
    # Your game logic here
    pass

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def play_game(request, category):
    if request.method == "POST":
        guess = request.POST.get('guess').lower()
        word = request.session['word']
        guessed_letters = request.session['guessed_letters']
        guessed_wrong_amount = request.session['guessed_wrong_amount']

        if guess in guessed_letters:
            return render(request, 'play_game.html', {'error': 'You already guessed that letter!', 'stick_figure': stick_figure_dict[guessed_wrong_amount]})

        guessed_letters.append(guess)
        if guess in word:
            word_tiles = list(request.session['word_tiles'])
            for i, letter in enumerate(word):
                if letter == guess:
                    word_tiles[i] = guess
            request.session['word_tiles'] = ''.join(word_tiles)
        else:
            guessed_wrong_amount += 1
            request.session['guessed_wrong_amount'] = guessed_wrong_amount

        if guessed_wrong_amount == 6:
            return render(request, 'play_game.html', {'stick_figure': stick_figure_dict[6], 'message': f"You lost! The word was {word}"})
        elif '_' not in request.session['word_tiles']:
            return render(request, 'play_game.html', {'stick_figure': stick_figure_dict[guessed_wrong_amount], 'message': "You won!"})

    else:
        word = random.choice(words_dict[category])
        request.session['word'] = word
        request.session['word_tiles'] = "_" * len(word)
        request.session['guessed_letters'] = []
        request.session['guessed_wrong_amount'] = 0

    return render(request, 'play_game.html', {'stick_figure': stick_figure_dict[0], 'word_tiles': request.session['word_tiles']})

def leaderboard(request):
    return render(request, 'leaderboard.html')
