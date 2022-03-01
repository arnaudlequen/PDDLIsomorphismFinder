(define (problem elevators-sequencedstrips-p40_60_1 ) 
(:domain elevators-sequencedstrips ) 

(:objects
n2 n20 n21 n25 n29 n30 n33 n35 n37 - count
p2 p5 p6 p8 p12 p13 p14 p16 p17 p22 p24 p26 p28 p31 p32 p35 p38 p43 p46 p47 p48 p51 p53 p57 p58 p59 - passenger
fast0 - fast-elevator
slow3-0 - slow-elevator
)

(:init










(passenger-at p12 n2 ) 
(passenger-at p13 n25 ) 
(passenger-at p24 n21 ) 
(passenger-at p28 n25 ) 
(passenger-at p31 n37 ) 
(passenger-at p48 n2 ) 
(passenger-at p51 n35 ) 














(= (total-cost )  0 ) 

 ) 

(:goal
(and
(passenger-at p24 n20 ) 
(passenger-at p35 n21 ) 
(passenger-at p53 n33 ) 
(passenger-at p58 n33 ) 
(passenger-at p59 n21 ) 
 )  ) 

(:metric minimize (total-cost )  ) 

 ) 
