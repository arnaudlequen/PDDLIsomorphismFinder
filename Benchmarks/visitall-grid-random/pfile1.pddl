(define (problem grid-10  ) 
(:domain grid-visit-all ) 
(:objects
loc-x1-y1
loc-x3-y7
loc-x6-y1
loc-x6-y8
loc-x7-y8
loc-x8-y2
loc-x8-y7
loc-x10-y4
loc-x10-y5
loc-x10-y6
- place
)
(:init
	(at-robot loc-x1-y1 ) 
	(visited loc-x1-y1 ) 
	(connected loc-x6-y8 loc-x7-y8 ) 
	(connected loc-x7-y8 loc-x6-y8 ) 
	(connected loc-x10-y4 loc-x10-y5 ) 
	(connected loc-x10-y5 loc-x10-y4 ) 
	(connected loc-x10-y4 loc-x11-y4 ) 
	(connected loc-x11-y4 loc-x10-y4 ) 
	(connected loc-x10-y5 loc-x10-y6 ) 
	(connected loc-x10-y6 loc-x10-y5 ) 
	(connected loc-x10-y5 loc-x11-y5 ) 
	(connected loc-x11-y5 loc-x10-y5 ) 
	(connected loc-x10-y6 loc-x11-y6 ) 
	(connected loc-x11-y6 loc-x10-y6 ) 
 ) 
(:goal
(and
	(visited loc-x1-y1 )  
	(visited loc-x3-y7 ) 
	(visited loc-x6-y1 ) 
	(visited loc-x6-y8 ) 
	(visited loc-x7-y4 ) 
	(visited loc-x7-y8 ) 
	(visited loc-x8-y2 ) 
	(visited loc-x8-y7 ) 
	(visited loc-x10-y4 ) 
	(visited loc-x10-y5 ) 
	(visited loc-x10-y6 ) 
 ) 
 ) 
 ) 
