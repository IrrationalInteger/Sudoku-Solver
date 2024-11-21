# Sudoku Solver

## Overview

A simple CLI interface to load sudoku puzzles, solve them, and save the puzzles to disk.

## Features

- Can solve sudokus of any size.
- Easy to use and check solutions.
- Can solve with SAT Solving, Integer Programming, and Constraint Programming approaches

## Installation

### Prerequisites

- Python 3.x
- `uv` package

You can install the required dependencies using `pip`:

```bash
pip install uv
```
## Setting Up the Project
Clone this repository:

```bash
git clone https://github.com/IrrationalInteger/Sudoku-Solver
cd Sudoku-Solver
```
Install the dependencies:

```bash
uv install
```

## Usage
To run the CLI, you can use the following command:

```bash
python sudoku_cli.py
```

To list all CLI Commands
```bash
help
```

To load a sudoku from a file:

```bash
load <path_to_file>
```
Sudoku Solver supports txt files with the following format:
```bash
_ _ _ _ _ _ _ 6 5
_ _ _ 1 _ 2 8 _ _
_ _ 7 _ _ _ 2 _ _
6 _ 2 _ 1 5 _ 7 _
5 _ 1 _ _ 9 _ 4 2
_ _ _ 4 2 _ _ 3 1
_ 2 _ 8 _ _ 4 _ _
_ 5 _ _ 3 1 _ _ 9
_ 8 _ _ 6 _ 1 _ _
```
If the grid given isn't a perfect square then empty cells are appended to reach the next perfect square larger than the current size 

(Note: Be careful as this can result in an unsolvable sudoku).


To show the currently loaded sudoku:

```bash
 show puzzle
```
To solve the currently loaded puzzle:

```bash
 solve all
```

This solves using all the approaches. Specific solvers can be chosen with the arguments ``` sat ```, ``` ip ```, or ``` cp ```.
To show the current solution:

```bash
 show solution
```

To save the sudoku to a file:

```bash
save <path_to_file>
```

## Running Tests
To run tests, use:

```bash
pytest tests/test_sudoku.py
```