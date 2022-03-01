(define (problem prob ) 
 (:domain barman ) 
(:objects
shaker1 - shaker
left - hand
shot13 - shot
ingredient2 - ingredient
cocktail4 cocktail9 - cocktail
dispenser1 - dispenser
l0 - level
)
 (:init 
  (ontable shaker1 ) 
  (ontable shot13 ) 
  (clean shaker1 ) 
  (clean shot13 ) 
  (empty shaker1 ) 
  (empty shot13 ) 
  (handempty left ) 
  (shaker-empty-level shaker1 l0 ) 
  (shaker-level shaker1 l0 ) 
  (cocktail-part1 cocktail4 ingredient2 ) 
 ) 
 (:goal
  (and
 )  )  ) 
