PROGRAM lec_02
  IMPLICIT NONE

  ! Declaration of variables
  INTEGER, PARAMETER :: nx = 2, ny = 2
  REAL, DIMENSION(nx, ny) :: v_smart, u1, u2

  ! Defining u1 and u2
  u1 = 0.0
  u1(1,1) = 1.0
  u1(2,2) = -1.0
  u2 = u1

  ! Defining v_smart
  v_smart(:, :) = EXP(u1(:, :)) * ABS(u2(:, :))

  ! Printing
  print '(F10.4)', v_smart

END PROGRAM lec_02