(define (problem blocks-7)
(:domain BLOCKS)
(:objects A B C D E F G)
(:INIT (CLEAR A) (ONTABLE A) (CLEAR B) (ONTABLE B) (CLEAR C) (ONTABLE C) (CLEAR D) (ONTABLE D) (CLEAR E) (ONTABLE E) (CLEAR F) (ONTABLE F) (CLEAR G) (ONTABLE G) (HANDEMPTY))
(:goal (AND (ON A B) (ON B C) (ON C D) (ON D E) (ON E F) (ON F G)))
)