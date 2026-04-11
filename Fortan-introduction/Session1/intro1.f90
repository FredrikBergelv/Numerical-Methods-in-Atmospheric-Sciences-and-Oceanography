PROGRAM lec_01
    IMPLICIT NONE
    ! Declaration of variables
    INTEGER :: index1, index2
    REAL :: rvalue1, rvalue2
    REAL, PARAMETER :: pi_single = 4.0 * ATAN(1.0)

    ! Initialization
    index1 = 2
    rvalue1 = 4.5
    rvalue2 = COS(pi_single / 2)
    index2 = INT(rvalue2)

    ! Printing
    PRINT *, 'INTEGER :: ', index1, INT(rvalue1), NINT(rvalue1)
    PRINT *, 'REAL :: ', rvalue1, rvalue1 * index1, REAL(index1)
    PRINT *, 'BOTH :: ', rvalue2, index2
END PROGRAM lec_01
