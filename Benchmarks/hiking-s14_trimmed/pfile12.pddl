(define (problem Hiking-3-4 ) 
(:domain hiking ) 
(:objects
car0 car2 car3 - car
tent0 tent1 - tent
couple1 couple2 - couple
place0 place1 place5 place6 - place
guy0 girl0 guy1 guy2 girl2 - person
)
(:init
(at_person guy0 place0 ) 
(at_person girl0 place0 ) 
(at_tent tent0 place0 ) 
(down tent0 ) 
(at_person guy1 place0 ) 
(walked couple1 place0 ) 
(at_tent tent1 place0 ) 
(down tent1 ) 
(partners couple2 guy2 girl2 ) 
(at_person guy2 place0 ) 
(at_person girl2 place0 ) 
(walked couple2 place0 ) 
(at_car car0 place0 ) 
(at_car car2 place0 ) 
(at_car car3 place0 ) 
(next place0 place1 ) 
(next place5 place6 ) 
 ) 
(:goal
(and
 ) 
 ) 
 ) 
