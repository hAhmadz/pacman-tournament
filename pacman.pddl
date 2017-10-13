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
            ;;time left for ghost to become active
            (ghostTimer ?timeLeft - time)
            ;; mark homebase
            (homeBase ?loc - index) 	
  ) 

  ;;function to move pacman to next position
  (:action movePacMan
    ;;variables representing index positions of the ghost, before and 
    ;;after the move
    :parameters (?from - index ?to - index)
    ;;Pacman can move when its 'from' index and ghostLoc are the same 
    ;;Pacman can move when from and to indices are cojoined
    :precondition (and (pacmanLoc ?from)
                       (connected ?from ?to)
                       (or (not(ghostLoc ?to))
                           (powerPacman)                    
                        )
                  )
    ;;Pacman position is updated to 'to' index
    ;;Pacman is not at 'from' index
    :effect (and (pacman ?to)
                 (not(pacman ?from))
                 (when(powerFoodLoc ?to)
                      (and (not(powerFoodLoc))
                      (powerPacman))                    
                  )
                  
                  (when (and (not(homeBase))
                             (foodLoc ?to)                            
                         )
                  (not (foodLoc ?to))

                  )

            )

  )

)


  ; ;;function to move pacman to next position
  ; (:action eatFood
  ;   ;;variables representing index positions of the ghost, before and 
  ;   ;;after the move
  ;   :parameters (?from - index ?to - index)
  ;   ;;Pacman can move when its 'from' index and ghostLoc are the same 
  ;   ;;Pacman can move when from and to indices are cojoined
  ;   ;;Food dot at 'to' index
  ;   :precondition (and (pacmanLoc ?from)
  ;                      (connected ?from ?to)
  ;                      (foodLoc ?to))
  ;   ;;Pacman position is updated to 'to' index
  ;   ;;Pacman is not at 'from' index
  ;   ;;Food dot not at 'to' index
  ;   :effect (and (pacman ?to)
  ;                (not(pacman ?from))
  ;                (not(foodDot ?to)))

  ; )

  ; ;;function to move pacman to next position
  ; (:action eatPowerFood
  ;   ;;variables representing index positions of the ghost, before and 
  ;   ;;after the move
  ;   :parameters (?from - index ?to - index)
  ;   ;;Pacman can move when its 'from' index and ghostLoc are the same 
  ;   ;;Pacman can move when from and to indices are cojoined
  ;   ;;Food dot at 'to' index
  ;   :precondition (and (pacmanLoc ?from)
  ;                      (connected ?from ?to)
  ;                      (powerFoodLoc ?to))
  ;   ;;Pacman position is updated to 'to' index
  ;   ;;Pacman is not at 'from' index
  ;   ;;Food dot not at 'to' index
  ;   :effect (and (pacman ?to)
  ;                (not(pacman ?from))
  ;                (not(powerFoodLoc ?to)))

  ; )

  ; ;;function to move pacman to next position
  ; (:action eatGhost
  ;   ;;variables representing index positions of the ghost, before and 
  ;   ;;after the move
  ;   :parameters (?from - index ?to - index)
  ;   ;;Pacman can move when its 'from' index and ghostLoc are the same 
  ;   ;;Pacman can move when from and to indices are cojoined
  ;   ;;When Pacman is powered
  ;   :precondition (and (pacmanLoc ?from)
  ;                      (connected ?from ?to)
  ;                      (powerPacman))
  ;   ;;Pacman position is updated to 'to' index
  ;   ;;Pacman is not at 'from' index
  ;   ;;Food dot not at 'to' index
  ;   :effect (and (pacman ?to)
  ;                (not(pacman ?from))
  ;                (not(ghostLoc ?to)))

  ; )



