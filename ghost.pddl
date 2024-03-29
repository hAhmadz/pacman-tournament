(define (domain ghost)

  (:requirements :typing :conditional-effects) 

  ;; coordinates x and y on the state space are represented by the
  ;; index variable 
  (:types index
          time)

   ;;location of the static pacman
  (:predicates (pacmanLoc ?loc - index)
               ;;location of the ghost
               (ghostLoc ?loc - index)  
               ;;if ghost is scared and cannot attack pacman
               (ghostInActive)
               ;;for adjoining index indices 
               (connected ?loc1 ?loc2 - index)
               ;; wall coordinates
               (isWall ?loc - index) 
  ) 

  ;;Assumption: Pacman is static
    (:action moveGhost
      ;;variables representing index positions of the ghost, before and 
      ;;after the move
      :parameters (?from - index ?to - index)
      ;;Ghost can move when its 'from' index and ghostLoc are the same 
      ;;Ghost can move when from and to indices are cojoined 
      ;;needs to avoid wall
      :precondition (and (ghostLoc ?from)
                         (connected ?from ?to)
                         (not(isWall ?to)))
      ;;Ghost position is updated to 'to' index
      ;;Ghost is not at 'from' index
      :effect (and (ghostLoc ?to)
                   (not (ghostLoc ?from))
                     (when (not(ghostInActive))
                           (not(pacmanLoc ?to))
                     )
                   )
    )
)
  
  

