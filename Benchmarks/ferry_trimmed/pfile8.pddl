


(define (problem ferry-l13-c9 ) 
(:domain ferry ) 
(:objects l2 l3 l6 l7 l9 l10
c1 c4 c5 c8
)
(:init
(location l2 ) 
(location l3 ) 
(location l6 ) 
(location l7 ) 
(location l9 ) 
(location l10 ) 
(car c1 ) 
(car c4 ) 
(car c5 ) 
(car c8 ) 
(not-eq l2 l3 ) 
(not-eq l3 l2 ) 
(not-eq l2 l6 ) 
(not-eq l6 l2 ) 
(not-eq l2 l7 ) 
(not-eq l7 l2 ) 
(not-eq l2 l9 ) 
(not-eq l9 l2 ) 
(not-eq l2 l10 ) 
(not-eq l10 l2 ) 
(not-eq l3 l6 ) 
(not-eq l6 l3 ) 
(not-eq l3 l7 ) 
(not-eq l7 l3 ) 
(not-eq l3 l9 ) 
(not-eq l9 l3 ) 
(not-eq l3 l10 ) 
(not-eq l10 l3 ) 
(not-eq l6 l7 ) 
(not-eq l7 l6 ) 
(not-eq l6 l9 ) 
(not-eq l9 l6 ) 
(not-eq l6 l10 ) 
(not-eq l10 l6 ) 
(not-eq l7 l9 ) 
(not-eq l9 l7 ) 
(not-eq l7 l10 ) 
(not-eq l10 l7 ) 
(not-eq l9 l10 ) 
(not-eq l10 l9 ) 
(empty-ferry ) 
(at c4 l3 ) 
(at c8 l7 ) 
(at-ferry l3 ) 
 ) 
(:goal
(and
(at c1 l2 ) 
 ) 
 ) 
 ) 


