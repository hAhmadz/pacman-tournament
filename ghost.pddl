(define (domain ghost)

  (:requirements :typing :conditional-effects :constraints) 

  ;; coordinates x and y on the state space are represented by the
  ;; index variable 
  (:types index
          time)

   ;;location of the static pacman
  (:predicates (pacmanLoc ?loc - index)
               ;;location of the ghost
  			       (ghostLoc ?loc - index) 
               ;;time left for ghost to become active
               (ghostTimer ?timeLeft - time) 
               ;;if ghost is scared and cannot attack pacman
  			       (ghostInActive)
               ;;for adjoining index indices 
  			       (connected ?loc1 ?loc2 - index) 
  ) 

  ;;Assumption: Pacman is static
  (:action moveGhost
    ;;variables representing index positions of the ghost, before and 
    ;;after the move
    :parameters (?from - index ?to - index)
    ;;Ghost can move when its 'from' index and ghostLoc are the same 
    ;;Ghost can move when from and to indices are cojoined
    :precondition (and (ghostLoc ?from)
                       (connected ?from ?to))
    ;;Ghost position is updated to 'to' index
    ;;Ghost is not at 'from' index
    ;;PacMan is not at 'to' index if
    :effect (and (ghostLoc ?to)
                 (not ghostLoc ?from))
  )

  (:action eatPacman
    ;;variables representing index positions of the ghost, before and 
    ;;after the move
    :parameters (?from - index ?to - index)
    ;;Ghost can eat PacMan when it is not inactive
    ;;Ghost can move when its 'from' index and ghostLoc are the same 
    ;;Ghost can move when from and to indices are cojoined
    ;;Ghost can eat PacMan if PacMan is at 'to' index
    :precondition (and (ghostLoc ?from)
                       (connected ?from ?to)
                       (pacmanLoc ?to)
                       (not(ghostInActive)))
    ;;Ghost position is updated to 'to' index
    ;;Ghost is not at 'from' index
    ;;PacMan is not at 'to'
    :effect (and (ghostLoc ?to)
                 (not (ghostLoc ?from)
                 (not (pacman ?to)))

    )

)
