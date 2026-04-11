PROGRAM lec_02
  IMPLICIT NONE

  ! Declaration of variables
  integer :: iyear, imonth, iday
  character(20) :: ccity
  
  print*, "Introduce date: DD MM YYYY"
  read(*,*) iday, imonth, iyear 
  print*, "Introduce city:"
  read(*,*) ccity

  print*, "date : ", iday, imonth, iyear
  print*, "city : ", ccity


END PROGRAM lec_02