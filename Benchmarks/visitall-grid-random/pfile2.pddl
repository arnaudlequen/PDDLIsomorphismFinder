(define (problem grid-10  ) 
(:domain grid-visit-all ) 
(:objects
loc-x1-y1
loc-x2-y1
loc-x2-y4
loc-x3-y2
loc-x3-y3
loc-x3-y7
loc-x4-y6
loc-x6-y1
loc-x6-y8
loc-x7-y4
loc-x7-y6
loc-x7-y8
loc-x8-y2
loc-x8-y7
loc-x9-y4
loc-x10-y3
loc-x10-y4
loc-x10-y5
loc-x10-y6
loc-x10-y10
- place
)
(:init
	(at-robot loc-x1-y1 ) 
	(visited loc-x1-y1 ) 
	(connected loc-x1-y1 loc-x2-y1 ) 
	(connected loc-x2-y1 loc-x1-y1 ) 
	(connected loc-x3-y2 loc-x3-y3 ) 
	(connected loc-x3-y3 loc-x3-y2 ) 
	(connected loc-x6-y8 loc-x7-y8 ) 
	(connected loc-x7-y8 loc-x6-y8 ) 
	(connected loc-x9-y4 loc-x10-y4 ) 
	(connected loc-x10-y4 loc-x9-y4 ) 
	(connected loc-x10-y3 loc-x10-y4 ) 
	(connected loc-x10-y4 loc-x10-y3 ) 
	(connected loc-x10-y3 loc-x11-y3 ) 
	(connected loc-x11-y3 loc-x10-y3 ) 
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
	(connected loc-x10-y10 loc-x10-y11 ) 
	(connected loc-x10-y11 loc-x10-y10 ) 
	(connected loc-x10-y10 loc-x11-y10 ) 
	(connected loc-x11-y10 loc-x10-y10 ) 
 ) 
(:goal
(and 
	(visited loc-x1-y1 ) 
	(visited loc-x2-y1 ) 
	(visited loc-x2-y4 ) 
	(visited loc-x3-y2 ) 
	(visited loc-x3-y3 ) 
	(visited loc-x3-y7 ) 
	(visited loc-x4-y6 ) 
	(visited loc-x6-y1 ) 
	(visited loc-x6-y8 ) 
	(visited loc-x7-y4 ) 
	(visited loc-x7-y6 ) 
	(visited loc-x7-y8 ) 
	(visited loc-x8-y2 ) 
	(visited loc-x8-y7 ) 
	(visited loc-x9-y4 ) 
	(visited loc-x10-y3 ) 
	(visited loc-x10-y4 ) 
	(visited loc-x10-y5 ) 
	(visited loc-x10-y6 ) 
	(visited loc-x10-y10 ) 
 ) 
 ) 
 ) 
