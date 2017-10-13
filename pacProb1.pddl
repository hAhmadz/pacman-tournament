(define (problem pacProb1)
(:domain pacman)
(:objects  			   	 	
	
		   i_6_0	i_6_1	i_6_2	i_6_3	i_6_4	i_6_5	
		   i_5_0	i_5_1	i_5_2	i_5_3	i_5_4	i_5_5	
		   i_4_0	i_4_1	i_4_2	i_4_3	i_4_4	i_4_5	
		   i_3_0	i_3_1	i_3_2	i_3_3	i_3_4	i_3_5	
		   i_2_0	i_2_1	i_2_2	i_2_3	i_2_4	i_2_5	
		   i_1_0	i_1_1	i_1_2	i_1_3	i_1_4	i_1_5	
		   i_0_0	i_0_1	i_0_2	i_0_3	i_0_4	i_0_5	
- index)

(:init
	  (pacmanLoc i_2_4)
	  (ghostLoc i_5_4)
	  (foodLoc i_3_0)
	  (foodLoc i_6_2)

	  (foodLoc i_3_4)
	  (foodLoc i_0_5)

	  (homeBase i_6_0) (homeBase i_6_1) (homeBase i_6_2)
	  (homeBase i_5_0) (homeBase i_5_1) (homeBase i_5_2)
	  (homeBase i_4_0) (homeBase i_4_1) (homeBase i_4_2)
	  (homeBase i_3_0) (homeBase i_3_1) (homeBase i_3_2)
	  (homeBase i_2_0) (homeBase i_2_1) (homeBase i_2_2)
	  (homeBase i_1_0) (homeBase i_1_1) (homeBase i_1_2)
	  (homeBase i_0_0) (homeBase i_0_1) (homeBase i_0_2)


	  (connected i_6_0 i_6_1) (connected i_6_0 i_5_0)
	  (connected i_5_0 i_5_1) (connected i_5_0 i_4_0)
	  (connected i_4_0 i_4_1) (connected i_4_0 i_3_0)
	  (connected i_3_0 i_3_1) (connected i_3_0 i_2_0)
	  (connected i_2_0 i_2_1) (connected i_2_0 i_1_0)
	  (connected i_1_0 i_1_1) (connected i_1_0 i_0_0)
	  (connected i_0_0 i_0_1)


	  (connected i_6_1 i_6_2) (connected i_6_1 i_5_1)
	  (connected i_5_1 i_5_2) (connected i_5_1 i_4_1)
	  (connected i_4_1 i_4_2) (connected i_4_1 i_3_1)
	  (connected i_3_1 i_3_2) (connected i_3_1 i_2_1)
	  (connected i_2_1 i_2_2) (connected i_2_1 i_1_1)
	  (connected i_1_1 i_1_2) (connected i_1_1 i_0_1)
	  (connected i_0_1 i_0_2)


	  (connected i_6_2 i_6_3) (connected i_6_2 i_5_2)
	  (connected i_5_2 i_5_3) (connected i_5_2 i_4_2)
	  (connected i_4_2 i_4_3) (connected i_4_2 i_3_2)
	  (connected i_3_2 i_3_3) (connected i_3_2 i_2_2)
	  (connected i_2_2 i_2_3) (connected i_2_2 i_1_2)
	  (connected i_1_2 i_1_3) (connected i_1_2 i_0_2)
	  (connected i_0_2 i_0_3)


	  (connected i_6_3 i_6_4) (connected i_6_3 i_5_3)
	  (connected i_5_3 i_5_4) (connected i_5_3 i_4_3)
	  (connected i_4_3 i_5_4) (connected i_4_3 i_3_3)
	  (connected i_3_3 i_3_4) (connected i_3_3 i_2_3)
	  (connected i_2_3 i_2_4) (connected i_2_3 i_1_3)
	  (connected i_1_3 i_1_4) (connected i_1_3 i_0_3)
	  (connected i_0_3 i_0_4) 

	  (connected i_6_4 i_6_5) (connected i_6_4 i_5_4)
	  (connected i_5_4 i_5_5) (connected i_5_4 i_4_4)
	  (connected i_4_4 i_4_5) (connected i_4_4 i_3_4)
	  (connected i_3_4 i_3_5) (connected i_3_4 i_2_4)
	  (connected i_2_4 i_2_5) (connected i_2_4 i_1_4)
	  (connected i_1_4 i_1_5) (connected i_1_4 i_0_4)
	  (connected i_0_4 i_0_5)


	  (connected i_6_5 i_6_6) (connected i_6_5 i_5_5)
	  (connected i_5_5 i_5_6) (connected i_5_5 i_4_5)
	  (connected i_4_5 i_4_6) (connected i_4_5 i_3_5)
	  (connected i_3_5 i_3_6) (connected i_3_5 i_2_5)
	  (connected i_2_5 i_2_6) (connected i_2_5 i_1_5)
	  (connected i_1_5 i_1_6) (connected i_1_5 i_0_5)
	  (connected i_0_5 i_0_6) 


)	  
(:goal
	(and
	  (not(foodLoc i_3_4))
	  (not(foodLoc i_0_5))

	  (or 
	  	(pacmanLoc i_6_2)
	  	(pacmanLoc i_5_2)
	  	(pacmanLoc i_4_2)
	  	(pacmanLoc i_3_2)
	  	(pacmanLoc i_2_2)
	  	(pacmanLoc i_1_2)
	  	(pacmanLoc i_0_2)
	 )

)









