# Whack-a-Mole Game

This project is a terminal-based Whack-a-Mole game using **Pygame**. It introduces students to interactive game design using object-oriented principles and real-time graphical rendering.

---

## What’s Provided

A partially working version of a Whack-a-Mole game with:

- A 3x3 grid of holes that randomly pop moles up for a short time
- Mouse-click "whacking" that scores a point when it lands on an active mole
- A countdown timer and score display

You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Clone the repo or download the project folder.
2. Make sure you have Python 3.10+ installed.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the game:

```bash
python main.py
```

---



## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Refine Collision Detection

> A single click can sometimes award two points instead of one, when two neighboring moles are both up and the click lands near the border between their holes. Investigate and enhance click-hit accuracy.


### Task 2: Implement Game Over Condition

> Add a screen that displays the final score once the round timer reaches zero, then gracefully waits for input instead of just printing to the console.


### Task 3: Add Replay Option

> After Game Over, allow the user to play again by choosing a difficulty (Easy, Medium, or Hard mole speed/spawn rate), or exit.



### Task 4: Add Sound Feedback

> Add basic sound effects for a successful whack, a missed click, and the round ending.


---

## Expected Behavior

- Moles pop up at random holes for a short time and go back down if not whacked
- Clicking directly on an active mole scores a point and sends it back down immediately
- Clicking an empty hole (or missing entirely) does not score
- A countdown timer and the current score are visible at all times
- The round ends when the timer reaches zero

---

## Folder Structure

```
whack-a-mole-main/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   └── hole.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
