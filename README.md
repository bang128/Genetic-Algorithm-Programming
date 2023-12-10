# Genetic-Algorithm-Programming
## Objective 
Develop a program for genetic algorithm, randomly generate a list of chromosomes, build selection, crossover and mutation approach to develop new generations.
## Method
- Programmed in Python; utilized random functions from numpy to generate and mutate chromosomes with a given normal distribution; calculated fitness scores.
- Built Roulette Wheel selection to select chromosomes regarding fitness scores.
- Created uniform and 1-kpoint crossover.
## Parameters
- FILE_NAME: filename containing the training data (including .txt extension), this file must be located in the same 
  directory as this Python file (my training file for debugging is genAlgData3.txt)
- CHROMOSOMES: the number of chromosomes in each generation (must be at least 2)
- GENERATIONS: the number of generations the program will run before terminating (must be at least 10)
- X: the percentage for elitist selection (0.0 <= X <= 1.0; X must satisfy that: the remaining number of chromosomes for 
  crossover is at least 2)
- CROSSOVER: crossover algorithm to use; only 'uniform' and '1-point' are acceptable
- Z: mutation rate (0.0 <= Z <= 1.0)
## The Best Combination of Parameters
- FILE_NAME = "genAlgData3.txt"
- CHROMOSOMES = 10
- GENERATIONS = 12
- X = 0.1
- CROSSOVER = '1-point'
- Z = 0.3
<p>Since the size of this file is very small, we need high mutation rate (Z) and low elitist selection percentage (X). 
Warning that with this small file, no mutation (Z = 0.0) may cause an infinite loop because there are more and more 
same chromosomes generated, making crossover algorithm get stuck.</p>

