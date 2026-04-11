PROGRAM analytic

    implicit none

    real(8), parameter :: courant_nr = 1.0
    real(8), parameter :: delX = 0.02, c = 1.0
    real(8), parameter :: delT = courant_nr * delX / c
    real(8), parameter :: Lx = 1.0, Lt = 2.2, pi = 4.0 * ATAN(1.0)
    integer, parameter :: Nx = INT(Lx/delX), Nt = INT(Lt/delT)

    integer :: j, n
    real(8) :: x, t, xt
    real(8), dimension(Nt, Nx) :: array

    ! run analytic solution
    DO n = 1, Nt
        t = (n-1) * delT
        DO j = 1, Nx
            x = (j-1) * delX
            xt = MODULO(x - c*t + Lx, Lx)   ! periodic shift 
            if (xt > 0.4 .AND. xt < 0.6) then
                array(n,j) = 0.5 + 0.5*cos(10*pi*(xt - 0.5))
            else
                array(n,j) = 0.0
            end if
        END DO
    END DO


    ! write file
    open(10, file="analytic.txt", status="replace")
    do n = 1, Nt
        write(10, *) array(n, :)
    end do
    close(10)


END PROGRAM analytic

