include "alldifferent.mzn";

int: N;
int: M = N * N;

set of int: PuzzleRange = 1..M;
set of int: SubSquareRange = 1..N;

array[1..M,1..M] of 0..M: start; %% initial board 0 = empty
array[1..M,1..M] of var PuzzleRange: puzzle;

% fill initial board
constraint forall(i,j in PuzzleRange)(
    if start[i,j] > 0 then puzzle[i,j] = start[i,j] else true endif );

% All different in rows 
constraint forall (i in PuzzleRange) (
                   alldifferent( [ puzzle[i,j] | j in PuzzleRange ]) ); 

% All different in columns.
constraint forall (j in PuzzleRange) (
                   alldifferent( [ puzzle[i,j] | i in PuzzleRange ]) ); 

% All different in sub-squares:
constraint
        forall (a, o in SubSquareRange)(
                alldifferent( [ puzzle[(a-1) *N + a1, (o-1)*N + o1] |
                                        a1, o1 in SubSquareRange ] ) );

solve satisfy;

output [show2d(puzzle)];
% output["ok"];
