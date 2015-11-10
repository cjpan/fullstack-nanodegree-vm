#Intro
 A database schema to store the game matches between players. A Python module to rank the players and pair them up in matches in a tournament.
 The game tournament will use the Swiss system for pairing up players in each round: players are not eliminated, and each player should be paired with another player with the same number of wins, or as close as possible.

#How to run
1. Start Vagrant virtual machine
    To use the Vagrant virtual machine, navigate to the full-stack-nanodegree-vm/tournament directory in the terminal, then use the command vagrant up (powers on the virtual machine) followed by vagrant ssh (logs into the virtual machine).  
2. Launches and connects to tournament database:
    vagrant@trusty32: psql tournament -f tournament.sql
3. Run Python unit test module:
    vagrant@trusty32: python tournament_test.py
4. Verify the test result will show "Success! All test pass!".

