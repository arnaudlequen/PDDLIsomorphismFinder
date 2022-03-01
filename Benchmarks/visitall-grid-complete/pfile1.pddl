(define (problem grid-1 )
(:domain grid-visit-all)
(:objects 
	loc-x1-y1
- place
)
(:init
	(at-robot loc-x1-y1)
	(visited loc-x1-y1)
)
(:goal
(and 
	(visited loc-x1-y1)
)
)
)