(define (problem elevators-sequencedstrips-p40_60_1 ) 
(:domain elevators-sequencedstrips ) 

(:objects
n1 n2 n3 n4 n5 n6 n9 n11 n12 n13 n14 n15 n17 n18 n19 n20 n21 n22 n23 n24 n25 n26 n27 n28 n29 n30 n31 n33 n34 n35 n36 n37 n38 n39 - count
p0 p1 p2 p3 p4 p5 p6 p7 p8 p10 p12 p13 p14 p15 p16 p17 p18 p19 p21 p22 p23 p24 p25 p26 p27 p28 p29 p30 p31 p32 p34 p35 p36 p37 p38 p40 p41 p42 p43 p44 p45 p46 p47 p48 p49 p51 p52 p53 p54 p55 p57 p58 p59 - passenger
fast0 fast1 fast3 - fast-elevator
slow0-0 slow1-0 slow3-0 - slow-elevator
)

(:init


(can-hold fast0 n1 )  (can-hold fast0 n2 )  (can-hold fast0 n3 )  (can-hold fast0 n4 )  (can-hold fast0 n5 )  (can-hold fast0 n6 )  

(can-hold fast1 n1 )  (can-hold fast1 n2 )  (can-hold fast1 n3 )  (can-hold fast1 n4 )  (can-hold fast1 n5 )  (can-hold fast1 n6 )  


(lift-at fast3 n20 ) 
(can-hold fast3 n1 )  (can-hold fast3 n2 )  (can-hold fast3 n3 )  (can-hold fast3 n4 )  (can-hold fast3 n5 )  (can-hold fast3 n6 )  

(lift-at slow0-0 n9 ) 
(can-hold slow0-0 n1 )  (can-hold slow0-0 n2 )  (can-hold slow0-0 n3 )  (can-hold slow0-0 n4 )  

(lift-at slow1-0 n12 ) 
(can-hold slow1-0 n1 )  (can-hold slow1-0 n2 )  (can-hold slow1-0 n3 )  (can-hold slow1-0 n4 )  


(lift-at slow3-0 n36 ) 
(can-hold slow3-0 n1 )  (can-hold slow3-0 n2 )  (can-hold slow3-0 n3 )  (can-hold slow3-0 n4 )  

(passenger-at p0 n18 ) 
(passenger-at p2 n17 ) 
(passenger-at p4 n35 ) 
(passenger-at p5 n3 ) 
(passenger-at p6 n38 ) 
(passenger-at p7 n38 ) 
(passenger-at p8 n36 ) 
(passenger-at p10 n34 ) 
(passenger-at p12 n2 ) 
(passenger-at p13 n25 ) 
(passenger-at p14 n13 ) 
(passenger-at p15 n29 ) 
(passenger-at p16 n1 ) 
(passenger-at p17 n11 ) 
(passenger-at p18 n9 ) 
(passenger-at p19 n19 ) 
(passenger-at p21 n11 ) 
(passenger-at p22 n17 ) 
(passenger-at p23 n11 ) 
(passenger-at p24 n21 ) 
(passenger-at p26 n39 ) 
(passenger-at p27 n24 ) 
(passenger-at p28 n25 ) 
(passenger-at p29 n9 ) 
(passenger-at p30 n22 ) 
(passenger-at p31 n37 ) 
(passenger-at p32 n15 ) 
(passenger-at p34 n12 ) 
(passenger-at p35 n38 ) 
(passenger-at p36 n17 ) 
(passenger-at p37 n36 ) 
(passenger-at p40 n27 ) 
(passenger-at p41 n12 ) 
(passenger-at p42 n20 ) 
(passenger-at p43 n23 ) 
(passenger-at p44 n29 ) 
(passenger-at p47 n36 ) 
(passenger-at p48 n2 ) 
(passenger-at p51 n35 ) 
(passenger-at p52 n23 ) 
(passenger-at p53 n22 ) 
(passenger-at p54 n38 ) 
(passenger-at p55 n24 ) 
(passenger-at p59 n38 ) 



(= (travel-slow n20 n21 )  6 )  (= (travel-slow n20 n22 )  7 )  (= (travel-slow n20 n23 )  8 )  (= (travel-slow n20 n24 )  9 )  (= (travel-slow n20 n25 )  10 )  (= (travel-slow n20 n26 )  11 )  (= (travel-slow n20 n27 )  12 )  (= (travel-slow n20 n28 )  13 )  (= (travel-slow n20 n29 )  14 )  (= (travel-slow n20 n30 )  15 )  (= (travel-slow n21 n22 )  6 )  (= (travel-slow n21 n23 )  7 )  (= (travel-slow n21 n24 )  8 )  (= (travel-slow n21 n25 )  9 )  (= (travel-slow n21 n26 )  10 )  (= (travel-slow n21 n27 )  11 )  (= (travel-slow n21 n28 )  12 )  (= (travel-slow n21 n29 )  13 )  (= (travel-slow n21 n30 )  14 )  (= (travel-slow n22 n23 )  6 )  (= (travel-slow n22 n24 )  7 )  (= (travel-slow n22 n25 )  8 )  (= (travel-slow n22 n26 )  9 )  (= (travel-slow n22 n27 )  10 )  (= (travel-slow n22 n28 )  11 )  (= (travel-slow n22 n29 )  12 )  (= (travel-slow n22 n30 )  13 )  (= (travel-slow n23 n24 )  6 )  (= (travel-slow n23 n25 )  7 )  (= (travel-slow n23 n26 )  8 )  (= (travel-slow n23 n27 )  9 )  (= (travel-slow n23 n28 )  10 )  (= (travel-slow n23 n29 )  11 )  (= (travel-slow n23 n30 )  12 )  (= (travel-slow n24 n25 )  6 )  (= (travel-slow n24 n26 )  7 )  (= (travel-slow n24 n27 )  8 )  (= (travel-slow n24 n28 )  9 )  (= (travel-slow n24 n29 )  10 )  (= (travel-slow n24 n30 )  11 )  (= (travel-slow n25 n26 )  6 )  (= (travel-slow n25 n27 )  7 )  (= (travel-slow n25 n28 )  8 )  (= (travel-slow n25 n29 )  9 )  (= (travel-slow n25 n30 )  10 )  (= (travel-slow n26 n27 )  6 )  (= (travel-slow n26 n28 )  7 )  (= (travel-slow n26 n29 )  8 )  (= (travel-slow n26 n30 )  9 )  (= (travel-slow n27 n28 )  6 )  (= (travel-slow n27 n29 )  7 )  (= (travel-slow n27 n30 )  8 )  (= (travel-slow n28 n29 )  6 )  (= (travel-slow n28 n30 )  7 )  (= (travel-slow n29 n30 )  6 )  











(= (total-cost )  0 ) 

 ) 

(:goal
(and
(passenger-at p0 n1 ) 
(passenger-at p1 n13 ) 
(passenger-at p2 n9 ) 
(passenger-at p3 n18 ) 
(passenger-at p4 n25 ) 
(passenger-at p5 n1 ) 
(passenger-at p6 n6 ) 
(passenger-at p7 n31 ) 
(passenger-at p12 n39 ) 
(passenger-at p15 n14 ) 
(passenger-at p17 n34 ) 
(passenger-at p18 n5 ) 
(passenger-at p19 n13 ) 
(passenger-at p21 n15 ) 
(passenger-at p22 n1 ) 
(passenger-at p24 n20 ) 
(passenger-at p25 n21 ) 
(passenger-at p27 n37 ) 
(passenger-at p28 n34 ) 
(passenger-at p29 n35 ) 
(passenger-at p30 n24 ) 
(passenger-at p31 n24 ) 
(passenger-at p34 n37 ) 
(passenger-at p35 n21 ) 
(passenger-at p37 n35 ) 
(passenger-at p40 n21 ) 
(passenger-at p41 n26 ) 
(passenger-at p42 n36 ) 
(passenger-at p43 n4 ) 
(passenger-at p44 n33 ) 
(passenger-at p45 n11 ) 
(passenger-at p46 n36 ) 
(passenger-at p48 n14 ) 
(passenger-at p49 n14 ) 
(passenger-at p51 n28 ) 
(passenger-at p52 n31 ) 
(passenger-at p53 n33 ) 
(passenger-at p54 n33 ) 
(passenger-at p55 n25 ) 
(passenger-at p57 n34 ) 
(passenger-at p58 n33 ) 
(passenger-at p59 n21 ) 
 )  ) 

(:metric minimize (total-cost )  ) 

 ) 
