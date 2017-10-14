(define (domain pacman)

  (:requirements :typing :conditional-effects)

  ;; coordinates x and y on the state space are represented by the
  ;; index variable 
  (:types index)

  ;;location of the static pacman
  (:predicates
            ;;location of the pacman
            (pacmanLoc ?loc - index)
            ;;location of the ghost
            (ghostLoc ?loc - index)
            ;;location of food dot
            (foodLoc ?loc - index)
            ;;location of powerfood pellet
            (powerFoodLoc ?loc - index)
            ;;pacman is powered
            (powerPacman)
            ;;for adjoining index indices 
            (connected ?loc1 ?loc2 - index)
            ;;mark homebase
            (homeBase ?loc - index)
            ;;mark wall coordinates
            (isWall ?loc - index)   
  ) 
  
  ;;function to move pacman to next position
  (:action movePacMan
    ;;variables representing index positions of the ghost, before and 
    ;;after the move
    :parameters (?from - index ?to - index)
    ;;Pacman can move when its 'from' index and ghostLoc are the same 
    ;;Pacman can move when from and to indices are cojoined
    ;;needs to avoid wall
    :precondition (and (pacmanLoc ?from)
                       (connected ?from ?to)
                       (or (not(ghostLoc ?to))
                           (powerPacman))                    
                       (not (isWall ?to))
                  )
    ;;Pacman position is updated to 'to' index
    ;;Pacman is not at 'from' index
    :effect (and (pacmanLoc ?to)
                 (not(pacmanLoc ?from))
                 (when(powerFoodLoc ?to)
                      (and (not(powerFoodLoc ?to))
                      (powerPacman))                    
                  )
                 (when (and (not(homeBase ?to))
                             (foodLoc ?to)                            
                         )
                 (not (foodLoc ?to)))
                  
            )
  )

)

