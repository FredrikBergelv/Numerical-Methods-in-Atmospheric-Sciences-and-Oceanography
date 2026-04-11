PROGRAM travelling
    implicit none

    real, parameter :: delX=0.05, delT=0.05, c=1.0
    real, parameter :: Lx=1.0, Lt=1.0, x0=0.25, x1=0.75
    integer, parameter :: Nx = INT(Lx/delX), Nt = INT(Lt/delT)

    integer :: j, n, shift, jshift
    real :: x, t
    real, dimension(Nt, Nx) :: array

    ! initialize (t = 0)
    DO j = 1, Nx
        x = (j-1)*delX
        if (x > x0 .AND. x < x1) then
            array(1,j) = 1.0
        else
            array(1,j) = 0.0
        end if
    END DO

    ! travelling wave
    DO n = 2, Nt
        t = (n-1)*delT
        shift = INT(c * t / delX)

        DO j = 1, Nx
            jshift = j - shift

            ! periodic boundary
            DO WHILE (jshift < 1)
                jshift = jshift + Nx
            END DO
            DO WHILE (jshift > Nx)
                jshift = jshift - Nx
            END DO

            array(n,j) = array(1, jshift)
        END DO
    END DO

    ! write file
    open(10, file="travelling-pulse.txt", status="replace")
    do n = 1, Nt
        write(10, *) array(n, :)
    end do
    close(10)

    print*, "done"

END PROGRAM travelling