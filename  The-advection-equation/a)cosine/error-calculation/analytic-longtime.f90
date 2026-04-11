PROGRAM analytic

    implicit none

    real, parameter :: courant_nr = 1.0
    real, parameter :: delX = 0.02, c = 1.0
    real, parameter :: delT = courant_nr * delX / c
    real, parameter :: Lx = 1.0, Lt = 1000, pi = 4.0 * ATAN(1.0)
    integer, parameter :: Nx = INT(Lx/delX), Nt = INT(Lt/delT)

    integer :: j, n
    real :: x, t, xt
    real, dimension(Nt, Nx) :: array

    ! --- travelling cosine wave directly
    DO n = 1, Nt
        t = (n-1) * delT
        DO j = 1, Nx
            x = (j-1) * delX
            xt = MOD(x - c*t, Lx)        ! periodic shift
            array(n,j) = COS(2.0*pi*xt)
        END DO
    END DO

    ! write file
    open(10, file="analytic-longtime.txt", status="replace")
    do n = 1, Nt
        write(10, *) array(n, :)
    end do
    close(10)


END PROGRAM analytic

