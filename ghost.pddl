(define (domain ghost)

  (:requirements :typing)

  (:types index)

  (:predicates (pacmanLoc ?loc s index)
  			   (ghostLoc ?loc s index)
  			   (ghostInActive)
  			   (connectedLoc ?loc1 ?loc2 s index)
  ) 

  (:action moveGhost
    :parameters (?currentLoc s index ?currentLoc s index)
    :precondition ( )
    :effect ()

  )

)
