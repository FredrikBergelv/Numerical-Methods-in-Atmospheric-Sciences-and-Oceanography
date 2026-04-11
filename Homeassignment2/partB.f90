PROGRAM PARTA
    
    IMPLICIT NONE

    REAL :: x_u = 10.4
    REAL, DIMENSION(1:11) :: T_u = 0.0
    REAL :: T_int

    T_u(9)  = 5.0
    T_u(10) = 10.0
    T_u(11) = 20.0

    CALL interp(x_u, T_u, T_int)
    PRINT *, "Tint = ", T_int

CONTAINS

    SUBROUTINE interp(xu, T, Tint)
        IMPLICIT NONE
        REAL, INTENT(IN) :: xu
        REAL, DIMENSION(:), INTENT(IN) :: T
        REAL, INTENT(OUT) :: Tint
        REAL :: ax, xh
        INTEGER :: ip, im

        xh = xu-0.5

        ip = FLOOR(xh) + 1
        im = FLOOR(xh)
        ax = REAL(ip) - xh

        Tint = T(im)*ax + T(ip)*(1 - ax)

    END SUBROUTINE interp

END PROGRAM PARTA