(define (domain pacman)

  (:requirements :typing :)
  (:types location)
  (:predicates
    (pacmanLoc ?loc - location)
    (ghostLoc ?loc - location)
    (foodLoc ?loc - location)
    (powerFoodLoc ?loc - location)
    (connectedLoc ?loc1 - location ?loc2 - location) 	
  ) 

  (:action movePacMan
    :parameters (?locBefore - location ?locAfter - location)
    :precondition ()
    :effect ()

  )

)
