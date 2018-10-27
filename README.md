# **VE593 Project1**
Written by HU Chong, student ID 5151370910114. In this project, 
I implement several seach methods, such as BFS, UCS, DFS, DLS, IDS, A* and MCTS
in this project. Notice that each function has their requirements, please refer
to the comments in the code.


---

If you feel confused about my code, please run `python3 testtime.py -h` 
or `python3 clickomaniaplayer.py -h` for help. And feel free to contact me 
about any issues about this project. 

## Part1

- run the script:  
`python3 testtime.py -n 3`  
By using the option `-n`, we can set the nPuzzle length and test its average running
time. By using `--BFS`, `--UCS`,`--DFS`, `--DLS`, `--IDS`, `--Astar`,
you can select the search method you want to test. Notice MCTS is skipped.

In this part, I get the average time of search methods for 3*3 nPuzzle graph
and notice that not all search methods could get a result within a certain time.
And MCTS is too slow to solve the problem, since I still use the original 
implementation of roll out policy. We may replace the roll out policy to get a 
result.

For other search methods, since I use a trick in the DFS function, by using the
`popitem()` to get the get the last item of the dict, which speed is very fast,
which may generate tens of thousands steps for 3*3 nPuzzle. I assume 
this implementation is OK. 

For other methods, the time cost is considerable for 3\*3 case. 
But for 5\*5 case, I think the time complexity is so huge that none of 
those methods could work well.

## Part2
- run the script:  
`python3 clickomaniaplayer.py`  
You can set the N, M, K by using `-n`, `-m` and `-k`to set N, M, K.
 And you set budget by using `--budget`. I have already given
a default value in the script, don't worry if you don't set a value.
N for height, M for width and K for types. My script will automatically
generate a N\*M case with K types cell to test. And run the MCTS step by step
to get a result. The step state and step score will be reported on the screen.
The penalty will be counted into last step and the final score will be shown
in the last.

We can see from this case that MCTS has its limits. If it could roll out easily,
MCTS will get a not bad solution. Given enough budget, it could even do better.
But if the roll out policy is not fitted, it may get a roll out result through
a lot of steps. It is unwise to apply MCTS to this condition, such as nPuzzle.
If we change the roll out policy, it may affect the MCTS performance in clickomania
situation, which is easy to get a result, but uneasy to get a better solution.






 