(define (problem prob ) 
 (:domain barman ) 
(:objects
shaker1 - shaker
left - hand
shot3 shot4 shot13 shot16 - shot
ingredient2 ingredient4 - ingredient
cocktail1 cocktail4 cocktail7 cocktail9 cocktail10 - cocktail
dispenser1 dispenser4 dispenser5 - dispenser
l0 - level
)
 (:init 
  (ontable shaker1 ) 
  (ontable shot3 ) 
  (ontable shot4 ) 
  (ontable shot13 ) 
  (ontable shot16 ) 
  (dispenses dispenser4 ingredient4 ) 
  (clean shaker1 ) 
  (clean shot3 ) 
  (clean shot4 ) 
  (clean shot13 ) 
  (clean shot16 ) 
  (empty shaker1 ) 
  (empty shot3 ) 
  (empty shot4 ) 
  (empty shot13 ) 
  (empty shot16 ) 
  (handempty left ) 
  (shaker-empty-level shaker1 l0 ) 
  (shaker-level shaker1 l0 ) 
  (cocktail-part2 cocktail1 ingredient2 ) 
  (cocktail-part1 cocktail4 ingredient2 ) 
  (cocktail-part2 cocktail7 ingredient4 ) 
  (cocktail-part1 cocktail9 ingredient4 ) 
 ) 
 (:goal
  (and
     (contains shot4 cocktail1 ) 
 )  )  ) 
