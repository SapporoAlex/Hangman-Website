from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random

words_dict = {
    1: ["elephant", "giraffe", "penguin", "dolphin", "kangaroo", "butterfly", "hummingbird", "rhinoceros", "alligator", "ostrich"],
    2: ["harrypotter", "harrypotter"],
    #2: ["harrypotter", "hermionegranger", "ronweasley", "albusdumbledore", "severussnape"],
    3: ["python", "javascript", "java", "csharp", "ruby"]
}

wrong_messages = [
    "You big silly!", "Unbelievable!", "You blew it!", "Some muthas are still tryna' ice-skate uphill", "You couldn't guess your way out of a paper bag!"
]

@login_required
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
        if 'action' in request.POST:
            action = request.POST['action']
            if action == "play_game":
                # Start a new game
                word = random.choice(words_dict[category])
                request.session['word'] = word
                request.session['word_tiles'] = "_" * len(word)
                request.session['guessed_letters'] = ""
                request.session['guessed_wrong_amount'] = 0
                return render(request, 'play_game.html', {
                    'stickword': word,
                    'guessed_wrong_amount': 0,
                    'word_tiles': request.session['word_tiles']
                })
            elif action == "home":
                return redirect('home')  # Redirect to the home view

        guess = request.POST.get('guess', '').lower()

        # Get current game state
        word = request.session.get('word')
        guessed_letters = request.session.get('guessed_letters', "")
        guessed_wrong_amount = request.session.get('guessed_wrong_amount', 0)

        # Check for valid guess
        if len(guess) != 1 or not guess.isalpha():
            return render(request, 'play_game.html', {
                'error': 'Invalid guess. Please enter a single letter.',
                'guessed_letters': guessed_letters,
                'stickword': word,
                'guessed_wrong_amount': guessed_wrong_amount,
                'word_tiles': request.session['word_tiles']
            })

        # Check for already guessed
        if guess in guessed_letters:
            return render(request, 'play_game.html', {
                'error': 'You already guessed that letter!',
                'guessed_letters': guessed_letters,
                'stickword': word,
                'guessed_wrong_amount': guessed_wrong_amount,
                'word_tiles': request.session['word_tiles']
            })

        # Process the guess
        if guess in word:
            word_tiles = list(request.session['word_tiles'])
            for i, letter in enumerate(word):
                if letter == guess:
                    word_tiles[i] = guess
            request.session['word_tiles'] = ''.join(word_tiles)
        else:
            guessed_wrong_amount += 1
            request.session['guessed_wrong_amount'] = guessed_wrong_amount

        guessed_letters += guess + ", "
        request.session['guessed_letters'] = guessed_letters

        # Losing condition
        if guessed_wrong_amount == 5:
            wrong_message = random.choice(wrong_messages)
            return render(request, 'play_game.html', {
                'stickword': word,
                'guessed_wrong_amount': guessed_wrong_amount,
                'game_over': '<button type="submit" name="action" value="play_game">Play Again</button><button type="submit" name="action" value="home">Home</button>',
                'message': f"You lost! The word was {word}. {wrong_message}",
                'word_tiles': request.session['word_tiles']
            })

        # Winning condition
        if '_' not in request.session['word_tiles']:
            return render(request, 'play_game.html', {
                'stickword': word,
                'guessed_wrong_amount': 5,
                'game_over': '<button type="submit" name="action" value="play_game">Play Again</button><button type="submit" name="action" value="home">Home</button>',
                'message': "You won!",
                'word_tiles': request.session['word_tiles']
            })

        # Continue game
        return render(request, 'play_game.html', {
            'guessed_letters': guessed_letters,
            'stickword': word,
            'guessed_wrong_amount': guessed_wrong_amount,
            'word_tiles': request.session['word_tiles']
        })

    # Starting a new game
    else:
        word = random.choice(words_dict[category])
        request.session['word'] = word
        request.session['word_tiles'] = "_" * len(word)
        request.session['guessed_letters'] = ""
        request.session['guessed_wrong_amount'] = 0

        return render(request, 'play_game.html', {
            'stickword': word,
            'guessed_wrong_amount': 0,
            'word_tiles': request.session['word_tiles']
        })


def leaderboard(request):
    return render(request, 'leaderboard.html')
